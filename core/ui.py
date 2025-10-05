import streamlit as st
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class UD:
    title: str
    bullets: List[str]
    readings: Optional[List[str]] = None

def header(week:int, title:str, subtitle:str=""):
    st.title(f"Semana {week} · {title}")
    if subtitle: st.caption(subtitle)
    st.divider()

def ud_block(ud: UD):
    st.subheader(ud.title)
    for b in ud.bullets: st.markdown(f"- {b}")
    if ud.readings:
        with st.expander("Lecturas sugeridas"):
            for r in ud.readings: st.write("•", r)
