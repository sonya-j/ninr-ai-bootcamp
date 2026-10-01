import hashlib
import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class PortfolioArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads((ROOT / "config" / "portfolio.json").read_text(encoding="utf-8"))
        cls.catalog = pd.read_csv(ROOT / "metadata" / "portfolio" / "catalog.csv")

    def test_exactly_twenty_unique_datasets(self):
        self.assertEqual(len(self.config["datasets"]), 20)
        self.assertEqual(len({item["slug"] for item in self.config["datasets"]}), 20)
        source_ids = {
            item.get("source_id", item.get("uci_id"))
            for item in self.config["datasets"]
        }
        self.assertEqual(len(source_ids), 20)

    def test_catalog_matches_manifest_and_all_validations_pass(self):
        expected = {item["slug"] for item in self.config["datasets"]}
        self.assertEqual(set(self.catalog["slug"]), expected)
        self.assertTrue(self.catalog["validation_passed"].all())

    def test_each_dataset_has_questions_and_complete_artifacts(self):
        for spec in self.config["datasets"]:
            with self.subTest(dataset=spec["slug"]):
                self.assertGreaterEqual(len(spec["questions"]), 3)
                participant_path = ROOT / "data" / "processed" / "portfolio" / spec["slug"] / "participant.csv"
                metadata_dir = ROOT / "metadata" / "portfolio" / spec["slug"]
                participant = pd.read_csv(participant_path, keep_default_na=False)
                dictionary = pd.read_csv(metadata_dir / "data_dictionary.csv", keep_default_na=False)
                provenance = json.loads((metadata_dir / "provenance.json").read_text(encoding="utf-8"))
                report = json.loads((metadata_dir / "validation_report.json").read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(participant), 700)
                self.assertLessEqual(len(participant), 10000)
                self.assertGreaterEqual(len(participant.columns), 10)
                self.assertLessEqual(len(participant.columns), 31)
                self.assertTrue(set(participant.columns).issubset(set(dictionary["variable"])))
                self.assertEqual(sha256(participant_path), provenance["participant_sha256"])
                self.assertTrue(report["passed"])
                for filename in ["missing_values.csv", "risk_flags.csv", "value_labels.csv"]:
                    self.assertTrue((metadata_dir / filename).exists())

    def test_catalog_page_lists_every_dataset(self):
        page = (ROOT / "docs" / "dataset_catalog.md").read_text(encoding="utf-8")
        for title in self.catalog["title"]:
            self.assertIn(title, page)


if __name__ == "__main__":
    unittest.main()
