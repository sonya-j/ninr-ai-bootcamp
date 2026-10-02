import hashlib
import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "multimodal_symptom_trajectories" / "participant_day.csv"
METADATA_DIR = ROOT / "metadata" / "multimodal_symptom_trajectories"
NOTEBOOK_PATH = ROOT / "notebooks" / "02_multimodal_symptom_trajectories.ipynb"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class MultimodalActivityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(DATA_PATH)
        cls.dictionary = pd.read_csv(METADATA_DIR / "data_dictionary.csv")
        cls.provenance = json.loads((METADATA_DIR / "provenance.json").read_text(encoding="utf-8"))

    def test_shape_and_unique_participant_days(self):
        self.assertEqual(self.data.shape, (8160, 22))
        self.assertEqual(self.data["participant_id"].nunique(), 240)
        self.assertFalse(self.data.duplicated(["participant_id", "day_index"]).any())

    def test_all_modalities_and_outcome_are_documented(self):
        expected = {"patient-reported", "wearable", "EHR", "context", "outcome"}
        self.assertTrue(expected.issubset(set(self.dictionary["modality"])))
        self.assertEqual(set(self.data.columns), set(self.dictionary["variable"]))
        self.assertFalse(self.data["symptom_score_tomorrow"].isna().any())

    def test_next_day_outcome_is_shifted_within_participant(self):
        ordered = self.data.sort_values(["participant_id", "day_index"])
        next_observed = ordered.groupby("participant_id")["symptom_score_today"].shift(-1)
        comparable = next_observed.notna()
        self.assertTrue(
            (ordered.loc[comparable, "symptom_score_tomorrow"].to_numpy() == next_observed[comparable].to_numpy()).all()
        )

    def test_provenance_and_validation(self):
        self.assertEqual(sha256(DATA_PATH), self.provenance["participant_file_sha256"])
        report = json.loads((METADATA_DIR / "validation_report.json").read_text(encoding="utf-8"))
        self.assertTrue(report["passed"])
        self.assertIn("Synthetic teaching data", self.provenance["status"])

    def test_notebook_is_valid_and_output_free(self):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        self.assertGreaterEqual(len(notebook["cells"]), 20)
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                self.assertEqual(cell.get("outputs", []), [])
                self.assertIsNone(cell.get("execution_count"))


if __name__ == "__main__":
    unittest.main()
