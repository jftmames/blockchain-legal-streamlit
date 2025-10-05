import streamlit as st, importlib
st.set_page_config(page_title="Semana 15", page_icon="🎓", layout="wide")
st.title("Semana 15 · Defensa y síntesis ética")

opts = {
    "S29 · Checklist de defensa": "apps.checklist_defensa",
    "S30 · Autoevaluación radar RA": "apps.auto_radar_ra",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
