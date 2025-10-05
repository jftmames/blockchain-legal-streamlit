# apps/incidentes_simulador.py
import streamlit as st
from datetime import datetime

INCIDENTES = {
    "Reentrancy (DeFi)": ["Auditoría externa", "Patrón checks-effects-interactions", "ReentrancyGuard", "Pruebas con fuzzing"],
    "Rug pull": ["Timelock de owner", "Multisig para upgrades", "Transparencia en tokenomics"],
    "Pérdida de claves": ["MFA", "Hardware wallet/HSM", "Política de recuperación", "Segregación de roles"],
    "Oráculo manipulado": ["Oráculos redundantes", "TWAP/medianizador", "Pausable/guardian"],
    "DoS / Congestión": ["Rate limiting", "CDN/Cache", "Circuit breakers"],
}

def _riesgo_residual(base:int, controles_aplicados:int):
    # modelo didáctico: cada control baja 1 punto hasta mínimo 1
    return max(1, base - controles_aplicados)

def main(st=st):
    st.set_page_config(page_title="Simulador de incidentes", page_icon="🧯", layout="wide")
    st.title("Simulador de incidentes — riesgo residual y mitigación")

    inc = st.selectbox("Incidente", list(INCIDENTES.keys()))
    base = st.slider("Severidad base (1-5)", 1, 5, 4)
    controles = INCIDENTES[inc]
    aplicados = st.multiselect("Controles aplicados", controles, default=[])

    residual = _riesgo_residual(base, len(aplicados))
    etq = {1:"Muy bajo",2:"Bajo",3:"Medio",4:"Alto",5:"Crítico"}[residual]
    st.metric("Riesgo residual", f"{residual} · {etq}")

    st.subheader("Recomendación mínima")
    faltantes = [c for c in controles if c not in aplicados]
    if faltantes:
        st.markdown("- Implementa también: " + ", ".join(faltantes))
    else:
        st.success("Conjunto de controles recomendable aplicado.")

    st.divider()
    txt = st.text_area("Síntesis (5–7 líneas): encaje jurídico del incidente (responsabilidad, deber de diligencia, notificación).")
    md = f"""# S24 · Simulador de incidentes
- Fecha: {datetime.utcnow().isoformat()}Z
- Incidente: {inc}
- Severidad base: {base}
- Controles aplicados: {', '.join(aplicados) if aplicados else '(ninguno)'}
- Riesgo residual: {residual}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s24_incidentes.md")

if __name__ == "__main__":
    main()
