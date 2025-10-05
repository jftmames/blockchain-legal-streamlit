import streamlit as st

def rubric_eee(defaults=(7,8,7)):
    e = st.slider("Ético (0-10)", 0, 10, defaults[0])
    ep = st.slider("Epistémico (0-10)", 0, 10, defaults[1])
    ec = st.slider("Económico (0-10)", 0, 10, defaults[2])
    score = round((e+ep+ec)/3, 2)
    st.metric("Score EEE", score)
    return {"etico": e, "epistemico": ep, "economico": ec, "score": score}
