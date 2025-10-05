# apps/pow_energia.py
import streamlit as st, hashlib, random, time
from datetime import datetime

def main(st=st):
    st.set_page_config(page_title="Simulador PoW", page_icon="⚡", layout="wide")
    st.title("Simulador de energía y coste — Proof of Work")

    dif = st.slider("Dificultad (nº de ceros al inicio)", 1, 6, 3)
    kwh_por_mhash = st.number_input("kWh por 1e6 hashes (estimado)", 0.001, 10.0, 0.25, step=0.01)
    c_kwh = st.number_input("Coste kWh (€)", 0.01, 2.0, 0.20, step=0.01)
    target = "0"*dif

    st.caption("Nota didáctica: cálculo aproximado (no hardware real).")
    if st.button("Ejecutar prueba breve"):
        N = 100_000
        t0 = time.time()
        found = False
        for _ in range(N):
            raw = str(random.random())
            h = hashlib.sha256(raw.encode()).hexdigest()
            if h.startswith(target):
                found = True
                break
        t = max(time.time() - t0, 0.001)
        p = (1/16)**dif
        hashes_esperados = 1/p
        energia_kwh = (hashes_esperados/1e6) * kwh_por_mhash
        coste = energia_kwh * c_kwh
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Muestra (s)", f"{t:.2f}")
        c2.metric("Prob. teórica", f"{p:.2e}")
        c3.metric("Hashes esperados", f"{hashes_esperados:,.0f}")
        c4.metric("Coste estimado (€)", f"{coste:,.4f}")

    st.divider()
    sint = st.text_area("Síntesis (6–8 líneas): justificación jurídica del gasto energético.")
    st.download_button("Descargar (.md)", f"# S04 PoW\n\n{sint}".encode("utf-8"),
                       file_name="s04_sintesis.md", mime="text/markdown")

if __name__ == "__main__":
    main()
