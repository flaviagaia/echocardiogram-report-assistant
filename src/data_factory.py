from __future__ import annotations

from pathlib import Path
import json


def build_case_corpus() -> list[dict]:
    return [
        {
            "study_id": "ECHO-1001",
            "indication": "Heart failure evaluation.",
            "lvef_percent": 30,
            "lv_size": "moderately_dilated",
            "rv_function": "mildly_reduced",
            "diastolic_function": "grade_2",
            "mitral_regurgitation": "moderate",
            "aortic_stenosis": "none_trace",
            "pericardial_effusion": "none",
            "findings": (
                "Left ventricle is moderately dilated with moderately reduced systolic function; estimated ejection fraction is 30%. "
                "Grade II diastolic dysfunction is present. Right ventricular systolic function is mildly reduced. "
                "Moderate mitral regurgitation. No significant aortic stenosis. No pericardial effusion."
            ),
            "impression": "Dilated cardiomyopathy pattern with moderately reduced LVEF and moderate mitral regurgitation.",
        },
        {
            "study_id": "ECHO-1002",
            "indication": "Cardiomyopathy follow-up.",
            "lvef_percent": 20,
            "lv_size": "severely_dilated",
            "rv_function": "moderately_reduced",
            "diastolic_function": "grade_3",
            "mitral_regurgitation": "mild",
            "aortic_stenosis": "none_trace",
            "pericardial_effusion": "small",
            "findings": (
                "Severely dilated left ventricle with severely reduced systolic function; estimated ejection fraction is 20%. "
                "Grade III diastolic dysfunction. Right ventricular systolic function is moderately reduced. "
                "Mild mitral regurgitation. Small pericardial effusion."
            ),
            "impression": "Severe biventricular dysfunction with advanced LV systolic impairment and small pericardial effusion.",
        },
        {
            "study_id": "ECHO-1003",
            "indication": "Murmur evaluation.",
            "lvef_percent": 60,
            "lv_size": "normal",
            "rv_function": "normal",
            "diastolic_function": "normal",
            "mitral_regurgitation": "mild",
            "aortic_stenosis": "moderate",
            "pericardial_effusion": "none",
            "findings": (
                "Left ventricular size and systolic function are normal with estimated ejection fraction of 60%. "
                "Right ventricular systolic function is normal. Mild mitral regurgitation. Moderate aortic stenosis. "
                "No pericardial effusion."
            ),
            "impression": "Preserved biventricular systolic function with moderate aortic stenosis.",
        },
        {
            "study_id": "ECHO-1004",
            "indication": "Hypertension.",
            "lvef_percent": 55,
            "lv_size": "normal",
            "rv_function": "normal",
            "diastolic_function": "grade_1",
            "mitral_regurgitation": "none_trace",
            "aortic_stenosis": "none_trace",
            "pericardial_effusion": "none",
            "findings": (
                "Left ventricular size is normal with preserved systolic function and estimated ejection fraction of 55%. "
                "Grade I diastolic dysfunction. Right ventricular systolic function is normal. "
                "No significant valvular disease. No pericardial effusion."
            ),
            "impression": "Preserved left ventricular systolic function with grade I diastolic dysfunction.",
        },
        {
            "study_id": "ECHO-1005",
            "indication": "Pericardial disease assessment.",
            "lvef_percent": 50,
            "lv_size": "normal",
            "rv_function": "normal",
            "diastolic_function": "normal",
            "mitral_regurgitation": "none_trace",
            "aortic_stenosis": "none_trace",
            "pericardial_effusion": "moderate",
            "findings": (
                "Preserved left ventricular systolic function with estimated ejection fraction of 50%. "
                "No significant valvular disease. Moderate pericardial effusion."
            ),
            "impression": "Moderate pericardial effusion with otherwise preserved ventricular function.",
        },
        {
            "study_id": "ECHO-1006",
            "indication": "Valvular follow-up.",
            "lvef_percent": 58,
            "lv_size": "normal",
            "rv_function": "normal",
            "diastolic_function": "normal",
            "mitral_regurgitation": "severe",
            "aortic_stenosis": "none_trace",
            "pericardial_effusion": "none",
            "findings": (
                "Left ventricular size is normal with preserved systolic function and estimated ejection fraction of 58%. "
                "Severe mitral regurgitation is present. Right ventricular systolic function is normal. No pericardial effusion."
            ),
            "impression": "Severe mitral regurgitation with preserved left ventricular systolic function.",
        },
        {
            "study_id": "ECHO-1007",
            "indication": "Pulmonary hypertension work-up.",
            "lvef_percent": 48,
            "lv_size": "normal",
            "rv_function": "moderately_reduced",
            "diastolic_function": "grade_1",
            "mitral_regurgitation": "mild",
            "aortic_stenosis": "none_trace",
            "pericardial_effusion": "none",
            "findings": (
                "Left ventricular systolic function is mildly reduced with estimated ejection fraction of 48%. "
                "Right ventricular systolic function is moderately reduced. Mild mitral regurgitation. No pericardial effusion."
            ),
            "impression": "Mild left ventricular systolic dysfunction with moderate right ventricular dysfunction.",
        },
        {
            "study_id": "ECHO-1008",
            "indication": "Aortic stenosis surveillance.",
            "lvef_percent": 57,
            "lv_size": "normal",
            "rv_function": "normal",
            "diastolic_function": "grade_1",
            "mitral_regurgitation": "mild",
            "aortic_stenosis": "severe",
            "pericardial_effusion": "none",
            "findings": (
                "Left ventricular systolic function is preserved with estimated ejection fraction of 57%. "
                "Mild mitral regurgitation. Severe aortic stenosis. No pericardial effusion."
            ),
            "impression": "Severe aortic stenosis with preserved left ventricular systolic function.",
        },
    ]


def build_knowledge_base() -> list[dict]:
    return [
        {
            "doc_id": "KB-ECHO-1001",
            "title": "LV systolic function wording",
            "category": "template",
            "content": (
                "Echocardiogram impressions should clearly state whether left ventricular systolic function is normal, mildly reduced, moderately reduced, or severely reduced, and mention the estimated ejection fraction."
            ),
        },
        {
            "doc_id": "KB-ECHO-1002",
            "title": "Diastolic function reporting",
            "category": "guideline",
            "content": (
                "Diastolic function should be described as normal or with the reported grade when sufficient data are available, especially in routine transthoracic studies."
            ),
        },
        {
            "doc_id": "KB-ECHO-1003",
            "title": "Valve severity reporting",
            "category": "template",
            "content": (
                "Valvular findings should separate regurgitant and stenotic lesions and state the severity using standard categories such as mild, moderate, or severe."
            ),
        },
        {
            "doc_id": "KB-ECHO-1004",
            "title": "Pericardial effusion wording",
            "category": "template",
            "content": (
                "Pericardial effusion should be described by magnitude and, in a more advanced version, the report could note tamponade physiology if present."
            ),
        },
    ]


def write_public_dataset_reference(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "recommended_public_dataset": {
            "name": "EchoNet-Dynamic",
            "why_it_was_chosen": [
                "largest widely used public echocardiography video dataset",
                "contains apical four-chamber videos with expert measurements including LVEF and LV volumes",
                "strong fit for future multimodal retrieval and visual estimation of LV systolic function",
            ],
            "references": [
                {
                    "label": "EchoNet-Dynamic official dataset",
                    "url": "https://echonet.github.io/dynamic/",
                },
                {
                    "label": "ASE chamber quantification guideline",
                    "url": "https://www.asecho.org/guideline/cardiac-chamber-quantification-by-echo-in-adults/",
                },
            ],
        },
        "upgrade_path": {
            "datasets": [
                {
                    "name": "CAMUS",
                    "note": "good next step for segmentation-oriented echo pipelines",
                }
            ]
        },
        "runtime_note": "This repository uses a local structured echocardiogram sample corpus inspired by public echo datasets and ASE-style reporting so the stack remains fully reproducible.",
    }
    path = output_dir / "public_dataset_reference.json"
    serialized = json.dumps(payload, indent=2)
    if not path.exists() or path.read_text(encoding="utf-8") != serialized:
        path.write_text(serialized, encoding="utf-8")
    return path
