# apps/selector_red.py
import streamlit as st
from datetime import datetime

CRITERIOS = [
    ("Privacidad alta", 0.35, {"privada/consorcio": 2, "pública": -2}),
    ("Necesidad de auditoría pública", 0.25, {"pública": 2, "privada/consorcio": -1}),
    ("Coste crítico", 0.15, {"privada/consorcio": 1, "pública": 1}),
    ("Escala abierta (muchos participantes anónimos)", 0.15, {"pública": 2, "privada/consorcio": -1}),
    ("Gobernanza formal por contrato", 0.10, {"privada/consorcio": 2, "pública": 0}),
]

def _score(respuestas):
    puntos = {"pública": 0.0, "privada/consorcio": 0.0}
    for (label, w, weights), si in zip(CRITERIOS, respuestas):
        mult = 1 if si else 0
        for red, val in weights.items():
            puntos[red] += w * val * mult
    return puntos

def main(st=st):
    st.set_page_config(page_title="Selector de red", page_icon="🌐", layout="wide")
    st.title("Selector de red: pública vs privada/consorcio")

    st.caption("Marca los criterios que aplican a tu caso de uso.")
    respuestas = []
    for label, _, _ in CRITERIOS:
        respuestas.append(st.checkbox(label))

    puntos = _score(respuestas)
    recomendada = max(puntos, key=puntos.get)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pública (score)", f"{puntos['pública']:.2f}")
    with col2:
        st.metric("Privada/Consorcio (score)", f"{puntos['privada/consorcio']:.2f}")

    st.success(f"**Recomendación:** {recomendada.upper()}") if puntos[recomendada] > 0 else st.info("Escenario equilibrado; requiere análisis adicional.")

    st.subheader("Notas jurídicas rápidas")
    if recomendada == "pública":
        st.markdown("- Transparencia fuerte; evalúa RGPD y revelación de metadatos.\n- Difícil control de jurisdicción y borrado.")
    else:
        st.markdown("- Control de acceso y SLA entre miembros.\n- Facilitación de cumplimiento (RGPD, DORA).")

    st.divider()
    txt = st.text_area("Síntesis (5–7 líneas): justifica la recomendación.")
    md = f"""# S09 · Selector de red
- Fecha: {datetime.utcnow().isoformat()}Z
- Selección: {', '.join([l for (l,_,_), s in zip(CRITERIOS, respuestas) if s])}
- Score pública: {puntos['pública']:.2f}
- Score privada/consorcio: {puntos['privada/consorcio']:.2f}
- Recomendación: {recomendada}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s09_selector_red.md")

if __name__ == "__main__":
    main()
