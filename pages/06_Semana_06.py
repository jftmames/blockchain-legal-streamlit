import streamlit as st, importlib
st.set_page_config(page_title="Semana 6", page_icon="🏛️", layout="wide")
st.title("Semana 6 · Sector público y riesgos")

opts = {
    "S11 · Licitación trazable (hash + sello)": "apps.licitacion_trazable",
    "S12 · Mapa de riesgos (heatmap)": "apps.mapa_riesgos",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
