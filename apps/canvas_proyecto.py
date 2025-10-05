# apps/canvas_proyecto.py
import streamlit as st
from datetime import datetime

def main(st=st):
    st.set_page_config(page_title="Canvas Proyecto Final", page_icon="🧩", layout="wide")
    st.title("Canvas del proyecto final — 1-pager")

    col1, col2 = st.columns(2)
    with col1:
        titulo = st.text_input("Título del proyecto", "Trazabilidad alimentaria con blockchain")
        problema = st.text_area("Problema / oportunidad", "Fraude en la cadena de suministro...")
        stakeholders = st.text_area("Stakeholders", "Productores, distribuidores, retailers, regulador, consumidores")
        arquitectura = st.text_area("Arquitectura técnica (resumen)", "Red permissioned (Quorum), contratos de registro, oráculos de temperatura...")
    with col2:
        normativa = st.text_area("Normativa y cumplimiento", "MiCA (si token), RGPD, DORA, sector alimentario…")
        riesgos = st.text_area("Riesgos y mitigaciones", "Pérdida de claves (multisig), oráculos manipulados (redundancia), privacidad (off-chain + hash)...")
        kpis = st.text_area("KPIs de éxito", "Tiempo de trazado < 3s, reducción fraude 30%, cumplimiento auditorías…")
        plan = st.text_area("Plan y entregables", "MVP en 8 semanas, pruebas piloto, informe jurídico, demo Streamlit.")

    md = f"""# Canvas Proyecto
- Fecha: {datetime.utcnow().isoformat()}Z

## Título
{titulo}

## Problema / oportunidad
{problema}

## Stakeholders
{stakeholders}

## Arquitectura técnica (resumen)
{arquitectura}

## Normativa y cumplimiento
{normativa}

## Riesgos y mitigaciones
{riesgos}

## KPIs de éxito
{kpis}

## Plan y entregables
{plan}
"""
    st.divider()
    st.subheader("Vista previa (Markdown)")
    st.markdown(md)
    st.download_button("Descargar 1-pager (.md)", md.encode("utf-8"), "s27_canvas_proyecto.md")

if __name__ == "__main__":
    main()
