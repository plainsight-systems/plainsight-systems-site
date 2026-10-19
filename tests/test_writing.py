"""Publication contracts: outage retention, dates, edits/removals and syndication.

RSS parsing uses real XML; the HTML integration runs Hugo against isolated data
and checks both consumers of the shared index. No network is needed by tests.
"""
import importlib.util
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import yaml
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('refresh_writing', ROOT / 'scripts/refresh-writing.py')
writing = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(writing)
FEED = 'https://project.example/writing/index.xml'
NOW = datetime(2026, 10, 13, 18, tzinfo=timezone.utc)


def feed(title='A & B', slug='article', date='Tue, 13 Oct 2026 00:00:00 +0000', guid=None):
    url = f'https://project.example/writing/{slug}/'
    item = (f'<item><title>{escape(title)}</title><link>{url}</link>'
            f'<guid isPermaLink="true">{guid or url}</guid><pubDate>{date}</pubDate>'
            '<description>&lt;p&gt;A &amp; B: checked GPU work.&lt;/p&gt;</description></item>')
    return f'<rss version="2.0"><channel><title>Project</title>{item}</channel></rss>'.encode()


class FeedTests(unittest.TestCase):
    def test_metadata_preserves_title_and_canonical_identity(self):
        item, = writing.parse_feed(feed(guid='https://author.example/article/'), FEED, NOW)
        self.assertEqual(item['title'], 'A & B')
        self.assertEqual(item['summary'], 'A & B: checked GPU work.')
        self.assertEqual(item['canonical_url'], 'https://project.example/writing/article/')
        self.assertEqual(item['url'], 'https://project.example/writing/article/')
        self.assertEqual(item['date'], '2026-10-13')

    def test_future_articles_and_duplicates_do_not_enter_index(self):
        self.assertEqual(writing.parse_feed(feed(date='Thu, 01 Jan 2099 00:00:00 +0000'), FEED, NOW), [])
        raw = feed()
        item = raw[raw.index(b'<item>'):raw.index(b'</item>') + 7]
        raw = raw.replace(b'</channel>', item + b'</channel>')
        self.assertEqual(len(writing.parse_feed(raw, FEED, NOW)), 1)

    def test_invalid_feed_cannot_replace_saved_articles(self):
        prior = {FEED: dict(fetched_at=NOW.isoformat(), items=writing.parse_feed(feed(), FEED, NOW))}
        for broken in (b'<html>Not a feed</html>', b'<rss>', feed(date='invalid'),
                       feed().replace(b'https://project.example/writing/article/', b'javascript:alert(1)'),
                       b'<!DOCTYPE rss>' + feed(), b'x' * (writing.MAX_BYTES + 1)):
            with self.subTest(broken=broken[:70]):
                result, warnings = writing.refresh({FEED: 'Project'}, prior, lambda _: broken, NOW)
                self.assertEqual(result, prior)
                self.assertEqual(len(warnings), 1)

    def test_one_outage_does_not_stop_another_project_refreshing(self):
        second = 'https://second.example/index.xml'
        prior = {FEED: dict(fetched_at=NOW.isoformat(), items=writing.parse_feed(feed(), FEED, NOW))}
        def load(url):
            if url == FEED:
                raise OSError('offline')
            return feed(title='New work').replace(b'project.example', b'second.example')
        result, warnings = writing.refresh({FEED: 'Project', second: 'Second'}, prior, load, NOW)
        self.assertEqual(result[FEED], prior[FEED])
        self.assertEqual(result[second]['items'][0]['title'], 'New work')
        self.assertEqual(len(warnings), 1)

    def test_new_source_failure_is_explicit(self):
        with self.assertRaisesRegex(ValueError, 'no saved articles'):
            writing.refresh({FEED: 'Project'}, {}, lambda _: b'<html/>', NOW)

    def test_cli_recovers_from_corrupt_cache_using_production_feed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            registry, output, cache, xml = [root / name for name in
                                           ['projects.yaml', 'snapshot.json', 'cache.json', 'feed.xml']]
            registry.write_text(f'- repo: example/project\n  feed: {FEED}\n  writing_name: Project\n')
            cache.write_text('not JSON')
            xml.write_bytes(feed(date='Wed, 01 Jan 2020 00:00:00 +0000'))
            run = subprocess.run([sys.executable, str(ROOT / 'scripts/refresh-writing.py'),
                                  '--registry', str(registry), '--output', str(output),
                                  '--cache', str(cache), '--feed-file', f'{FEED}={xml}'],
                                 check=True, capture_output=True, text=True)
            self.assertIn('ignoring invalid feed cache', run.stderr)
            self.assertEqual(writing.read_snapshot(output), writing.read_snapshot(cache))
            self.assertEqual(writing.read_snapshot(output)[FEED]['items'][0]['title'], 'A & B')

    def test_success_replaces_source_and_removes_unregistered_sources(self):
        prior = {FEED: dict(fetched_at=NOW.isoformat(), items=writing.parse_feed(feed(), FEED, NOW)),
                 'https://removed.example/feed': dict(fetched_at=NOW.isoformat(), items=[])}
        result, warnings = writing.refresh({FEED: 'Project'}, prior, lambda _: feed(title='Corrected', slug='new'), NOW)
        self.assertEqual(list(result), [FEED])
        self.assertEqual([i['title'] for i in result[FEED]['items']], ['Corrected'])
        empty = b'<rss><channel><title>Project</title></channel></rss>'
        result, _ = writing.refresh({FEED: 'Project'}, result, lambda _: empty, NOW)
        self.assertEqual(result[FEED]['items'], [])
        self.assertFalse(warnings)

    def test_persisted_snapshot_is_validated_and_future_cache_filtered(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'snapshot.json'
            snapshot = {FEED: dict(fetched_at=NOW.isoformat(), items=writing.parse_feed(feed(), FEED, NOW))}
            writing.write_snapshot(path, snapshot)
            self.assertEqual(writing.read_snapshot(path), snapshot)
            snapshot[FEED]['items'][0]['canonical_url'] = 'https://author.example/article/'
            writing.write_snapshot(path, snapshot)
            migrated = writing.read_snapshot(path)
            self.assertEqual(migrated[FEED]['items'][0]['canonical_url'],
                             'https://project.example/writing/article/')
            result, _ = writing.refresh({FEED: 'Project'}, snapshot, lambda _: b'invalid',
                                        datetime(2020, 1, 1, tzinfo=timezone.utc))
            self.assertEqual(result[FEED]['items'], [])
            snapshot[FEED]['items'][0]['url'] = 'javascript:alert(1)'
            writing.write_snapshot(path, snapshot)
            with self.assertRaises(ValueError):
                writing.read_snapshot(path)


class WorkflowTests(unittest.TestCase):
    def test_schedule_stays_active_without_granting_deploy_write_access(self):
        workflow = yaml.safe_load((ROOT / '.github/workflows/deploy.yaml').read_text())
        keepalive = workflow['jobs']['keep-schedule-active']
        self.assertEqual(keepalive['if'], "github.event_name == 'schedule'")
        self.assertEqual(keepalive['permissions'], {'actions': 'write'})
        self.assertEqual(workflow['permissions'], {'contents': 'read'})
        self.assertNotIn('permissions', workflow['jobs']['deploy'])
        self.assertIn('actions/workflows/deploy.yaml/enable', keepalive['steps'][0]['run'])
        self.assertFalse(any('uses' in step for step in keepalive['steps']))
        for step in workflow['jobs']['deploy']['steps']:
            if step.get('name') in {'Deploy (Wrangler)', 'Refresh project articles', 'Save publication snapshots'}:
                self.assertEqual(step['if'], "github.event_name != 'pull_request'")


class RenderTests(unittest.TestCase):
    def test_registered_articles_reach_both_lists_once_and_are_searchable(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'data').mkdir()
            (root / 'layouts').mkdir()
            (root / 'content/research').mkdir(parents=True)
            (root / 'hugo.toml').write_text('baseURL = "https://hub.example/"\ndisableKinds = ["taxonomy", "term", "RSS"]\n')
            for name in ['featured_repos.yaml', 'project_writing.json', 'writing.yaml']:
                shutil.copy(ROOT / 'data' / name, root / 'data' / name)
            # A curated copy of Cradle's canonical edition must not duplicate it.
            with (root / 'data/writing.yaml').open('a') as output:
                output.write('\n- title: Duplicate canonical edition\n  kind: article\n'
                             '  url: https://andrewphunter.com/writing/cradle-01-the-cradle/\n'
                             '  canonical_url: https://cradle.plainsight-systems.com/lessons/01-the-cradle/\n'
                             '  venue: Personal site\n  date: 2026-10-13\n')
            shutil.copytree(ROOT / 'layouts/partials/writing', root / 'layouts/partials/writing')
            template = '{{ partial "writing/list.html" (dict "items" (partial "writing/items.html" .) "filter" false) }}'
            (root / 'layouts/index.html').write_text(template)
            (root / 'layouts/research').mkdir()
            (root / 'layouts/research/list.html').write_text(template.replace('"filter" false', '"filter" true'))
            (root / 'content/research/_index.md').write_text('---\ntitle: Research\n---\n')
            subprocess.run(['hugo', '--source', str(root), '--clock', '2026-10-14T00:00:00Z',
                            '--panicOnWarning'], check=True, capture_output=True)
            for name in ['index.html', 'research/index.html']:
                html = (root / 'public' / name).read_text()
                for title in ['Milestone 2: reusing work with ReSTIR', 'Milestone 1: building the baseline',
                              'Prologue: Getting the cradle ready', 'The cradle']:
                    self.assertIn(title, html)
                self.assertNotIn('Duplicate canonical edition', html)
                self.assertEqual(html.count('href="https://cradle.plainsight-systems.com/lessons/01-the-cradle/"'), 1)
                self.assertIn('class="ps-writing__summary"', html)
                self.assertIn('data-about="Cradle"', html)
                self.assertLess(html.index('Milestone 2: reusing'), html.index('Milestone 1: building'))


if __name__ == '__main__':
    unittest.main()
