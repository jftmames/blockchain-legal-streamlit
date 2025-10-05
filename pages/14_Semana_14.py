import streamlit as st, importlib
st.set_page_config(page_title="Semana 14", page_icon="🧩", layout="wide")
st.title("Semana 14 · Proyecto final y peer review")

opts = {
    "S27 · Canvas de proyecto": "apps.canvas_proyecto",
    "S28 · Rúbrica EEE (peer review)": "apps.rubrica_eee",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
