# apps/rgpd_roles_bases.py
import streamlit as st
import pandas as pd
from datetime import datetime

BASES = [
    "Consentimiento",
    "Ejecución de contrato",
    "Obligación legal",
    "Intereses legítimos",
    "Interés público",
    "Vital (excepcional)",
]

def _sugerir_roles(escenario:str, red:str):
    if escenario == "Exchange centralizado":
        return "Responsable (Exchange)", "Encargado (proveedores)"
    if escenario == "Wallet self-custody":
        return "Usuario (Control efectivo)", "Proveedor (posible corresponsable si procesa datos)"
    if escenario == "DAO pública":
        return "Corresponsables (miembros/órganos)", "Proveedores (oráculos/exploradores) como encargados"
    if escenario == "Empresa consorcio (permissioned)":
        return "Corresponsables (miembros del consorcio)", "Encargados (operadores/IT)"
    return "Responsable", "Encargado"

def main(st=st):
    st.set_page_config(page_title="RGPD: Roles y Bases", page_icon="🛡️", layout="wide")
    st.title("Matriz RGPD — Roles y Bases legales")

    col1, col2 = st.columns(2)
    with col1:
        escenario = st.selectbox("Escenario", [
            "Exchange centralizado", "Wallet self-custody",
            "DAO pública", "Empresa consorcio (permissioned)", "Otro"
        ])
        red = st.selectbox("Tipo de red", ["Pública", "Privada/Consorcio"])
        dato = st.selectbox("Tipo de dato", ["No personal", "Personal", "Especial (art. 9)"])
    with col2:
        finalidades = st.multiselect("Finalidades", ["Registro transaccional", "Trazabilidad", "Prevención de fraude", "Atención al cliente"])
        base = st.selectbox("Base legal predominante", BASES, index=1)
        dpo = st.checkbox("Existe DPO/DPD designado")

    rol_resp, rol_enc = _sugerir_roles(escenario, red)
    df = pd.DataFrame([{
        "Escenario": escenario,
        "Red": red,
        "Dato": dato,
        "Base legal": base,
        "Roles": f"{rol_resp} / {rol_enc}",
        "Finalidades": ", ".join(finalidades) if finalidades else "(no indicado)",
        "DPO": "Sí" if dpo else "No"
    }])
    st.subheader("Diagnóstico")
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("Recomendaciones mínimas")
    if dato != "No personal":
        st.markdown("- Minimiza datos on-chain; prioriza off-chain con hash verificable.")
    if red == "Pública" and dato != "No personal":
        st.markdown("- Evalúa impacto (DPIA) y privacidad por defecto (privacy by design).")
    if escenario.startswith("Exchange"):
        st.markdown("- Registros AML/KYC; contratos de encargo y auditorías de proveedores.")
    if not dpo and dato != "No personal":
        st.markdown("- Designa DPO si procede por volumen/actividad de riesgo.")

    st.divider()
    txt = st.text_area("Síntesis (5–7 líneas): justifica la base legal y roles en tu caso.")
    md = f"""# S19 · Matriz RGPD (roles/bases)
- Fecha: {datetime.utcnow().isoformat()}Z
{df.to_markdown(index=False)}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s19_rgpd_roles_bases.md")

if __name__ == "__main__":
    main()
