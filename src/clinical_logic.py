from __future__ import annotations

from typing import Literal


LVSizeValue = Literal["normal", "mildly_dilated", "moderately_dilated", "severely_dilated"]
RVFunctionValue = Literal["normal", "mildly_reduced", "moderately_reduced", "severely_reduced"]
DiastolicValue = Literal["normal", "grade_1", "grade_2", "grade_3"]
ValveSeverityValue = Literal["none_trace", "mild", "moderate", "severe"]
EffusionValue = Literal["none", "small", "moderate", "large"]


def validate_value(name: str, value: str, allowed_values: set[str]) -> None:
    if value not in allowed_values:
        allowed_list = ", ".join(sorted(allowed_values))
        raise ValueError(f"Invalid value for {name}: {value}. Allowed values: {allowed_list}.")


def classify_lvef(lvef_percent: int) -> str:
    if lvef_percent >= 52:
        return "normal"
    if lvef_percent >= 41:
        return "mildly_reduced"
    if lvef_percent >= 30:
        return "moderately_reduced"
    return "severely_reduced"


def summarize_lv_function(lvef_percent: int) -> str:
    category = classify_lvef(lvef_percent)
    mapping = {
        "normal": f"Left ventricular systolic function is normal with estimated ejection fraction of {lvef_percent}%.",
        "mildly_reduced": f"Left ventricular systolic function is mildly reduced with estimated ejection fraction of {lvef_percent}%.",
        "moderately_reduced": f"Left ventricular systolic function is moderately reduced with estimated ejection fraction of {lvef_percent}%.",
        "severely_reduced": f"Left ventricular systolic function is severely reduced with estimated ejection fraction of {lvef_percent}%.",
    }
    return mapping[category]


def summarize_diastolic_function(diastolic_function: DiastolicValue) -> str:
    mapping = {
        "normal": "Diastolic function appears normal.",
        "grade_1": "Findings are consistent with grade I diastolic dysfunction.",
        "grade_2": "Findings are consistent with grade II diastolic dysfunction.",
        "grade_3": "Findings are consistent with grade III diastolic dysfunction.",
    }
    return mapping[diastolic_function]


def summarize_valve(name: str, severity: ValveSeverityValue) -> str:
    if severity == "none_trace":
        return f"No hemodynamically significant {name.lower()}."
    return f"{severity.replace('_', ' ').capitalize()} {name.lower()} is present."


def summarize_effusion(effusion: EffusionValue) -> str:
    if effusion == "none":
        return "No pericardial effusion."
    return f"{effusion.capitalize()} pericardial effusion is present."
