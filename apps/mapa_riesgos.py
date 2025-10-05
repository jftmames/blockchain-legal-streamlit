# apps/mapa_riesgos.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

RIESGOS_BASE = [
    "Ataque 51%",
    "Pérdida de claves",
    "Oráculo manipulado",
    "Rug pull / fraude",
    "Fallo de privacidad (RGPD)",
    "DoS / latencia crítica",
]

CONTROLES = {
    "Ataque 51%": "Diversificar hashpower / migrar consenso",
    "Pérdida de claves": "MFA + wallet con multisig / HSM",
    "Oráculo manipulado": "Oráculos redundantes + agregación",
    "Rug pull / fraude": "Auditorías + timelocks + governance",
    "Fallo de privacidad (RGPD)": "Off-chain + cifrado + DPA",
    "DoS / latencia crítica": "Rate limiting + CDN + QoS",
}

def _heatmap(df):
    import plotly.express as px
    fig = px.density_heatmap(
        df, x="Probabilidad", y="Impacto", z="Score",
        histfunc="sum", nbinsx=5, nbinsy=5, range_x=[1,5], range_y=[1,5],
        color_continuous_scale="YlOrRd"
    )
    fig.update_layout(height=450, margin=dict(l=20,r=20,t=20,b=20))
    return fig

def main(st=st):
    st.set_page_config(page_title="Mapa de riesgos", page_icon="⚠️", layout="wide")
    st.title("Mapa de riesgos — Probabilidad × Impacto")

    st.caption("Valora cada riesgo del 1 (bajo) al 5 (muy alto).")
    data = []
    for r in RIESGOS_BASE:
        c1, c2 = st.columns(2)
        with c1:
            p = st.slider(f"{r} · Probabilidad", 1, 5, 3, key=f"p_{r}")
        with c2:
            i = st.slider(f"{r} · Impacto", 1, 5, 3, key=f"i_{r}")
        score = p * i
        data.append({"Riesgo": r, "Probabilidad": p, "Impacto": i, "Score": score, "Control": CONTROLES[r]})

    df = pd.DataFrame(data).sort_values("Score", ascending=False)
    st.dataframe(df, use_container_width=True)
    st.plotly_chart(_heatmap(df), use_container_width=True)

    top = df.iloc[0]
    st.info(f"**Prioritario:** {top['Riesgo']} · Score {int(top['Score'])} → Control sugerido: {top['Control']}")

    st.divider()
    txt = st.text_area("Síntesis (5–7 líneas): correlato jurídico de los principales riesgos.")
    md = f"""# S12 · Mapa de riesgos
- Fecha: {datetime.utcnow().isoformat()}Z
- Top riesgo: {top['Riesgo']} (Score {int(top['Score'])})
## Tabla
{df.to_markdown(index=False)}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s12_mapa_riesgos.md")

if __name__ == "__main__":
    main()
