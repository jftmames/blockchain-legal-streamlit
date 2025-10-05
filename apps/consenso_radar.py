# apps/consenso_radar.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def main(st=st):
    st.set_page_config(page_title="Comparador Consenso", page_icon="🧭", layout="wide")
    st.title("Comparador de consenso: PoW · PoS · BFT")

    col1, col2, col3 = st.columns(3)
    with col1:
        pow_seg = st.slider("PoW · Seguridad", 1, 10, 9)
        pow_des = st.slider("PoW · Descentralización", 1, 10, 9)
        pow_efi = st.slider("PoW · Eficiencia", 1, 10, 3)
    with col2:
        pos_seg = st.slider("PoS · Seguridad", 1, 10, 8)
        pos_des = st.slider("PoS · Descentralización", 1, 10, 7)
        pos_efi = st.slider("PoS · Eficiencia", 1, 10, 9)
    with col3:
        bft_seg = st.slider("BFT · Seguridad", 1, 10, 8)
        bft_des = st.slider("BFT · Descentralización", 1, 10, 3)
        bft_efi = st.slider("BFT · Eficiencia", 1, 10, 9)

    df = pd.DataFrame({
        "Métrica": ["Seguridad", "Descentralización", "Eficiencia"],
        "PoW": [pow_seg, pow_des, pow_efi],
        "PoS": [pos_seg, pos_des, pos_efi],
        "BFT": [bft_seg, bft_des, bft_efi],
    })
    melt = df.melt(id_vars=["Métrica"], var_name="Algoritmo", value_name="Valor")

    fig = px.line_polar(melt, r="Valor", theta="Métrica", color="Algoritmo",
                        line_close=True, range_r=[0, 10])
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Síntesis comparada (5–7 líneas)")
    txt = st.text_area("¿Qué modelo debería inspirar la regulación europea y por qué?")
    md = f"""# S05 · Comparador de Consenso
- Fecha: {datetime.utcnow().isoformat()}Z
- PoW: {pow_seg}/{pow_des}/{pow_efi}
- PoS: {pos_seg}/{pos_des}/{pos_efi}
- BFT: {bft_seg}/{bft_des}/{bft_efi}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"),
                       file_name="s05_consenso_radar.md")

if __name__ == "__main__":
    main()
