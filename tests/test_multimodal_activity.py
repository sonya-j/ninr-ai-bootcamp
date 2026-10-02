import hashlib
import json
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "multimodal_symptom_trajectories" / "participant_day.csv"
METADATA_DIR = ROOT / "metadata" / "multimodal_symptom_trajectories"
NOTEBOOK_PATH = ROOT / "notebooks" / "02_multimodal_symptom_trajectories.ipynb"
WALKTHROUGH = ROOT / "docs" / "activities" / "multimodal_fatigue_walkthrough.md"
TEACHING_GUIDE = ROOT / "docs" / "teaching_guides" / "multimodal_fatigue_teaching_guide.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class MultimodalActivityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(DATA_PATH, parse_dates=["date"])
        cls.dictionary = pd.read_csv(METADATA_DIR / "data_dictionary.csv")
        cls.provenance = json.loads((METADATA_DIR / "provenance.json").read_text(encoding="utf-8"))

    def test_real_public_dataset_shape_and_unique_days(self):
        self.assertEqual(self.data.shape, (450, 26))
        self.assertEqual(self.data["participant_id"].nunique(), 28)
        self.assertEqual(self.data["fatigue_tomorrow"].notna().sum(), 336)
        self.assertFalse(self.data.duplicated(["participant_id", "date"]).any())

    def test_modalities_are_documented_without_fake_ehr(self):
        expected = {"patient-reported", "wearable", "time context", "outcome"}
        self.assertTrue(expected.issubset(set(self.dictionary["modality"])))
        self.assertNotIn("EHR", set(self.dictionary["modality"]))
        self.assertEqual(set(self.data.columns), set(self.dictionary["variable"]))

    def test_next_day_outcome_is_next_calendar_day(self):
        ordered = self.data.sort_values(["participant_id", "date"]).copy()
        next_fatigue = ordered.groupby("participant_id")["fatigue_today"].shift(-1)
        next_date = ordered.groupby("participant_id")["date"].shift(-1)
        consecutive = (next_date - ordered["date"]).dt.days.eq(1)
        self.assertTrue(ordered.loc[~consecutive, "fatigue_tomorrow"].isna().all())
        self.assertTrue(
            ordered.loc[consecutive, "fatigue_tomorrow"].reset_index(drop=True).equals(
                next_fatigue[consecutive].reset_index(drop=True)
            )
        )

    def test_provenance_and_validation(self):
        self.assertEqual(sha256(DATA_PATH), self.provenance["processed_sha256"])
        self.assertEqual(self.provenance["doi"], "10.5281/zenodo.4266157")
        self.assertEqual(self.provenance["license"], "cc-by-4.0")
        self.assertEqual(self.provenance["access_right"], "open")
        self.assertIn("does not contain EHR", self.provenance["important_scope_note"])
        report = json.loads((METADATA_DIR / "validation_report.json").read_text(encoding="utf-8"))
        self.assertTrue(report["passed"])

    def test_notebook_and_guides_are_present(self):
        notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        self.assertGreaterEqual(len(notebook["cells"]), 20)
        self.assertTrue(WALKTHROUGH.exists())
        self.assertTrue(TEACHING_GUIDE.exists())
        for cell in notebook["cells"]:
            self.assertTrue(cell.get("id"))
            if cell["cell_type"] == "code":
                self.assertEqual(cell.get("outputs", []), [])
                self.assertIsNone(cell.get("execution_count"))


if __name__ == "__main__":
    unittest.main()
