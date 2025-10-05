import streamlit as st, importlib
st.set_page_config(page_title="Semana 4", page_icon="🔐", layout="wide")
st.title("Semana 4 · Criptografía aplicada y trazabilidad")

opts = {
    "S7 · Firma y verificación RSA": "apps.firma_rsa",
    "S8 · Matriz RGPD–Trazabilidad": "apps.rgpd_matriz",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
