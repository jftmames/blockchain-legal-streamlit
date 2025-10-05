import streamlit as st, importlib
st.set_page_config(page_title="Semana 2", page_icon="🔗", layout="wide")
st.title("Semana 2 · Anatomía de cadena y PoW")

opts = {
    "S3 · Cadena interactiva (5 bloques)": "apps.cadena_interactiva",
    "S4 · PoW energía": "apps.pow_energia",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
