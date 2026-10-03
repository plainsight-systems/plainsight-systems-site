---
# LAYOUT FIXTURE. Draft only: never published (hugo builds without -D).
# Exercises every part of layouts/research/single.html.
title: "Paper Layout Fixture"
subtitle: "A draft page that exercises every element of the research paper template"
date: 2026-10-03
version: "0.1"
status: working-paper
draft: true
authors:
  - given: Andrew P
    family: Hunter
    orcid: 0009-0005-7613-8019
    affiliation: Plainsight Systems
abstract: |
  This page is a layout fixture, not a paper. It exists so the research
  paper template can be checked in a browser: the header, the action row,
  the abstract, the contents rail, headings at two levels, a table, a
  code block, a block quote, and footnotes. It is marked as a draft, so
  production builds never include it.
pdf: paper-layout-fixture.pdf
keywords: [layout, fixture]
---

## Introduction

The body column holds the reading measure at 44rem and starts on the same left edge as the navigation. Long paragraphs should wrap comfortably at this width on a desktop screen and reflow without horizontal scrolling on a phone. This sentence is here to make the paragraph long enough to show three or more lines of text at the widest breakpoint.

A second paragraph checks spacing between paragraphs, and carries a footnote marker.[^1]

## Background

### A third-level heading

Third-level headings appear indented in the contents rail. The rail is sticky on wide screens and drops above the body as a plain list below 1024px.

> A block quote, set off from the body by a rule on its left.

### A table

| Element | Where it renders | Checked by |
|---|---|---|
| Action row | Page header | Download, Cite, DOI |
| Contents | Right rail or above body | Viewport width |
| Footnotes | End of body | Back-links |

## Method

A code block checks monospace setting and horizontal overflow:

```
scripts/build-paper.sh paper-layout-fixture   # resolves citations, renders the PDF
```

Inline code such as `index.md` should sit in the line without changing its height.

## Results

This section is short on purpose, to check the spacing between consecutive headings and short paragraphs.

## Conclusion

The fixture ends here. Its footnote follows.[^2]

[^1]: Footnotes render as endnotes, set smaller, with a link back to their marker.
[^2]: A second footnote checks numbering.
