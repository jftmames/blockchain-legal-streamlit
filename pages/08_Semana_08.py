import streamlit as st, importlib
st.set_page_config(page_title="Semana 8", page_icon="🧩", layout="wide")
st.title("Semana 8 · Validez y responsabilidad + oráculos")

opts = {
    "S15 · Checklist de validez (SC)": "apps.checklist_validez_sc",
    "S16 · Simulador de oráculo": "apps.oraculo_simulador",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod_name = opts[sel]
try:
    mod = importlib.import_module(mod_name)
    importlib.reload(mod)  # hot reload al cambiar de opción
    if not hasattr(mod, "main"):
        st.error(f"La mini-app `{mod_name}` debe exponer `def main(st): ...`")
    else:
        mod.main(st)
except ModuleNotFoundError as e:
    st.error(f"No se encontró el módulo `{mod_name}`. ¿Existe `apps/{mod_name.split('.')[-1]}.py`?")
    st.exception(e)
except Exception as e:
    st.exception(e)
