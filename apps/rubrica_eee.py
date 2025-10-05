# apps/rubrica_eee.py
import streamlit as st
import pandas as pd
from datetime import datetime

CAMPOS = ["Ético (E)", "Epistémico (E)", "Económico (E)", "Claridad expositiva", "Viabilidad técnica", "Solidez jurídica"]

def main(st=st):
    st.set_page_config(page_title="Rúbrica EEE (peer review)", page_icon="🧮", layout="wide")
    st.title("Rúbrica EEE — Revisión entre pares")

    grupo_eval = st.text_input("Tu grupo (quién evalúa)", "Grupo Alfa")
    grupo_obj = st.text_input("Grupo evaluado (quién recibe)", "Grupo Beta")

    st.subheader("Puntuación (0–10)")
    scores = {}
    cols = st.columns(3)
    for i, campo in enumerate(CAMPOS):
        with cols[i%3]:
            scores[campo] = st.slider(campo, 0, 10, 7)

    comentarios = st.text_area("Comentarios cualitativos", "Fortalezas, áreas de mejora, riesgos no cubiertos…")

    if "reviews" not in st.session_state:
        st.session_state["reviews"] = []

    if st.button("Añadir evaluación"):
        st.session_state["reviews"].append({
            "evalua": grupo_eval, "evaluado": grupo_obj, **scores, "comentarios": comentarios
        })

    st.subheader("Evaluaciones registradas")
    if st.session_state["reviews"]:
        df = pd.DataFrame(st.session_state["reviews"])
        st.dataframe(df, use_container_width=True)

        # Consolidado por grupo evaluado
        agg = df.groupby("evaluado")[CAMPOS].mean().round(2)
        agg["Score EEE (promedio)"] = agg[["Ético (E)", "Epistémico (E)", "Económico (E)"]].mean(axis=1).round(2)
        st.subheader("Consolidado por grupo evaluado")
        st.dataframe(agg, use_container_width=True)

        md = f"""# S28 · Rúbrica EEE (peer review)
- Fecha: {datetime.utcnow().isoformat()}Z
## Evaluaciones
{df.to_markdown(index=False)}

## Consolidado
{agg.to_markdown()}
"""
        st.download_button("Descargar informe (.md)", md.encode("utf-8"), "s28_rubrica_eee.md")
    else:
        st.info("Aún no hay evaluaciones. Completa puntuaciones y pulsa **Añadir evaluación**.")

if __name__ == "__main__":
    main()
