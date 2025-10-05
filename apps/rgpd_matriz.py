# apps/rgpd_matriz.py
import streamlit as st
from datetime import datetime

def _riesgo(tipo_dato:str, tecnica:str):
    # Scoring simple, didáctico
    base = {"personal": 3, "especial": 5, "no_personal": 1}.get(tipo_dato, 2)
    t = {
        "hash": 2,            # no anonimiza por sí mismo
        "pseudonimizacion": 2,
        "cifrado": 1,
        "offchain": 1,
    }.get(tecnica, 3)
    return max(1, min(5, base + (t-2)))

def _reco(tecnica:str):
    m = {
        "hash": "Añade sal y almacena el dato original fuera de cadena.",
        "pseudonimizacion": "Gestiona la tabla de correspondencia de forma segura.",
        "cifrado": "Custodia de claves y rotación periódica.",
        "offchain": "Verificación por hash; controla accesos al repositorio.",
    }
    return m.get(tecnica, "Revisa DPIA y aplica minimización de datos.")

def main(st=st):
    st.set_page_config(page_title="Matriz RGPD–Trazabilidad", page_icon="🔏", layout="wide")
    st.title("Matriz RGPD–Trazabilidad")

    tipo_dato = st.selectbox("Tipo de dato", ["personal", "especial", "no_personal"])
    tecnica = st.selectbox("Técnica aplicada", ["hash", "pseudonimizacion", "cifrado", "offchain"])
    red = st.selectbox("Tipo de red", ["pública", "privada/consorcio"])
    rol = st.selectbox("Rol principal", ["responsable", "encargado", "corresponsable"])

    riesgo = _riesgo(tipo_dato, tecnica)
    etiquetas = {1:"Muy bajo",2:"Bajo",3:"Medio",4:"Alto",5:"Muy alto"}
    st.metric("Riesgo residual (1-5)", f"{riesgo} · {etiquetas[riesgo]}")

    st.subheader("Recomendaciones")
    st.markdown(f"- { _reco(tecnica) }")
    if red == "pública":
        st.markdown("- Evalúa si el dato puede mantenerse off-chain con hash en cadena.")
    if rol == "encargado":
        st.markdown("- Revisa contrato de encargo y subencargados.")

    st.divider()
    st.subheader("Síntesis (5–7 líneas)")
    txt = st.text_area("¿Cómo compatibilizar inmutabilidad con minimización y limitación de conservación?")
    md = f"""# S08 · Matriz RGPD–Trazabilidad
- Fecha: {datetime.utcnow().isoformat()}Z
- Dato: {tipo_dato} · Técnica: {tecnica} · Red: {red} · Rol: {rol}
- Riesgo residual: {riesgo} / 5
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"),
                       file_name="s08_rgpd_matriz.md")

if __name__ == "__main__":
    main()
