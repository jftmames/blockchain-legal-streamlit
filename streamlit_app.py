import streamlit as st
import importlib

st.set_page_config(page_title="Blockchain & Derecho", page_icon="⚖️", layout="wide")

st.title("Portal docente · Blockchain: fundamentos técnicos y problemática jurídica")
st.caption("Selecciona una semana/sesión o usa el menú 'Pages' de la izquierda.")

# Mapa Sesión -> módulo apps/<archivo>.py
MAP = {
    "Semana 1": {
        "S1 · Hash Visual": "apps.hash_visual_demo",
        "S2 · Sello de tiempo": "apps.sello_tiempo",
    },
    "Semana 2": {
        "S3 · Cadena interactiva": "apps.cadena_interactiva",
        "S4 · PoW energía": "apps.pow_energia",
    },
    # ... rellena hasta Semana 15 con todas las sesiones ...
}

sem = st.selectbox("Semana", list(MAP.keys()))
ses = st.selectbox("Sesión", list(MAP[sem].keys()))
mod_name = MAP[sem][ses]

st.divider()
st.markdown(f"### {ses}")

try:
    mod = importlib.import_module(mod_name)
    # cada mini-app debe exponer una función `main(st)`
    if hasattr(mod, "main"):
        mod.main(st)
    else:
        st.warning("La mini-app no define `main(st)`. Abriéndose en modo embed.")
        # fallback: ejecutar el módulo (si usa top-level code)
        exec(open(mod.__file__, "r", encoding="utf-8").read(), {})
except ModuleNotFoundError as e:
    st.error(f"Mini-app no encontrada: {mod_name}\n{e}")
