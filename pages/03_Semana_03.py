import streamlit as st, importlib
st.set_page_config(page_title="Semana 3", page_icon="⚖️", layout="wide")
st.title("Semana 3 · PoS y gobernanza Bitcoin")

opts = {
    "S5 · Comparador PoW/PoS/BFT (radar)": "apps.consenso_radar",
    "S6 · Explorador BIP sintético": "apps.bip_explorador",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
