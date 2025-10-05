import streamlit as st, importlib
st.set_page_config(page_title="Semana 12", page_icon="🧯", layout="wide")
st.title("Semana 12 · Compliance y ciberseguridad")

opts = {
    "S23 · Mapa de cumplimiento (MiCA/DORA/AML)": "apps.mapa_cumplimiento",
    "S24 · Simulador de incidentes": "apps.incidentes_simulador",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
