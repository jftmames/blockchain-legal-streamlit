import streamlit as st, importlib
st.set_page_config(page_title="Semana 11", page_icon="🪙", layout="wide")
st.title("Semana 11 · Tokenización, NFTs y DAOs")

opts = {
    "S21 · Ficha legal de token/NFT": "apps.ficha_token",
    "S22 · Arbitraje DAO (Kleros/Aragon)": "apps.arbitraje_dao",
}
sel = st.radio("Elige sesión", list(opts.keys()), horizontal=True)
mod = importlib.import_module(opts[sel])
(getattr(mod, "main", lambda st: exec(open(mod.__file__, "r", encoding="utf-8").read(), {})))(st)
