# Where to publish

Venue survey for Plainsight Systems papers. Checked 2026-10-03; deadlines
and page limits change every cycle, so confirm on the venue's own call for
papers before writing to a limit.

The site is the first home for every paper: its page carries Google Scholar
`citation_*` tags and a PDF, which is what Scholar indexes. Everything
below is a second home: a timestamped preprint, a DOI, or peer review.

## Preprints and DOIs (no venue choice needed)

| Option | Gate | What it gives | Notes |
|---|---|---|---|
| **Zenodo** (CERN) | None | Free DOI, versioned, linked to ORCID | Fills the site's empty `doi` slot. Deposit the PDF at each version. |
| **TechRxiv** (IEEE) | Moderator screen only: genuine research, in scope, not plagiarized. Not peer review, no endorsement. | DOI per preprint, citable | IEEE's own preprint server for EE, CS and related technology. Any file format, 10 MB per file. Natural pair with an IEEE venue. |
| **arXiv** | Since 2026-01-21, a first submission to a category needs an institutional email *and* a prior paper in that category, **or** a personal endorsement from an established arXiv author in that category. | The default discovery channel in ML and IT | Build the bundle with `scripts/build-paper.sh <slug> --arxiv`. Categories for the BPE paper: cs.CL, cs.LG, cs.IT. Line up an endorser early; anyone with prior papers in the category can endorse. |

## Peer-reviewed venues, by how the paper is framed

The template follows the venue. The site PDF and the arXiv bundle work for
any of them as a preprint; a venue's own LaTeX style is built only once a
venue is chosen.

### BPE / tokenization paper

| Framing | Venue | Publisher | Format and fit |
|---|---|---|---|
| Information theory: vocabulary size derived from bounded-learner measures | **ISIT** (IEEE International Symposium on Information Theory) | IEEE IT Society | 2026 cycle: 5 pages plus an optional 6th page of references only, 10 pt minimum, template margins unchanged; deadline was 2026-01-16, so the next is roughly January 2027. Expects a formal result. |
| | **IEEE Transactions on Information Theory**, **ITW** (IT Workshop) | IEEE IT Society | Journal (long form) or workshop. Same expectation of a formal result. |
| Compression: BPE as a dictionary coder whose vocabulary falls out of the learner | **DCC** (Data Compression Conference) | IEEE | Most natural IEEE home. Re-Pair, BPE's dictionary-compression ancestor in the Shannon lineage, was published at DCC 1999 (Larsson and Moffat, Snowbird, pp. 296–305). |
| ML: the Charlotte sweep, where vocabulary size peaks for a compute budget | **TMLR** (Transactions on Machine Learning Research) | Independent | Rolling submissions, open review on OpenReview, judged on technical correctness over subjective significance. No deadline, no prestige filter on topic. Best fit for an independent empirical paper. |
| | NeurIPS, ICLR, ICML | Independent | Annual deadlines, each with its own style file (author-year citations). Where Tao et al., Zouhar et al. and the epiplexity paper publish. |
| | ACL, EMNLP | ACL | Tokenization work lands here; submissions go through ACL Rolling Review on OpenReview. |

OpenReview (TMLR, ICLR, ACL) needs an account; profiles without an
institutional email may be held for moderation, so create one well before
a deadline.

### Inference and GPU performance work

| Venue | Publisher | Fit |
|---|---|---|
| **ISPASS** (Performance Analysis of Systems and Software) | IEEE | Measured performance studies: ROCm silent fallbacks, KV-cache tiering, decode bandwidth. |
| **IISWC** (Workload Characterization) | IEEE | Characterizing inference workloads on real hardware. |

For IC roles in inference and GPU performance, a paper here likely carries
more hiring signal than an information-theory paper.

## Decision rule

1. Publish on the site, with a Zenodo DOI, as soon as a paper is ready.
2. Post a preprint: arXiv once endorsed, TechRxiv if not.
3. Choose the peer-reviewed venue from the result: a clean derivation
   points to ISIT or DCC; a measured scaling curve points to TMLR or an
   ML conference. Then build that venue's template.

## Sources

- arXiv endorsement policy (2026-01-21): <https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/>
- arXiv TeX processors: <https://info.arxiv.org/help/faq/texlive.html>
- TechRxiv FAQ: <https://www.techrxiv.org/faqs>
- ISIT 2026 information for authors: <https://2026.ieee-isit.org/information-authors>
- TMLR: <https://jmlr.org/tmlr/>
- Re-Pair at DCC 1999: <https://en.wikipedia.org/wiki/Re-Pair>
