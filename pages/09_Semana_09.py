import streamlit as st, importlib
st.set_page_config(page_title="Semana 9", page_icon="🧪", layout="wide")
st.title("Semana 9 · Prueba digital y peritaje")

opts = {
    "S17 · Prueba hash (integridad)": "apps.prueba_hash",
    "S18 · Informe pericial (MD/PDF)": "apps.informe_pericial",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
