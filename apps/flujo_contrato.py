# apps/flujo_contrato.py
import streamlit as st
from datetime import datetime

STATES = ["Borrador", "Oferta emitida", "Aceptado", "Pagado", "Cumplido", "Incumplido"]

def _now_iso():
    return datetime.utcnow().isoformat() + "Z"

def _event(label, meta=None):
    return {"ts": _now_iso(), "evento": label, "meta": meta or {}}

def main(st=st):
    st.set_page_config(page_title="Flujo contractual", page_icon="📜", layout="wide")
    st.title("Flujo contractual — Oferta → Aceptación → Pago → Cumplimiento")

    # Parámetros del “contrato”
    colA, colB, colC = st.columns(3)
    with colA:
        oferente = st.text_input("Parte A (oferente)", "Empresa Alfa")
        precio = st.number_input("Precio (EUR)", 0.0, 1e9, 1200.0, step=50.0)
    with colB:
        aceptante = st.text_input("Parte B (aceptante)", "Cliente Beta")
        plazo_dias = st.number_input("Plazo de entrega (días)", 0, 120, 7, step=1)
    with colC:
        penalizacion = st.number_input("Penalización por retraso (%)", 0.0, 100.0, 5.0, step=0.5)

    if "estado" not in st.session_state:
        st.session_state["estado"] = STATES[0]
        st.session_state["timeline"] = [_event("Contrato creado", {"estado": STATES[0]})]
        st.session_state["pagado"] = False
        st.session_state["entregado_en_plazo"] = True

    st.write("### Estado actual:", f"**{st.session_state['estado']}**")
    st.caption("Avanza con los botones en orden lógico. Puedes simular retrasos o impagos.")

    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("Emitir oferta"):
        st.session_state["estado"] = STATES[1]
        st.session_state["timeline"].append(_event("Oferta emitida", {"precio": precio}))
    if col2.button("Aceptar oferta"):
        st.session_state["estado"] = STATES[2]
        st.session_state["timeline"].append(_event("Oferta aceptada", {"parte": aceptante}))
    if col3.button("Registrar pago"):
        st.session_state["estado"] = STATES[3]
        st.session_state["pagado"] = True
        st.session_state["timeline"].append(_event("Pago recibido", {"monto": precio}))
    if col4.button("Marcar retraso"):
        st.session_state["entregado_en_plazo"] = False
        st.warning("Marcado retraso: se aplicará penalización si se cumple el contrato.")
        st.session_state["timeline"].append(_event("Retraso en entrega", {}))
    if col5.button("Cumplir/Resolver"):
        if st.session_state["pagado"]:
            st.session_state["estado"] = STATES[4]
            total = precio
            if not st.session_state["entregado_en_plazo"]:
                total *= (1 - penalizacion / 100.0)
            st.session_state["timeline"].append(_event("Contrato cumplido", {"importe_final": round(total, 2)}))
        else:
            st.session_state["estado"] = STATES[5]
            st.session_state["timeline"].append(_event("Incumplimiento (impago)", {}))

    st.divider()
    st.subheader("Línea de tiempo")
    for ev in st.session_state["timeline"]:
        st.markdown(f"- `{ev['ts']}` · **{ev['evento']}** — {ev['meta']}")

    st.divider()
    st.subheader("Síntesis (4–6 líneas)")
    sint = st.text_area("Traduce estos eventos técnicos a lenguaje jurídico (oferta, aceptación, precio, plazo, penalización).")

    md = f"""# S13 · Flujo contractual
- Fecha: {_now_iso()}
- Partes: {oferente} vs {aceptante}
- Precio: {precio} EUR · Plazo: {plazo_dias} días · Penalización: {penalizacion}%
- Estado final: {st.session_state['estado']}
## Timeline
""" + "\n".join([f"- {ev['ts']} · {ev['evento']} — {ev['meta']}" for ev in st.session_state["timeline"]]) + f"""

## Síntesis
{sint}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s13_flujo_contrato.md")

if __name__ == "__main__":
    main()
