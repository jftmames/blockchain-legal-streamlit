# apps/anonimizador_eval.py
import streamlit as st
from datetime import datetime

def _riesgo(tipo:str, tecnica:str, salt:bool, offchain:bool) -> int:
    base = {"No personal":1, "Personal":3, "Especial (art. 9)":5}[tipo]
    t = {"Hash":2, "Hash+Salt":1, "Pseudonimización":2, "Cifrado":1, "Off-chain + Hash":1}.get(tecnica, 3)
    bonus = -1 if salt else 0
    bonus += -1 if offchain else 0
    return max(1, min(5, base + t + bonus - 2))  # centrado didáctico

def main(st=st):
    st.set_page_config(page_title="Evaluador de anonimización", page_icon="🧩", layout="wide")
    st.title("Evaluador de anonimización / derecho al olvido")

    tipo = st.selectbox("Tipo de dato", ["No personal", "Personal", "Especial (art. 9)"])
    tecnica = st.selectbox("Técnica", ["Hash", "Hash+Salt", "Pseudonimización", "Cifrado", "Off-chain + Hash"])
    salt = st.checkbox("Gestión correcta de 'salt' / claves")
    offchain = st.checkbox("Datos fuera de cadena con verificación por hash")

    riesgo = _riesgo(tipo, tecnica, salt, offchain)
    etiquetas = {1:"Muy bajo",2:"Bajo",3:"Medio",4:"Alto",5:"Muy alto"}
    st.metric("Riesgo de reidentificación", f"{riesgo} · {etiquetas[riesgo]}")

    st.subheader("Notas")
    if tecnica == "Hash":
        st.markdown("- El hash **no** es anonimización per se; puede ser pseudónimo reversible por diccionario.")
    if tecnica in ("Hash+Salt", "Cifrado"):
        st.markdown("- La seguridad depende de la gestión de **sal**/claves (rotación, acceso, custodia).")
    if tecnica.startswith("Off-chain"):
        st.markdown("- Mantén on-chain solo el hash; controla accesos y retenciones off-chain.")

    st.divider()
    st.subheader("Síntesis (5–7 líneas)")
    txt = st.text_area("Explica cómo cumplirías el derecho de supresión en tu diseño.")
    md = f"""# S20 · Evaluador de anonimización
- Fecha: {datetime.utcnow().isoformat()}Z
- Tipo de dato: {tipo}
- Técnica: {tecnica}
- 'Salt' gestionado: {salt}
- Off-chain: {offchain}
- Riesgo: {riesgo}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s20_anonimizador_eval.md")

if __name__ == "__main__":
    main()
