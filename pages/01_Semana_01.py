import streamlit as st
import importlib

st.set_page_config(page_title="Semana 1", page_icon="📘", layout="wide")
st.title("Semana 1 · Introducción y confianza")

opts = {
    "S1 · Hash Visual": "apps.hash_visual_demo",
    "S2 · Sello de tiempo": "apps.sello_tiempo",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {}))(st)
