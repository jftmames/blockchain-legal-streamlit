import streamlit as st, importlib
st.set_page_config(page_title="Semana 10", page_icon="🛡️", layout="wide")
st.title("Semana 10 · RGPD y derecho al olvido")

opts = {
    "S19 · Matriz RGPD (roles/bases)": "apps.rgpd_roles_bases",
    "S20 · Evaluador de anonimización": "apps.anonimizador_eval",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
