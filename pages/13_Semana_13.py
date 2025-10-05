import streamlit as st, importlib
st.set_page_config(page_title="Semana 13", page_icon="🌍", layout="wide")
st.title("Semana 13 · Derecho comparado, IA y licencias")

opts = {
    "S25 · Semáforo regulatorio global": "apps.semaforo_regulatorio",
    "S26 · Explorador de licencias (OSS)": "apps.explorador_licencias",
    "S26bis · Pseudocódigo LegalTech": "apps.pseudocodigo_legaltech",
}
sel = st.radio("Elige sesión", list(opts.keys()))
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
