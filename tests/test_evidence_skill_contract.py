"""Authored-presence contracts only; these tests do not test model behavior.

Passing proves that the canonical instructions and example expose the reviewed
contract. Semantic source support and IDE execution require separate evaluation.
"""

import unittest
from pathlib import Path

import yaml

from scripts.skill_manifest import load_frontmatter


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".claude" / "skills"
ADMIN = SKILLS / "admin"


class EvidenceSkillContractTests(unittest.TestCase):
    def test_rule_worker_resource_has_an_explicit_owner_path(self):
        text = self.read(".claude/rules/latex-katex-compat.md")
        self.assertIn("`~/.claude/skills/latex-fix/scripts/latex_lint.py`", text)
        self.assertNotIn("the bundled `scripts/latex_lint.py`", text)

    def test_skill_authoring_distinguishes_canonical_and_portable_hosts(self):
        text = self.read(".claude/skills/writing-skills/SKILL.md")
        for term in ("Target host", "Canonical", "Antigravity IDE", "only `name` and `description`",
                     "Do not add `allowed-tools` or `argument-hint`"):
            self.assertContains(text, term)

    def test_metadata_does_not_embed_a_canonical_home_dependency(self):
        for source in SKILLS.glob("*/SKILL.md"):
            with self.subTest(skill=source.parent.name):
                metadata, _ = load_frontmatter(source, canonical=True)
                self.assertNotIn("~/.claude", metadata["description"])

    def test_worktree_policy_preserves_dirty_user_work(self):
        text = self.read(".claude/skills/using-git-worktrees/SKILL.md")
        for unsafe in ("git stash          # If", "Cannot create worktree with uncommitted changes",
                       "git worktree remove -f", "git branch -D"):
            self.assertNotIn(unsafe, text)
        for required in ("Uncommitted changes in the source do not prevent", "Do not automatically stash",
                         "explicit user authorization", "exact target"):
            self.assertContains(text, required)

    def assertContains(self, text, term):
        normalized = " ".join(text.casefold().split())
        wanted = " ".join(term.casefold().split())
        self.assertTrue(wanted in normalized, f"Missing authored invariant: {term}")

    def read(self, relative):
        path = ROOT / relative
        self.assertTrue(path.is_file(), f"Missing authored contract: {relative}")
        return path.read_text(encoding="utf-8")

    def test_admin_is_compact_and_routes_details_on_demand(self):
        _, body = load_frontmatter(ADMIN / "SKILL.md", canonical=True)
        self.assertGreaterEqual(len(body.splitlines()), 100)
        self.assertLessEqual(len(body.splitlines()), 160)
        for lane in ("Fast non-research", "Quick evidence", "Standard evidence", "Deep evidence"):
            self.assertIn(lane, body)
        for ref in ("research-protocol.md", "source-quality.md", "claim-ledger.md", "dispatch-protocol.md"):
            self.assertIn(f"references/{ref}", body)
            self.assertTrue((ADMIN / "references" / ref).is_file())

    def test_universal_rule_is_short_and_preserves_trust_boundary(self):
        rule = self.read(".claude/rules/evidence-first.md")
        self.assertGreaterEqual(len(rule.split()), 100)
        self.assertLessEqual(len(rule.split()), 150)
        for term in ("USER_REPORTED", "OBSERVED_VERIFIED", "dependent", "untrusted data", "not instructions"):
            self.assertContains(rule, term)
        self.assertIn("registration", rule)
        self.assertIn("activation", rule)

    def test_fact_provenance_and_calibration_contract(self):
        text = self.read(".claude/skills/admin/references/research-protocol.md")
        for term in ("USER_REPORTED", "OBSERVED_VERIFIED", "LOOKUP", "DERIVE", "ASSUMPTION_OR_UNKNOWN",
                     "SUPPORTED", "REFUTED", "CONTESTED", "NEI", "dependent", "untrusted data"):
            self.assertContains(text, term)
        self.assertNotIn("VERIFIED_OR_GIVEN", text)
        self.assertIn("Search snippets", text)
        self.assertIn("not evidence", text)

    def test_lane_limits_are_request_global_design_ceilings(self):
        text = self.read(".claude/skills/admin/references/research-protocol.md")
        for row in ("| Quick evidence | 1 | 3 | 2 | 0 |",
                    "| Standard evidence | 2 | 6 | 6 | 0 by default |",
                    "| Deep evidence | 3 | 12 | 12 | min(host capacity, 3) |"):
            self.assertIn(row, text)
        for term in ("design ceilings", "not measured optimum", "entire request", "aggregate budget", "remaining"):
            self.assertContains(text, term)
        self.assertContains(text, "release")
        self.assertContains(text, "not on each")

    def test_retained_source_text_is_bounded_across_workers(self):
        text = self.read(".claude/skills/admin/references/research-protocol.md")
        for term in ("20,000", "60,000", "120,000", "retained source characters", "not per worker"):
            self.assertIn(term, text)

    def test_source_contract_requires_entailment_origin_and_context(self):
        text = self.read(".claude/skills/admin/references/source-quality.md")
        for term in ("entail", "origin_id", "Vietnamese", "international", "primary", "jurisdiction",
                     "published_at", "accessed_at", "conflict", "retraction", "Real URL"):
            self.assertContains(text, term)
        self.assertIn("not semantic proof", text)

    def test_ledger_contract_has_review_and_answer_mapping(self):
        text = self.read(".claude/skills/admin/references/claim-ledger.md")
        for term in ("schema_version", "passage", "locator", "stance", "reviewer", "reviewed_at", "pending",
                     "derived_from_claim_ids", "fatal_flags", "corroboration_required", "statement_id",
                     "claim_ids", "cited_source_ids", "derivation_review", "derivation_rationale",
                     "structural", "semantic"):
            self.assertContains(text, term)

    def test_example_records_an_inspected_passage_and_answer_mapping(self):
        data = yaml.safe_load(self.read(".claude/skills/admin/resources/claim-ledger.example.yml"))
        self.assertEqual(data["schema_version"], 1)
        source = data["sources"][0]
        for key in ("source_id", "canonical_url", "title", "origin_id", "source_type", "accessed_at"):
            self.assertIn(key, source)
        self.assertEqual(source["canonical_url"], "https://antigravity.google/docs/skills?tab=ide")
        claim = data["claims"][0]
        self.assertEqual(claim["status"], "SUPPORTED")
        for key in ("claim_id", "text_atomic", "risk", "evidence", "derived_from_claim_ids", "fatal_flags",
                    "corroboration_required", "conflicts"):
            self.assertIn(key, claim)
        edge = claim["evidence"][0]
        self.assertIn("required `SKILL.md` file", edge["passage"])
        self.assertEqual(edge["review"]["status"], "accepted")
        self.assertTrue(edge["review"]["reviewer"])
        self.assertEqual(data["output"][0]["claim_ids"], [claim["claim_id"]])
        self.assertEqual(data["output"][0]["cited_source_ids"], [source["source_id"]])
        pending = data["claims"][1]
        self.assertEqual(pending["status"], "NEI")
        self.assertEqual(pending["evidence"], [])
        self.assertEqual(pending["derived_from_claim_ids"], [claim["claim_id"]])
        self.assertEqual(pending["derivation_review"]["status"], "pending")
        self.assertIsNone(pending["derivation_review"]["reviewed_at"])
        self.assertTrue(pending["derivation_rationale"])

    def test_dispatch_and_token_budget_remove_unsupported_host_policy(self):
        dispatch = self.read(".claude/skills/admin/references/dispatch-protocol.md")
        budget = self.read(".claude/skills/token-budget/SKILL.md")
        for text in (dispatch, budget):
            for forbidden in ("≈10x", "200k", "Haiku", "Sonnet", "Opus", "3–5", "4–5"):
                self.assertNotIn(forbidden, text)
            self.assertIn("sequential", text)
            self.assertIn("aggregate budget", text)
        for term in ("claim_id", "source_id", "origin_id", "locator", "passage", "review", "remaining"):
            self.assertContains(dispatch, term)

    def test_shared_guards_distinguish_citation_and_completion_checks(self):
        guard = self.read(".claude/skills/hallucination-guard/SKILL.md")
        evaluator = self.read(".claude/skills/self-evaluator/SKILL.md")
        for text in (guard, evaluator):
            for term in ("citation correctness", "citation completeness", "semantic", "NEI",
                         "USER_REPORTED", "OBSERVED_VERIFIED", "product", "unverified"):
                self.assertContains(text, term)

    def test_research_admin_uses_shared_caps_and_evidence_manifest(self):
        text = self.read(".claude/skills/research-admin/SKILL.md")
        for term in ("aggregate budget", "min(host capacity, 3)", "sequential", "claim_id", "source_id",
                     "origin_id", "locator", "passage", "review", "entail"):
            self.assertContains(text, term)
        self.assertNotIn("4–5", text)


if __name__ == "__main__":
    unittest.main()
