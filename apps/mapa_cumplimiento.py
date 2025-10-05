# apps/mapa_cumplimiento.py
import streamlit as st
import pandas as pd
from datetime import datetime

ACTORES = ["CEX (exchange centralizado)", "DEX (intercambio descentralizado)", "Wallet/Custodia", "Emisor de token", "DAO", "Oráculo/Proveedor datos"]
PAISES = ["UE (MiCA/DORA)", "EE. UU.", "Suiza", "Singapur", "EAU"]

OBLIG = {
    "UE (MiCA/DORA)": {
        "CEX (exchange centralizado)": ["Registro como CASP", "KYC/AML", "Salvaguarda de fondos", "Resiliencia DORA"],
        "DEX (intercambio descentralizado)": ["Evaluación si opera como CASP", "Riesgo AML", "Transparencia del protocolo"],
        "Wallet/Custodia": ["Autorización CASP (custodia)", "Segregación de activos", "Controles DORA"],
        "Emisor de token": ["Whitepaper MiCA", "Gobernanza y reservas (ART/EMT)", "Transparencia a usuarios"],
        "DAO": ["Evaluar personalidad/representación", "Políticas AML si hay onboarding", "Transparencia de gobernanza"],
        "Oráculo/Proveedor datos": ["Acuerdos de servicio", "Seguridad y continuidad", "Auditoría y logs"],
    },
    "EE. UU.": {
        "CEX (exchange centralizado)": ["Registro MSB/FinCEN", "KYC/AML", "Revisar estado SEC/CFTC"],
        "DEX (intercambio descentralizado)": ["Análisis de broker/exchange", "Riesgo enforcement", "Transparencia del protocolo"],
        "Wallet/Custodia": ["Licencia estatal (p.ej., NYDFS)", "Seguridad custodial", "Segregación"],
        "Emisor de token": ["Howey test", "Exención/registro", "Divulgaciones"],
        "DAO": ["LLC/Unincorporated assoc.", "Fiscalidad y reporting", "AML si hay onboarding"],
        "Oráculo/Proveedor datos": ["SLA y responsabilidad", "Controles de integridad", "Auditorías"],
    },
    # (mapas resumidos para demo)
    "Suiza": {a: ["FINMA guidance", "AML/KYC", "Clasificación token (payment/utility/asset)"] for a in ACTORES},
    "Singapur": {a: ["Licencias MAS", "AML/KYC", "Tecnología y ciberseguridad"] for a in ACTORES},
    "EAU": {a: ["VARA/ADGM registro", "AML/KYC", "Requisitos de resiliencia"] for a in ACTORES},
}

def main(st=st):
    st.set_page_config(page_title="Mapa de cumplimiento", page_icon="📊", layout="wide")
    st.title("Mapa de cumplimiento — MiCA / DORA / AML (por actor y país)")

    col1, col2 = st.columns(2)
    with col1:
        actor = st.selectbox("Actor", ACTORES)
    with col2:
        pais = st.selectbox("Jurisdicción", PAISES)

    obligaciones = OBLIG.get(pais, {}).get(actor, ["(sin datos demo)"])
    df = pd.DataFrame({"Obligación": obligaciones})
    st.subheader("Obligaciones relevantes")
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("Checklist rápido")
    checks = {o: st.checkbox(o) for o in obligaciones}
    p_cumpl = round(100*sum(checks.values())/len(obligaciones)) if obligaciones else 0
    st.metric("Avance de cumplimiento", f"{p_cumpl}%")

    st.divider()
    txt = st.text_area("Síntesis (6–8 líneas): prioridades regulatorias y plan de acción.")
    md = f"""# S23 · Mapa de cumplimiento
- Fecha: {datetime.utcnow().isoformat()}Z
- Actor: {actor} · Jurisdicción: {pais}
## Obligaciones
{df.to_markdown(index=False)}
## Avance
- {p_cumpl}% checklist marcado
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s23_mapa_cumplimiento.md")

if __name__ == "__main__":
    main()
