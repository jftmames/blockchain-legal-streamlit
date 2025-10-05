import streamlit as st, importlib
st.set_page_config(page_title="Semana 5", page_icon="🏭", layout="wide")
st.title("Semana 5 · Redes empresariales y cadena de valor")

opts = {
    "S9 · Selector de red": "apps.selector_red",
    "S10 · Trazabilidad Supply Chain (Sankey)": "apps.sankey_trazabilidad",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
