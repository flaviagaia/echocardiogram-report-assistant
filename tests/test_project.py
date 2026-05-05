from __future__ import annotations

import unittest

from src.clinical_logic import classify_lvef
from src.pipeline import EchocardiogramReportAssistantPipeline


class EchocardiogramReportAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pipeline = EchocardiogramReportAssistantPipeline()

    def test_lvef_classification(self) -> None:
        self.assertEqual(classify_lvef(60), "normal")
        self.assertEqual(classify_lvef(45), "mildly_reduced")
        self.assertEqual(classify_lvef(35), "moderately_reduced")
        self.assertEqual(classify_lvef(20), "severely_reduced")

    def test_pipeline_returns_dilated_cardiomyopathy_style_case(self) -> None:
        result = self.pipeline.run(
            indication="Heart failure evaluation",
            lvef_percent=32,
            lv_size="moderately_dilated",
            rv_function="mildly_reduced",
            diastolic_function="grade_2",
            mitral_regurgitation="moderate",
            aortic_stenosis="none_trace",
            pericardial_effusion="none",
        )
        self.assertEqual(result["lvef_class"], "moderately_reduced")
        self.assertIn("ECHO-1001", result["reference_case_ids"])
        self.assertIn("32%", result["draft_report"]["impression"])

    def test_pipeline_rejects_invalid_lvef(self) -> None:
        with self.assertRaises(ValueError):
            self.pipeline.run(
                indication="Heart failure evaluation",
                lvef_percent=2,
                lv_size="moderately_dilated",
                rv_function="mildly_reduced",
                diastolic_function="grade_2",
                mitral_regurgitation="moderate",
                aortic_stenosis="none_trace",
                pericardial_effusion="none",
            )


if __name__ == "__main__":
    unittest.main()
