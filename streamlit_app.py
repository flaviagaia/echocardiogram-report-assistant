from __future__ import annotations

import streamlit as st

from src.pipeline import EchocardiogramReportAssistantPipeline


pipeline = EchocardiogramReportAssistantPipeline()
st.set_page_config(page_title="Assistente de Laudo de Ecocardiograma", layout="wide")

st.title("Assistente de Laudo de Ecocardiograma")
st.write(
    "Este sistema recebe achados estruturados de ecocardiograma, recupera casos semelhantes e gera uma minuta de laudo para revisão médica."
)

with st.form("echo_form"):
    indication = st.text_input("Indicação clínica", value="Avaliação de insuficiência cardíaca")
    lvef_percent = st.number_input("Fração de ejeção (%)", min_value=5, max_value=90, value=32)

    col1, col2, col3 = st.columns(3)
    lv_size = col1.selectbox("Tamanho do VE", ["normal", "mildly_dilated", "moderately_dilated", "severely_dilated"])
    rv_function = col2.selectbox("Função do VD", ["normal", "mildly_reduced", "moderately_reduced", "severely_reduced"])
    diastolic_function = col3.selectbox("Função diastólica", ["normal", "grade_1", "grade_2", "grade_3"])

    col4, col5, col6 = st.columns(3)
    mitral_regurgitation = col4.selectbox("Insuficiência mitral", ["none_trace", "mild", "moderate", "severe"])
    aortic_stenosis = col5.selectbox("Estenose aórtica", ["none_trace", "mild", "moderate", "severe"])
    pericardial_effusion = col6.selectbox("Derrame pericárdico", ["none", "small", "moderate", "large"])

    extra_notes = st.text_area("Observações adicionais", value="Sem detalhe segmentar adicional nesta versão.")
    submitted = st.form_submit_button("Gerar minuta")

if submitted:
    result = pipeline.run(
        indication=indication,
        lvef_percent=int(lvef_percent),
        lv_size=lv_size,
        rv_function=rv_function,
        diastolic_function=diastolic_function,
        mitral_regurgitation=mitral_regurgitation,
        aortic_stenosis=aortic_stenosis,
        pericardial_effusion=pericardial_effusion,
        extra_notes=extra_notes,
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Classe da FEVE", result["lvef_class"].replace("_", " ").capitalize())
    col_b.metric("Confiança RAG", result["confidence"].capitalize())
    col_c.metric("Melhor similaridade", result["best_similarity"])

    st.subheader("Minuta sugerida")
    st.markdown(f"**Technique**: {result['draft_report']['technique']}")
    st.markdown(f"**Findings**: {result['draft_report']['findings']}")
    st.markdown(f"**Impression**: {result['draft_report']['impression']}")

    st.subheader("Apoio à revisão")
    st.write(result["recommendation"])
    st.write(f"Casos de referência: {', '.join(result['reference_case_ids']) or 'n/a'}")

    with st.expander("Evidências recuperadas"):
        for item in result["evidence"]:
            st.write(
                f"- {item['source_type']} | {item['source_id']} | {item['title']} | similarity={item['similarity']}"
            )

    with st.expander("Base pública sugerida"):
        st.code(result["public_dataset_reference"])
