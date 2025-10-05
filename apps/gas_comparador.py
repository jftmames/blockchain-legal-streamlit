# apps/gas_comparador.py
import streamlit as st
from datetime import datetime

def main(st=st):
    st.set_page_config(page_title="Comparador de Gas", page_icon="⛽", layout="wide")
    st.title("Comparador de Gas — Estimación didáctica por complejidad")

    st.caption("Modelo didáctico. Para estimaciones reales, usa herramientas de red (p.ej., estimador y verificación pública).")

    ops_lec = st.number_input("Operaciones de lectura de estado", 0, 10_000, 300, step=50)
    ops_escr = st.number_input("Operaciones de escritura de estado", 0, 10_000, 120, step=20)
    ops_cript = st.number_input("Operaciones criptográficas/pesadas", 0, 10_000, 40, step=10)
    precio_gwei = st.number_input("Precio del gas (Gwei)", 1.0, 5000.0, 20.0, step=1.0)
    eth_eur = st.number_input("Tipo de cambio ETH→EUR", 200.0, 10000.0, 3000.0, step=50.0)

    # Pesos didácticos
    W_READ, W_WRITE, W_CRYPTO = 5, 20, 200
    gas_est = ops_lec*W_READ + ops_escr*W_WRITE + ops_cript*W_CRYPTO
    coste_eth = gas_est * precio_gwei * 1e-9
    coste_eur = coste_eth * eth_eur

    c1, c2, c3 = st.columns(3)
    c1.metric("Gas estimado", f"{gas_est:,}")
    c2.metric("Coste estimado (ETH)", f"{coste_eth:.6f}")
    c3.metric("Coste estimado (€)", f"{coste_eur:.4f}")

    st.info("Tip: compara dos versiones de una función para visualizar el impacto de escribir estado o usar cripto pesada.")

    st.divider()
    st.subheader("Evidencia y síntesis")
    txt = st.text_area("¿Cómo puede servir la estimación/registro de gas como evidencia (verificación pública de tx)?")
    md = f"""# S14 · Comparador de Gas
- Fecha: {datetime.utcnow().isoformat()}Z
- Ops lectura: {ops_lec} · escritura: {ops_escr} · cripto: {ops_cript}
- Gas estimado: {gas_est}
- Gas price: {precio_gwei} Gwei · ETH/EUR: {eth_eur}
- Coste: {coste_eth:.6f} ETH ≈ {coste_eur:.4f} €
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), file_name="s14_gas_comparador.md")

if __name__ == "__main__":
    main()
