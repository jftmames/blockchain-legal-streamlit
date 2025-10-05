# apps/bip_explorador.py
import streamlit as st
from datetime import datetime

BIPS = {
    "BIP-32 · HD Wallets": "Estructura jerárquica de claves. Facilita backups.",
    "BIP-141 · SegWit": "Aislamiento de testigo. Eficiencia y maleabilidad.",
    "BIP-340 · Schnorr": "Firmas Schnorr. Agregación y privacidad.",
}

def main(st=st):
    st.set_page_config(page_title="Explorador BIP", page_icon="📝", layout="wide")
    st.title("Explorador de BIPs (sintético)")

    bip = st.selectbox("Selecciona BIP", list(BIPS.keys()))
    apoyo = st.slider("Apoyo comunitario estimado (%)", 0, 100, 72)
    descripcion = BIPS[bip]
    st.info(descripcion)

    if apoyo >= 66:
        st.success("Estado: Adoptable (umbral informal ≈ 2/3).")
    else:
        st.warning("Estado: Consenso insuficiente.")

    st.divider()
    st.subheader("Síntesis (4–6 líneas)")
    txt = st.text_area("¿Cómo se legitima socialmente la adopción de un BIP sin autoridad central?")
    md = f"""# S06 · Explorador BIP
- Fecha: {datetime.utcnow().isoformat()}Z
- BIP: {bip}
- Apoyo: {apoyo}%
- Descripción: {descripcion}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"),
                       file_name="s06_bip_explorador.md")

if __name__ == "__main__":
    main()
