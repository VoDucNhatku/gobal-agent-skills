# Code Discovery Procedure

Ordered search strategy for finding official or third-party code for a paper.
Read this file; reference it, never inline it.

## Search Order

1. **Papers With Code** — paperswithcode.com/paper/<arxiv-id>
   - Official links, implementations ranked by stars
2. **arXiv page** — arxiv.org/abs/<id>
   - Check "Ancillary files" and "Comments" for code links
3. **GitHub search** — github.com/search?q=<paper-title-keywords>
   - Filter by Python/Jupyter, sort by stars, check recency
4. **Hugging Face** — huggingface.co/models?search=<model-name>
   - For models that have HF integration

## Evaluation Criteria

| Factor | Good sign | Red flag |
|--------|-----------|----------|
| Stars | >500 stars, active commits | 0 stars, no activity |
| Author | Official lab/author account | Random user, no bio |
| Readme | Has requirements, how-to-run | Empty or vague |
| Tests | Has test suite | No tests at all |
| Last commit | <6 months | >2 years stale |
| License | Permissive (MIT/Apache) | No license or GPL |

## Fallback

If no code found after all 4 sources, implement from the method note (notes/<id>-method.md recipe mode) + paper PDF equations.
