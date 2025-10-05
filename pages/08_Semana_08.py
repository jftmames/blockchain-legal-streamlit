import streamlit as st, importlib
st.set_page_config(page_title="Semana 8", page_icon="🧩", layout="wide")
st.title("Semana 8 · Validez y responsabilidad + oráculos")

opts = {
    "S15 · Checklist de validez (SC)": "apps.checklist_validez_sc",
    "S16 · Simulador de oráculo": "apps.oraculo_simulador",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
