#!/usr/bin/env python3
"""Refresh project article metadata from complete RSS feeds.

The project registry owns feed URLs and display names. Each successful feed
replaces that source's snapshot, including removals; a failed source keeps its
last good snapshot and warns. A new source without a usable snapshot fails.
Only public metadata enters Hugo. Project links retain their edition while
canonical RSS GUIDs allow syndicated copies to be deduplicated by the template.
CI persists the snapshot in its cache; a checked-in seed supports offline builds.
"""

import argparse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
import http.client
import json
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 2 * 1024 * 1024


class PlainText(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.feed(text)

    def handle_data(self, data):
        self.parts.append(data)


def plain(text):
    return ' '.join(' '.join(PlainText(text).parts).split())


def https_url(value):
    if not isinstance(value, str):
        raise ValueError('Expected an HTTPS URL')
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or
            parsed.password or any(c.isspace() for c in value)):
        raise ValueError(f'Invalid public HTTPS URL: {value!r}')
    return value


def sources_from(path):
    sources = {}
    for project in yaml.safe_load(path.read_text()):
        if 'feed' not in project:
            continue
        feed = https_url(project['feed'])
        name = project.get('writing_name')
        if not isinstance(name, str) or not name.strip() or feed in sources:
            raise ValueError('Feed entries need a unique feed URL and writing_name')
        sources[feed] = name
    return sources


def parse_feed(raw, feed, now):
    if len(raw) > MAX_BYTES or b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('Oversized feed or unsupported XML declaration')
    root = ET.fromstring(raw)
    channel = root.find('channel')
    if root.tag != 'rss' or channel is None or not channel.findtext('title'):
        raise ValueError('Expected an RSS channel with a title')
    items, seen = [], set()
    for entry in channel.findall('item'):
        title = (entry.findtext('title') or '').strip()
        url = https_url((entry.findtext('link') or '').strip())
        # A feed may identify a canonical edition elsewhere, but its reading
        # links belong to the registered project site.
        if urlsplit(url).netloc != urlsplit(feed).netloc:
            raise ValueError(f'Article link is outside the project site: {url}')
        guid = entry.find('guid')
        canonical = https_url(guid.text.strip()) if (
            guid is not None and guid.get('isPermaLink', 'true') == 'true' and guid.text
        ) else url
        published = parsedate_to_datetime(entry.findtext('pubDate') or '')
        if not title or published.tzinfo is None:
            raise ValueError('Articles need a title and a timezone-aware publication date')
        if published > now:
            continue
        identity = canonical.rstrip('/')
        if identity in seen:
            continue
        seen.add(identity)
        items.append(dict(title=title, url=url, canonical_url=canonical,
                          date=published.date().isoformat(),
                          published=published.isoformat(),
                          summary=plain(entry.findtext('description') or '')))
    return sorted(items, key=lambda item: (item['published'], item['url']), reverse=True)


def fetch(feed):
    request = Request(feed, headers={'User-Agent': 'Plainsight-Writing-Index/1.0',
                                    'Accept': 'application/rss+xml, application/xml, text/xml'})
    with urlopen(request, timeout=20) as response:
        https_url(response.url)
        return response.read(MAX_BYTES + 1)


def read_snapshot(path):
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f'{path}: expected a snapshot object')
    # Validate persisted metadata before it can become an outage fallback.
    for feed, source in data.items():
        https_url(feed)
        datetime.fromisoformat(source['fetched_at'])
        if not isinstance(source['items'], list):
            raise ValueError(f'{path}: expected an article list')
        for item in source['items']:
            https_url(item['url'])
            https_url(item['canonical_url'])
            if urlsplit(item['url']).netloc != urlsplit(feed).netloc:
                raise ValueError(f'{path}: article link is outside its project')
            published = datetime.fromisoformat(item['published'])
            if published.tzinfo is None or item['date'] != published.date().isoformat():
                raise ValueError(f'{path}: invalid article publication date')
            if not item['title'] or not isinstance(item['summary'], str):
                raise ValueError(f'{path}: invalid article metadata')
    return data


def refresh(sources, previous, loader=fetch, now=None):
    now = now or datetime.now(timezone.utc)
    result, warnings = {}, []
    for feed in sources:
        try:
            items = parse_feed(loader(feed), feed, now)
            result[feed] = dict(fetched_at=now.isoformat(), items=items)
        except (OSError, ValueError, ET.ParseError, http.client.HTTPException) as exc:
            if feed not in previous:
                raise ValueError(f'{feed}: refresh failed with no saved articles: {exc}') from exc
            result[feed] = previous[feed]
            warnings.append(f'{feed}: using saved articles ({exc})')
        # Cached future entries must not become public either.
        result[feed] = {**result[feed], 'items': [item for item in result[feed]['items']
                       if datetime.fromisoformat(item['published']) <= now]}
    return result, warnings


def write_snapshot(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     delete=False) as output:
        temporary = Path(output.name)
        output.write(text)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry', type=Path, default=ROOT / 'data/featured_repos.yaml')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/project_writing.json')
    parser.add_argument('--cache', type=Path, default=ROOT / '.cache/project_writing.json')
    parser.add_argument('--feed-file', action='append', default=[], metavar='URL=PATH',
                        help='Use a locally built production feed for initial seeding or verification')
    args = parser.parse_args()
    sources = sources_from(args.registry)
    previous = read_snapshot(args.output)
    try:
        cached = read_snapshot(args.cache)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'WARNING: ignoring invalid feed cache ({exc})', file=sys.stderr)
        cached = {}
    for feed, source in cached.items():
        if feed not in previous or source['fetched_at'] > previous[feed]['fetched_at']:
            previous[feed] = source
    local = dict(value.split('=', 1) for value in args.feed_file)
    if local.keys() - sources.keys():
        parser.error('--feed-file must name a registered feed')
    result, warnings = refresh(sources, previous,
                               lambda feed: Path(local[feed]).read_bytes() if feed in local else fetch(feed))
    for warning in warnings:
        print(f'WARNING: {warning}', file=sys.stderr)
    write_snapshot(args.output, result)
    write_snapshot(args.cache, result)
    print(f"Writing: {sum(len(source['items']) for source in result.values())} articles from "
          f"{len(result)} projects; {len(warnings)} source(s) using saved data.")


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        sys.exit(f'Writing refresh failed: {exc}')
