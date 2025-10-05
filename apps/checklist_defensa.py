# apps/checklist_defensa.py
import streamlit as st
from datetime import datetime

CRITERIOS = [
    ("Problema y objetivo claros", 0.15),
    ("Marco jurídico bien delimitado", 0.15),
    ("Arquitectura técnica comprensible", 0.15),
    ("Riesgos y mitigaciones (EEE)", 0.15),
    ("Evidencias/mini-app funcional", 0.15),
    ("Impacto ético y social", 0.10),
    ("Viabilidad económica (costes/gas/compliance)", 0.10),
    ("Calidad expositiva (tiempos, narrativa, slidecraft)", 0.05),
]

TIPOS_PREG = [
    "Validez jurídica (consentimiento/objeto/forma)",
    "RGPD/Privacidad (bases, minimización, olvido)",
    "Responsabilidad (oráculos, bugs, governance)",
    "Compliance (MiCA, DORA, AML/KYC)",
    "Viabilidad técnica (rendimiento, gas, seguridad)",
]

def main(st=st):
    st.set_page_config(page_title="Checklist de defensa", page_icon="🎤", layout="wide")
    st.title("Checklist de defensa — Proyecto final")

    st.caption("Marca cada ítem y controla el tiempo de exposición. La app calcula un score orientativo.")

    # Control de tiempo
    colT1, colT2 = st.columns(2)
    with colT1:
        minutos = st.number_input("Tiempo disponible (min)", 5, 30, 12, step=1)
    with colT2:
        reparto = st.slider("Porcentaje para demo (UI/mini-app)", 10, 70, 35, step=5)
        st.caption(f"→ {int(minutos*reparto/100)} min demo · {int(minutos*(100-reparto)/100)} min discurso/QA")

    st.subheader("Criterios (marca los alcanzados)")
    puntos = 0.0
    total = sum(w for _, w in CRITERIOS)
    cols = st.columns(2)
    checks = []
    for i, (label, w) in enumerate(CRITERIOS):
        with cols[i % 2]:
            ok = st.checkbox(f"{label}  —  {int(w*100)}%")
            checks.append(ok)
            if ok: puntos += w

    score = round(100 * puntos / total, 1)
    st.metric("Score checklist (orientativo)", f"{score} / 100")

    st.subheader("Banco de preguntas (ensayo en voz alta)")
    sel = st.multiselect("Ensaya cómo responderías a…", TIPOS_PREG, default=TIPOS_PREG[:3])
    for q in sel:
        st.markdown(f"- **{q}** — apunta tu respuesta en una frase.")

    st.text_area("Notas rápidas para responder preguntas", placeholder="Idea-fuerza + evidencia pública + limitaciones + cierre…")

    st.divider()
    st.subheader("Síntesis (4–6 líneas)")
    txt = st.text_area("Escribe el cierre de tu defensa (mensaje principal + por qué importa).")

    md = f"""# S29 · Checklist de defensa
- Fecha: {datetime.utcnow().isoformat()}Z
- Tiempo total: {minutos} min · Demo: {reparto}% 
- Score checklist: {score} / 100

## Criterios marcados
""" + "\n".join([f"- [x] {lbl}" if ck else f"- [ ] {lbl}" for (lbl, _), ck in zip(CRITERIOS, checks)]) + f"""

## Preguntas ensayadas
- {chr(10).join(sel) if sel else '(ninguna)'}

## Cierre
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s29_checklist_defensa.md")

if __name__ == "__main__":
    main()
