# apps/semaforo_regulatorio.py
import streamlit as st
import pandas as pd
from datetime import datetime

MARCOS = ["Cripto-activos (mercado primario/secundario)", "DeFi/DEX", "Custodia/Wallet", "Tokenización de valores", "AML/KYC", "Sandbox/innovación"]
PAISES = [
    "UE (MiCA)", "EE. UU.", "Reino Unido", "Suiza", "Singapur", "EAU", "España", "LatAm (general)"
]

# 0=rojo,1=ámbar,2=verde (didáctico)
RATING = {
    "UE (MiCA)":                 [1, 1, 2, 2, 2, 2],
    "EE. UU.":                   [0, 0, 1, 1, 2, 1],
    "Reino Unido":               [2, 1, 2, 2, 2, 2],
    "Suiza":                     [2, 1, 2, 2, 2, 1],
    "Singapur":                  [2, 1, 2, 2, 2, 2],
    "EAU":                       [2, 1, 2, 2, 2, 2],
    "España":                    [1, 1, 2, 2, 2, 2],
    "LatAm (general)":           [1, 0, 1, 1, 1, 1],
}
EXPL = {0:"Rojo (riesgo/regulación adversa)", 1:"Ámbar (incertidumbre/transición)", 2:"Verde (marco claro/favorable)"}
COLOR = {0:"🟥", 1:"🟨", 2:"🟩"}

def _tabla(pais:str):
    vals = RATING[pais]
    rows = [{"Área": a, "Semáforo": COLOR[v], "Interpretación": EXPL[v]} for a, v in zip(MARCOS, vals)]
    return pd.DataFrame(rows)

def main(st=st):
    st.set_page_config(page_title="Semáforo regulatorio", page_icon="🚦", layout="wide")
    st.title("Semáforo regulatorio global (demo didáctica)")

    pais = st.selectbox("País/Jurisdicción", PAISES, index=0)
    df = _tabla(pais)
    st.dataframe(df, use_container_width=True)

    st.subheader("Comparativa rápida")
    otros = st.multiselect("Compara con", [p for p in PAISES if p != pais], default=["EE. UU.", "Reino Unido"])
    if otros:
        comp = pd.DataFrame({pais: RATING[pais]}, index=MARCOS)
        for o in otros: comp[o] = RATING[o]
        comp = comp.replace(EXPL).replace(COLOR)
        st.dataframe(comp, use_container_width=True)

    st.divider()
    st.subheader("Síntesis (6–8 líneas)")
    txt = st.text_area("¿Qué jurisdicción equilibra mejor innovación y protección en tu caso de uso concreto?")
    md = f"""# S25 · Semáforo regulatorio
- Fecha: {datetime.utcnow().isoformat()}Z
- Jurisdicción base: {pais}
## Tabla
{df.to_markdown(index=False)}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s25_semaforo_regulatorio.md")

if __name__ == "__main__":
    main()
