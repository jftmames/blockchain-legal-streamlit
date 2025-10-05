# apps/ficha_token.py
import streamlit as st
from datetime import datetime
import pandas as pd

TIPO = ["Utility", "Payment", "Asset-referenced", "E-money", "Security-like", "NFT (único)"]
DERECHOS = [
    "Acceso a servicio",
    "Descuento/bono",
    "Derecho de voto",
    "Derecho económico (dividend-like)",
    "Derecho de uso de obra (licencia)",
    "Ninguno (coleccionable)"
]

def _mica_hint(tipo:str):
    if tipo == "E-money": return "Probable **EMT** (MiCA): requisitos de fondos y emisión."
    if tipo == "Asset-referenced": return "Probable **ART** (MiCA): canasta de activos como referencia."
    if tipo == "Payment": return "Puede caer en MiCA como token de uso general (riesgo EMT/ART si promete paridad)."
    if tipo == "Security-like": return "Posible **valores mobiliarios** (MiFID/Prospectus); fuera de MiCA."
    if tipo == "Utility": return "Utility puro (MiCA): revisar si realmente da acceso a servicio presente."
    if tipo == "NFT (único)": return "Si es realmente **único/no fraccionable**, MiCA podría no aplicar salvo asimilación económica."
    return "Revisar caso concreto."

def main(st=st):
    st.set_page_config(page_title="Ficha legal de Token/NFT", page_icon="🪙", layout="wide")
    st.title("Ficha legal de Token / NFT — MiCA-lite")

    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del token", "UNIE-EDU")
        tipo = st.selectbox("Tipo", TIPO, index=0)
        oferta_publica = st.checkbox("Habrá oferta pública en la UE")
        custodia_terceros = st.checkbox("Habrá custodia por terceros (CEX/PSP)")
        transferible = st.selectbox("Transferibilidad", ["Libre", "Restringida (lista blanca)", "Intransferible (soulbound)"])
    with col2:
        dr = st.multiselect("Derechos asociados", DERECHOS, default=["Acceso a servicio"])
        royalties = st.number_input("Royalties (NFT) %", 0.0, 25.0, 0.0, step=0.5)
        kyc = st.checkbox("KYC a titulares (si aplica)")

    mica = _mica_hint(tipo)
    st.info(f"Sugerencia MiCA: {mica}")

    df = pd.DataFrame([{
        "Token": nombre, "Tipo": tipo, "Oferta pública UE": "Sí" if oferta_publica else "No",
        "Custodia terceros": "Sí" if custodia_terceros else "No",
        "Transferibilidad": transferible, "Derechos": ", ".join(dr) if dr else "(ninguno)",
        "Royalties%": royalties, "KYC": "Sí" if kyc else "No"
    }])
    st.subheader("Ficha resumida")
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("Riesgos y notas legales")
    if "Derecho económico (dividend-like)" in dr:
        st.warning("Derecho económico semejante a dividendo: riesgo de calificación como **valor**.")
    if tipo in ("Asset-referenced", "E-money"):
        st.warning("Requisitos estrictos MiCA para ART/EMT (capital, gobernanza, whitepaper).")
    if tipo.startswith("NFT") and royalties > 0:
        st.caption("Recuerda: los **royalties on-chain** no son exigibles en todos los marketplaces.")

    st.divider()
    st.subheader("Síntesis (6–8 líneas)")
    txt = st.text_area("Explica la calificación regulatoria prevista y los documentos a preparar (whitepaper, T&Cs, aviso de riesgos…)")
    md = f"""# S21 · Ficha legal Token/NFT
- Fecha: {datetime.utcnow().isoformat()}Z
{df.to_markdown(index=False)}
## Sugerencia MiCA
- {mica}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s21_ficha_token.md")

if __name__ == "__main__":
    main()
