import streamlit as st, importlib
st.set_page_config(page_title="Semana 6", page_icon="🏛️", layout="wide")
st.title("Semana 6 · Sector público y riesgos")

opts = {
    "S11 · Licitación trazable (hash + sello)": "apps.licitacion_trazable",
    "S12 · Mapa de riesgos (heatmap)": "apps.mapa_riesgos",
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
