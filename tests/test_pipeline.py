import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class PipelineArtifactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(ROOT / "data" / "processed" / "diabetes_130_hospitals_participant.csv")
        cls.dictionary = pd.read_csv(ROOT / "metadata" / "data_dictionary.csv")

    def test_participant_shape(self):
        self.assertEqual(self.data.shape, (5000, 26))

    def test_binary_outcome_matches_official_target(self):
        expected = (self.data["readmitted"] == "<30").astype(int)
        pd.testing.assert_series_equal(self.data["readmitted_30d"], expected, check_names=False)

    def test_identifiers_are_unique(self):
        self.assertTrue(self.data["encounter_id"].is_unique)

    def test_dictionary_covers_every_column(self):
        self.assertTrue(set(self.data.columns).issubset(set(self.dictionary["variable"])))

    def test_validation_report_passed(self):
        report = json.loads((ROOT / "metadata" / "validation_report.json").read_text(encoding="utf-8"))
        self.assertTrue(report["passed"])


if __name__ == "__main__":
    unittest.main()
