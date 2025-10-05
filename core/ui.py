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
    for b in ud.bullets:
        st.markdown(f"- {b}")
    if ud.readings:
        with st.expander("Lecturas sugeridas"):
            for r in ud.readings:
                st.write("•", r)

def rubric_eee():
    st.markdown("### Rúbrica EEE")
    e = st.slider("Ético", 0, 10, 7)
    ep = st.slider("Epistémico", 0, 10, 8)
    ec = st.slider("Económico", 0, 10, 7)
    score = round((e+ep+ec)/3, 2)
    st.metric("Score EEE", score)
    return {"etico":e,"epistemico":ep,"economico":ec,"score":score}
