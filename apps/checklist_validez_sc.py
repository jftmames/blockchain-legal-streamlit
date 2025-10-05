# apps/checklist_validez_sc.py
import streamlit as st
from datetime import datetime

def _score(val: bool) -> int:
    return 1 if val else 0

def _resultado(puntos:int) -> str:
    if puntos >= 8: return "ALTA probabilidad de validez (con reservas)"
    if puntos >= 6: return "VALIDEZ probable con riesgos"
    if puntos >= 4: return "DUDOSA: requiere refuerzo jurídico"
    return "BAJA: alto riesgo de invalidez o ineficacia"

def main(st=st):
    st.set_page_config(page_title="Checklist Validez SC", page_icon="✅", layout="wide")
    st.title("Checklist de validez — Smart Contract (civil/mercantil)")

    col1, col2 = st.columns(2)
    with col1:
        jurisd = st.selectbox("Jurisdicción principal", ["España (UE)", "EE. UU.", "LatAm", "Otra"])
        hay_texto = st.checkbox("Existe texto legal/paracontractual que describe el acuerdo")
        consentimiento = st.checkbox("Consentimiento inequívoco de las partes")
        objeto_licito = st.checkbox("Objeto lícito y posible")
        causa_valida = st.checkbox("Causa/contraprestación válida")
        forma_exigida = st.checkbox("Se cumple forma exigida (si aplica)")
    with col2:
        prueba = st.checkbox("Prueba suficiente: logs, hashes, verificación pública")
        identificacion = st.checkbox("Identificación adecuada (KYC/atribución de claves)")
        jurisdiccion = st.checkbox("Cláusulas de jurisdicción/ley aplicable")
        consumo = st.checkbox("Cumple normativa de consumo (si B2C)")
        ip_licencias = st.checkbox("Respeta licencias y propiedad intelectual")
        rgpd = st.checkbox("Cumple RGPD/privacidad (si hay datos personales)")

    puntos = sum([
        _score(hay_texto), _score(consentimiento), _score(objeto_licito),
        _score(causa_valida), _score(forma_exigida), _score(prueba),
        _score(identificacion), _score(jurisdiccion), _score(consumo),
        _score(ip_licencias), _score(rgpd)
    ])

    st.metric("Puntuación", f"{puntos}/11")
    st.success(_resultado(puntos)) if puntos>=6 else st.warning(_resultado(puntos))

    st.divider()
    st.subheader("Recomendaciones mínimas")
    if not hay_texto: st.markdown("- Añade documento legal (smart legal contract / Ricardian).")
    if not prueba: st.markdown("- Habilita verificación pública (hash, Etherscan, logs).")
    if not identificacion: st.markdown("- Atribuye identidad a direcciones (KYC/PSI).")
    if not jurisdiccion: st.markdown("- Fija jurisdicción y ley aplicable.")
    if not ip_licencias: st.markdown("- Revisa licencias OSS y derechos de autor.")
    if not rgpd: st.markdown("- Evalúa DPIA y minimización off-chain.")

    st.divider()
    st.subheader("Síntesis (5–7 líneas)")
    txt = st.text_area("Explica si tu contrato sería válido y qué reforzarías.")
    md = f"""# S15 · Checklist validez SC
- Fecha: {datetime.utcnow().isoformat()}Z
- Jurisdicción: {jurisd}
- Puntos: {puntos}/11 → {_resultado(puntos)}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s15_checklist_validez.md")

if __name__ == "__main__":
    main()
