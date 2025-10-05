# apps/auto_radar_ra.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def main(st=st):
    st.set_page_config(page_title="Autoevaluación RA", page_icon="📈", layout="wide")
    st.title("Autoevaluación final — RA1 · RA2 · RA3")

    st.caption("Valora tu dominio (0–10). RA1: fundamentos y uso jurídico; RA2: privacidad/ciberseguridad; RA3: sistemas de información para soluciones legales.")

    col1, col2, col3 = st.columns(3)
    with col1:
        ra1 = st.slider("RA1 — Blockchain para soluciones jurídicas", 0, 10, 8)
    with col2:
        ra2 = st.slider("RA2 — Privacidad y ciberseguridad", 0, 10, 7)
    with col3:
        ra3 = st.slider("RA3 — Sistemas de información/organización", 0, 10, 7)

    df = pd.DataFrame({"RA": ["RA1","RA2","RA3"], "Valor": [ra1, ra2, ra3]})
    fig = px.line_polar(df, r="Valor", theta="RA", line_close=True, range_r=[0,10])
    st.plotly_chart(fig, use_container_width=True)

    media = round((ra1 + ra2 + ra3) / 3, 2)
    st.metric("Media de logro", media)

    st.subheader("Evidencias clave (enlaza mini-apps, informes, commits)")
    evid = st.text_area("URLs/notas de evidencias", "- s14_gas_comparador.md …\n- s18_informe_pericial.md …")

    st.divider()
    st.subheader("Plan de mejora (próximos 90 días)")
    colA, colB = st.columns(2)
    with colA:
        gap = st.multiselect("Identifica tus gaps", ["RGPD profundo", "Auditoría SC", "Oráculos y TWAP", "MiCA/DORA avanzado", "Arquitectura permissioned", "LegalTech/Clause→code"])
    with colB:
        acciones = st.text_area("Acciones concretas", "• Refactorizar contrato con OpenZeppelin + tests\n• Estudiar DPIA y anonimización con casos reales\n• Practicar Hardhat + Etherscan Verify")

    st.divider()
    st.subheader("Reflexión final (6–8 líneas)")
    txt = st.text_area("¿Qué cambió en tu forma de pensar sobre ‘confianza’ y ‘prueba’ en sistemas automatizados?")

    md = f"""# S30 · Autoevaluación RA
- Fecha: {datetime.utcnow().isoformat()}Z
- RA1: {ra1} · RA2: {ra2} · RA3: {ra3} · Media: {media}

## Evidencias
{evid}

## Gaps
- {', '.join(gap) if gap else '(no indicado)'}

## Acciones (90 días)
{acciones}

## Reflexión
{txt}
"""
    st.download_button("Descargar informe (.md)", md.encode("utf-8"), "s30_auto_radar_ra.md")

if __name__ == "__main__":
    main()
