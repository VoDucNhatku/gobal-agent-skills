"""Executable structural ledger tests; no semantic/model behavior assertions."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.validate_evidence import validate_ledger


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_evidence.py"
EXAMPLE = ROOT / ".claude" / "skills" / "admin" / "resources" / "claim-ledger.example.yml"
DATE = "2026-10-03T05:58:35Z"


def review(status="accepted"):
    return {"method": "Passage comparison", "reviewer": "test reviewer",
            "status": status, "reviewed_at": DATE if status == "accepted" else None}


def edge(source_id="S1", stance="support", status="accepted"):
    return {"source_id": source_id, "locator": "Section one",
            "passage": "This is an inspected passage in the fixture.",
            "stance": stance, "review": review(status)}


def claim(claim_id="C1", status="SUPPORTED", evidence=None):
    return {"claim_id": claim_id, "text_atomic": "Atomic fixture claim.",
            "status": status, "risk": "low",
            "evidence": [edge()] if evidence is None else evidence,
            "derived_from_claim_ids": [], "fatal_flags": [],
            "corroboration_required": False, "conflicts": []}


def source(source_id="S1", origin_id="origin-one"):
    return {"source_id": source_id, "canonical_url": "https://example.org/document",
            "title": "Fixture source", "origin_id": origin_id,
            "source_type": "official_docs", "accessed_at": DATE}


def ledger():
    return {"schema_version": 1, "sources": [source()], "claims": [claim()],
            "output": [{"statement_id": "O1", "claim_ids": ["C1"],
                        "cited_source_ids": ["S1"]}]}


class EvidenceValidatorTests(unittest.TestCase):
    def assertInvalid(self, data, code):
        report = validate_ledger(data)
        self.assertFalse(report["valid"], report)
        self.assertFalse(report["semantic_verified"])
        self.assertIn(code, {error["code"] for error in report["errors"]}, report)

    def run_cli(self, text, *args):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.yml"
            path.write_text(text, encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), str(path), *args],
                                  cwd=ROOT, text=True, encoding="utf-8", capture_output=True)

    def test_supported_passes_structurally_without_semantic_verification(self):
        report = validate_ledger(ledger())
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["errors"], [])
        self.assertIs(report["semantic_verified"], False)
        self.assertIn("semantic", report["disclaimer"].lower())

    def test_nei_needs_no_fabricated_support(self):
        data = ledger()
        data["sources"] = []
        data["claims"] = [claim(status="NEI", evidence=[])]
        data["output"][0]["cited_source_ids"] = []
        self.assertTrue(validate_ledger(data)["valid"])

    def test_empty_all_ledger_is_not_a_vacuous_pass(self):
        self.assertInvalid({"schema_version": 1, "sources": [], "claims": [], "output": []}, "empty_ledger")

    def test_missing_support_rejected(self):
        data = ledger()
        data["claims"][0]["evidence"] = []
        self.assertInvalid(data, "unsupported_status")

    def test_missing_source_reference_rejected(self):
        data = ledger()
        data["claims"][0]["evidence"][0]["source_id"] = "missing"
        self.assertInvalid(data, "unknown_source")

    def test_local_file_absolute_identities_pass_syntax_only(self):
        for identity in ("/research/paper.pdf", r"C:\research\paper.pdf",
                         r"\\server\share\paper.pdf", "file:///C:/research/paper.pdf"):
            with self.subTest(identity=identity):
                data = ledger()
                data["sources"][0].update(source_type="local_file", canonical_url=identity)
                self.assertTrue(validate_ledger(data)["valid"])

    def test_relative_or_wrong_type_local_identity_rejected(self):
        for identity, source_type in (("paper.pdf", "local_file"),
                                      ("file:paper.pdf", "local_file"),
                                      (r"C:paper.pdf", "local_file"),
                                      (r"C:\paper.pdf", "official_docs")):
            with self.subTest(identity=identity, source_type=source_type):
                data = ledger()
                data["sources"][0].update(source_type=source_type, canonical_url=identity)
                self.assertInvalid(data, "invalid_source_identity")

    def test_cli_valid_json_report(self):
        result = self.run_cli(yaml.safe_dump(ledger()), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertFalse(report["semantic_verified"])

    def test_cli_rejects_duplicate_yaml_keys(self):
        result = self.run_cli("schema_version: 1\nschema_version: 1\n", "--json")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertFalse(report["valid"])
        self.assertIn("duplicate YAML key", str(report["errors"]))

    def test_cli_rejects_malformed_yaml(self):
        result = self.run_cli("claims: [\n", "--json")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)["valid"])

    def test_status_and_stance_enums_are_typechecked(self):
        for field, value, code in (("status", "verified", "invalid_status"),
                                   ("status", [], "invalid_status")):
            with self.subTest(field=field, value=value):
                data = ledger()
                data["claims"][0][field] = value
                self.assertInvalid(data, code)
        data = ledger()
        data["claims"][0]["evidence"][0]["stance"] = "neutral"
        self.assertInvalid(data, "invalid_stance")

    def test_sources_claims_and_output_are_typechecked(self):
        self.assertInvalid([], "invalid_type")
        for key in ("sources", "claims", "output"):
            for value in (None, {}, "wrong", [None], [[]]):
                with self.subTest(key=key, value=value):
                    data = ledger()
                    data[key] = value
                    self.assertInvalid(data, "invalid_type")
        for key, value in (("evidence", {}), ("fatal_flags", "bad"),
                           ("derived_from_claim_ids", [None]), ("corroboration_required", 1),
                           ("conflicts", "bad")):
            data = ledger()
            data["claims"][0][key] = value
            self.assertInvalid(data, "invalid_type")

    def test_schema_version_requires_exact_integer_one(self):
        for value in (True, "1", 2, None):
            data = ledger()
            data["schema_version"] = value
            self.assertInvalid(data, "invalid_schema_version")

    def test_source_url_and_date_syntax_not_network_truth(self):
        for value in ("ftp://example.org/a", "https:///path", "https://example.org:99999/a",
                      "https://example.org/a b", "javascript:alert(1)"):
            data = ledger()
            data["sources"][0]["canonical_url"] = value
            self.assertInvalid(data, "invalid_source_identity")
        data = ledger()
        data["sources"][0]["accessed_at"] = "not-a-date"
        self.assertInvalid(data, "invalid_date")
        data = ledger()
        data["sources"][0]["canonical_url"] = "https://this-domain-need-not-exist.invalid/a"
        self.assertTrue(validate_ledger(data)["valid"])

    def test_unique_source_claim_and_statement_ids(self):
        for key in ("sources", "claims", "output"):
            data = ledger()
            data[key].append(copy.deepcopy(data[key][0]))
            self.assertInvalid(data, "duplicate_id")

    def test_edge_passage_locator_and_review_fields_required(self):
        for field in ("passage", "locator", "review"):
            data = ledger()
            del data["claims"][0]["evidence"][0][field]
            self.assertInvalid(data, "missing_field")
        for field in ("method", "reviewer", "status", "reviewed_at"):
            data = ledger()
            del data["claims"][0]["evidence"][0]["review"][field]
            self.assertInvalid(data, "missing_field")
        data = ledger()
        data["claims"][0]["evidence"][0]["review"]["reviewed_at"] = None
        self.assertInvalid(data, "invalid_date")

    def test_pending_review_does_not_count_as_support(self):
        data = ledger()
        data["claims"][0]["evidence"] = [edge(status="pending")]
        self.assertInvalid(data, "unsupported_status")
        data["claims"][0]["status"] = "NEI"
        self.assertTrue(validate_ledger(data)["valid"])

    def test_fatal_flags_block_supported(self):
        data = ledger()
        data["claims"][0]["fatal_flags"] = ["wrong_scope"]
        self.assertInvalid(data, "fatal_supported")

    def test_refuted_requires_accepted_contradiction(self):
        data = ledger()
        data["claims"][0] = claim(status="REFUTED", evidence=[edge(stance="contradict")])
        self.assertTrue(validate_ledger(data)["valid"])
        data["claims"][0]["evidence"][0]["review"] = review("pending")
        self.assertInvalid(data, "unsupported_status")

    def contested(self):
        data = ledger()
        data["sources"].append(source("S2", "origin-two"))
        data["claims"][0] = claim(status="CONTESTED", evidence=[edge(), edge("S2", "contradict")])
        data["claims"][0]["conflicts"] = ["Accepted sources disagree on the claim."]
        data["output"][0]["cited_source_ids"] = ["S1", "S2"]
        return data

    def test_contested_requires_both_accepted_stances_and_preserved_conflict(self):
        data = self.contested()
        self.assertTrue(validate_ledger(data)["valid"])
        data["claims"][0]["evidence"].pop()
        self.assertInvalid(data, "unsupported_status")
        data = self.contested()
        data["claims"][0]["conflicts"] = []
        self.assertInvalid(data, "missing_conflict")

    def test_accepted_opposition_cannot_be_silently_ignored(self):
        for status in ("SUPPORTED", "REFUTED", "NEI"):
            data = self.contested()
            data["claims"][0]["status"] = status
            self.assertInvalid(data, "status_conflict")

    def test_unresolved_or_malformed_conflict_blocks_supported(self):
        data = ledger()
        data["claims"][0]["conflicts"] = ["A relevant disagreement is unresolved."]
        self.assertInvalid(data, "unresolved_conflict")
        for value in ([], None, 42, {}):
            data["claims"][0]["conflicts"] = [value]
            self.assertInvalid(data, "invalid_conflict")
        data["claims"][0]["conflicts"] = [{"reason": "Different version", "resolution": "Scope narrowed to the stated version"}]
        self.assertTrue(validate_ledger(data)["valid"])

    def test_corroboration_counts_independent_origins_not_urls(self):
        for status, stance in (("SUPPORTED", "support"), ("REFUTED", "contradict")):
            data = ledger()
            data["sources"].append(source("S2", "origin-one"))
            data["claims"][0] = claim(status=status, evidence=[edge(stance=stance), edge("S2", stance)])
            data["claims"][0]["corroboration_required"] = True
            self.assertInvalid(data, "insufficient_origins")
            data["sources"][1]["origin_id"] = "origin-two"
            self.assertTrue(validate_ledger(data)["valid"])
        data = ledger()
        data["claims"][0] = claim(status="NEI", evidence=[])
        data["claims"][0]["corroboration_required"] = True
        data["output"][0]["cited_source_ids"] = []
        self.assertTrue(validate_ledger(data)["valid"])

    def deduction(self, status="SUPPORTED"):
        data = ledger()
        child = claim("C2", status, [])
        child.update(derived_from_claim_ids=["C1"], derivation_rationale="Fixture logical step.",
                     derivation_review=review("accepted" if status == "SUPPORTED" else "pending"))
        data["claims"].append(child)
        data["output"] = [{"statement_id": "O2", "claim_ids": ["C2"], "cited_source_ids": ["S1"]}]
        return data

    def test_reviewed_deduction_inherits_parent_source_provenance(self):
        self.assertTrue(validate_ledger(self.deduction())["valid"])
        self.assertTrue(validate_ledger(self.deduction("NEI"))["valid"])

    def test_supported_deduction_requires_rationale_and_accepted_logical_review(self):
        for field in ("derivation_rationale", "derivation_review"):
            data = self.deduction()
            del data["claims"][1][field]
            self.assertInvalid(data, "invalid_derivation")
        data = self.deduction()
        data["claims"][1]["derivation_review"] = review("pending")
        self.assertInvalid(data, "unsupported_status")

    def test_dangling_and_unsupported_derivation_parents_rejected(self):
        data = self.deduction()
        data["claims"][1]["derived_from_claim_ids"] = ["missing"]
        self.assertInvalid(data, "unknown_derivation")
        for status in ("NEI", "REFUTED", "CONTESTED"):
            data = self.deduction()
            data["claims"][0]["status"] = status
            self.assertInvalid(data, "unsupported_dependency")

    def test_cycles_and_self_dependency_rejected(self):
        data = self.deduction()
        data["claims"][0]["derived_from_claim_ids"] = ["C2"]
        self.assertInvalid(data, "cyclic_derivation")
        data = ledger()
        data["claims"][0]["derived_from_claim_ids"] = ["C1"]
        self.assertInvalid(data, "self_dependency")

    def test_long_deduction_chain_is_iterative(self):
        data = ledger()
        for index in range(2, 1102):
            child = claim(f"C{index}", evidence=[])
            child.update(derived_from_claim_ids=[f"C{index - 1}"],
                         derivation_rationale="Fixture logical step.", derivation_review=review())
            data["claims"].append(child)
        data["output"][0]["claim_ids"] = ["C1101"]
        self.assertTrue(validate_ledger(data)["valid"])

    def test_output_cannot_cite_missing_or_unrelated_claim_source(self):
        data = ledger()
        data["output"][0]["claim_ids"] = ["missing"]
        self.assertInvalid(data, "unknown_claim")
        data = ledger()
        data["output"][0]["cited_source_ids"] = ["missing"]
        self.assertInvalid(data, "unknown_source")
        data = ledger()
        data["sources"].append(source("S2", "origin-two"))
        data["output"][0]["cited_source_ids"] = ["S2"]
        self.assertInvalid(data, "unrelated_citation")

    def test_output_settled_claims_need_citation_for_each_relevant_stance(self):
        for data in (ledger(), self.deduction(), self.contested()):
            data["output"][0]["cited_source_ids"] = []
            self.assertInvalid(data, "missing_citation")
        data = self.contested()
        data["output"][0]["cited_source_ids"] = ["S1"]
        self.assertInvalid(data, "missing_citation")
        data = ledger()
        data["claims"][0] = claim(status="REFUTED", evidence=[edge(stance="contradict")])
        data["output"][0]["cited_source_ids"] = []
        self.assertInvalid(data, "missing_citation")

    def test_deduction_does_not_depend_on_record_order(self):
        data = self.deduction()
        data["claims"].reverse()
        self.assertTrue(validate_ledger(data)["valid"])

    def test_pending_edge_cannot_supply_required_second_origin(self):
        data = ledger()
        data["sources"].append(source("S2", "origin-two"))
        data["claims"][0]["evidence"].append(edge("S2", status="pending"))
        data["claims"][0]["corroboration_required"] = True
        self.assertInvalid(data, "insufficient_origins")

    def test_irrelevant_passage_with_complete_review_cannot_be_semantically_detected(self):
        data = ledger()
        data["claims"][0]["text_atomic"] = "The sky is green."
        data["claims"][0]["evidence"][0]["passage"] = "This passage describes a cake recipe."
        report = validate_ledger(data)
        self.assertTrue(report["valid"])
        self.assertFalse(report["semantic_verified"])

    def test_cli_missing_file_is_machine_readable_failure(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "not-a-real-ledger.yml"), "--json"],
                                text=True, encoding="utf-8", capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)["valid"])

    def test_cli_rejects_non_string_mapping_key_and_nonzero_invalid_schema(self):
        for text in ("? [complex, key]\n: value\n", "42: value\n", yaml.safe_dump({"schema_version": True})):
            result = self.run_cli(text, "--json")
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(json.loads(result.stdout)["valid"])

    def test_authored_example_passes_with_pending_nei_deduction(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(EXAMPLE), "--json"],
                                text=True, encoding="utf-8", capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(json.loads(result.stdout)["semantic_verified"])


if __name__ == "__main__":
    unittest.main()
