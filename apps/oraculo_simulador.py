# apps/oraculo_simulador.py
import streamlit as st
from datetime import datetime

def main(st=st):
    st.set_page_config(page_title="Simulador de Oráculo", page_icon="🔮", layout="wide")
    st.title("Simulador de oráculo — Precio gatilla ejecución del contrato")

    col1, col2, col3 = st.columns(3)
    with col1:
        precio_real = st.number_input("Precio 'real' ETH/USD", 1.0, 100000.0, 2500.0, step=10.0)
    with col2:
        desviacion = st.slider("Desviación del oráculo (%)", -50, 50, 0, step=1)
    with col3:
        umbral = st.number_input("Umbral de ejecución (ETH/USD)", 1.0, 100000.0, 2600.0, step=10.0)

    precio_oraculo = precio_real * (1 + desviacion/100.0)

    c1, c2, c3 = st.columns(3)
    c1.metric("Precio real", f"{precio_real:,.2f} $")
    c2.metric("Precio del oráculo", f"{precio_oraculo:,.2f} $")
    c3.metric("Umbral", f"{umbral:,.2f} $")

    ejecuta_real = precio_real >= umbral
    ejecuta_orac = precio_oraculo >= umbral

    st.write("### Resultado de ejecución")
    colA, colB = st.columns(2)
    colA.info(f"**Según datos reales:** {'EJECUTA' if ejecuta_real else 'NO ejecuta'}")
    colB.warning(f"**Según oráculo:** {'EJECUTA' if ejecuta_orac else 'NO ejecuta'}")

    mismatch = ejecuta_real != ejecuta_orac
    if mismatch:
        st.error("⚠️ Divergencia real vs oráculo: posible ejecución errónea.")
    else:
        st.success("Coherencia: el oráculo coincide con la realidad asumida.")

    st.divider()
    st.subheader("Asignación de responsabilidad (escenario de error)")
    responsable = st.selectbox("Responsable principal si hay daño", [
        "Proveedor de oráculo (dato incorrecto)",
        "Desarrollador del contrato (diseño sin salvaguardas)",
        "Operador/DAO (gobernanza y supervisión)",
        "Nadie (riesgo asumido en las cláusulas)"
    ])
    salvaguardas = st.multiselect("Salvaguardas implementadas", [
        "Oráculos redundantes y agregación",
        "Umbrales con ventana temporal (TWAP)",
        "Pausable/Guardian (pausa de emergencia)",
        "Auditoría y pruebas con escenarios adversos"
    ])

    st.divider()
    st.subheader("Síntesis (6–8 líneas)")
    txt = st.text_area("Razona la asignación de responsabilidad y cómo habrías mitigado el error.")
    md = f"""# S16 · Simulador de Oráculo
- Fecha: {datetime.utcnow().isoformat()}Z
- Precio real: {precio_real:.2f} · Oráculo: {precio_oraculo:.2f} · Umbral: {umbral:.2f}
- Divergencia: {mismatch}
- Responsable estimado: {responsable}
- Salvaguardas: {', '.join(salvaguardas) if salvaguardas else '(ninguna)'}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s16_oraculo.md")

if __name__ == "__main__":
    main()
