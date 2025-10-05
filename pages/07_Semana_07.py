import streamlit as st, importlib
st.set_page_config(page_title="Semana 7", page_icon="📜", layout="wide")
st.title("Semana 7 · Smart Contracts (lectura y entorno)")

opts = {
    "S13 · Flujo oferta–aceptación–pago": "apps.flujo_contrato",
    "S14 · Comparador de gas + Etherscan": "apps.gas_comparador",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
