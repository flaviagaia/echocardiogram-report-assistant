from __future__ import annotations

from pathlib import Path

from .clinical_logic import (
    DiastolicValue,
    EffusionValue,
    LVSizeValue,
    RVFunctionValue,
    ValveSeverityValue,
    classify_lvef,
    summarize_diastolic_function,
    summarize_effusion,
    summarize_lv_function,
    summarize_valve,
    validate_value,
)
from .data_factory import build_case_corpus, build_knowledge_base, write_public_dataset_reference
from .generation import generate_report
from .retrieval import EchoRetriever


ALLOWED_LV_SIZE = {"normal", "mildly_dilated", "moderately_dilated", "severely_dilated"}
ALLOWED_RV_FUNCTION = {"normal", "mildly_reduced", "moderately_reduced", "severely_reduced"}
ALLOWED_DIASTOLIC = {"normal", "grade_1", "grade_2", "grade_3"}
ALLOWED_VALVE = {"none_trace", "mild", "moderate", "severe"}
ALLOWED_EFFUSION = {"none", "small", "moderate", "large"}

ROMAN_DIASTOLIC = {
    "grade_1": "Grade I diastolic dysfunction.",
    "grade_2": "Grade II diastolic dysfunction.",
    "grade_3": "Grade III diastolic dysfunction.",
}


class EchocardiogramReportAssistantPipeline:
    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parents[1])
        self.case_corpus = build_case_corpus()
        self.knowledge_base = build_knowledge_base()
        self.retriever = EchoRetriever(self.case_corpus, self.knowledge_base)
        self.dataset_reference_path = write_public_dataset_reference(self.project_root / "data" / "raw")

    def run(
        self,
        indication: str,
        lvef_percent: int,
        lv_size: LVSizeValue,
        rv_function: RVFunctionValue,
        diastolic_function: DiastolicValue,
        mitral_regurgitation: ValveSeverityValue,
        aortic_stenosis: ValveSeverityValue,
        pericardial_effusion: EffusionValue,
        extra_notes: str = "",
        top_k: int = 5,
    ) -> dict:
        validate_value("lv_size", lv_size, ALLOWED_LV_SIZE)
        validate_value("rv_function", rv_function, ALLOWED_RV_FUNCTION)
        validate_value("diastolic_function", diastolic_function, ALLOWED_DIASTOLIC)
        validate_value("mitral_regurgitation", mitral_regurgitation, ALLOWED_VALVE)
        validate_value("aortic_stenosis", aortic_stenosis, ALLOWED_VALVE)
        validate_value("pericardial_effusion", pericardial_effusion, ALLOWED_EFFUSION)
        if not 5 <= lvef_percent <= 90:
            raise ValueError("Invalid value for lvef_percent: expected a value between 5 and 90.")

        lvef_class = classify_lvef(lvef_percent)
        summary_lines = [
            summarize_lv_function(lvef_percent),
            f"Left ventricular size is {lv_size.replace('_', ' ')}.",
            f"Right ventricular systolic function is {rv_function.replace('_', ' ')}.",
            summarize_diastolic_function(diastolic_function),
            summarize_valve("mitral regurgitation", mitral_regurgitation),
            summarize_valve("aortic stenosis", aortic_stenosis),
            summarize_effusion(pericardial_effusion),
        ]
        if extra_notes:
            summary_lines.append(f"Additional note: {extra_notes}")

        impression_lines = [
            f"LVEF is {lvef_percent}% with {lvef_class.replace('_', ' ')} left ventricular systolic function.",
        ]
        if mitral_regurgitation != "none_trace":
            impression_lines.append(f"{mitral_regurgitation.replace('_', ' ').capitalize()} mitral regurgitation.")
        if aortic_stenosis != "none_trace":
            impression_lines.append(f"{aortic_stenosis.replace('_', ' ').capitalize()} aortic stenosis.")
        if pericardial_effusion != "none":
            impression_lines.append(f"{pericardial_effusion.capitalize()} pericardial effusion.")
        if diastolic_function != "normal":
            impression_lines.append(ROMAN_DIASTOLIC[diastolic_function])

        question = (
            f"Draft an echocardiogram report for EF {lvef_percent}% with {lv_size}, {rv_function} RV function, "
            f"{diastolic_function}, mitral regurgitation {mitral_regurgitation}, aortic stenosis {aortic_stenosis}, "
            f"and pericardial effusion {pericardial_effusion}."
        )
        structured_terms = [
            indication,
            str(lvef_percent),
            lvef_class,
            lv_size,
            rv_function,
            diastolic_function,
            mitral_regurgitation,
            aortic_stenosis,
            pericardial_effusion,
            extra_notes,
        ]
        retrieved = self.retriever.search(question=question, structured_terms=structured_terms, top_k=top_k)
        generated = generate_report(
            question=question,
            retrieved_items=retrieved,
            structured_summary={
                "lvef_percent": lvef_percent,
                "lvef_class": lvef_class,
                "lv_size": lv_size,
                "rv_function": rv_function,
                "diastolic_function": diastolic_function,
                "mitral_regurgitation": mitral_regurgitation,
                "aortic_stenosis": aortic_stenosis,
                "pericardial_effusion": pericardial_effusion,
            },
            summary_lines=summary_lines,
            impression_lines=impression_lines,
        )
        return {
            "dataset_source": "echonet_dynamic_style_local_sample",
            "public_dataset_reference": str(self.dataset_reference_path),
            "case_count": len(self.case_corpus),
            "knowledge_doc_count": len(self.knowledge_base),
            "lvef_class": lvef_class,
            "retrieved_count": len(retrieved),
            **generated,
        }
