from __future__ import annotations

import json

from src.pipeline import EchocardiogramReportAssistantPipeline


def main() -> None:
    pipeline = EchocardiogramReportAssistantPipeline()
    result = pipeline.run(
        indication="Heart failure evaluation",
        lvef_percent=32,
        lv_size="moderately_dilated",
        rv_function="mildly_reduced",
        diastolic_function="grade_2",
        mitral_regurgitation="moderate",
        aortic_stenosis="none_trace",
        pericardial_effusion="none",
        extra_notes="No major regional wall motion comment provided in this MVP.",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
