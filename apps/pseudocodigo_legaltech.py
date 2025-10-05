# apps/pseudocodigo_legaltech.py
import streamlit as st
import re
from datetime import datetime

AMBIG = ["pronto", "razonable", "significativo", "adecuado", "o equivalente", "lo antes posible"]

def _extraer_numeros(texto):
    nums = re.findall(r"\d+(\.\d+)?", texto)
    return nums

def _flag_ambig(texto):
    f = [w for w in AMBIG if re.search(rf"\b{re.escape(w)}\b", texto, flags=re.I)]
    return f

def _to_pseudocode(texto):
    t = texto.lower()
    # Reglas muy simples (demo)
    cond = []
    act = []
    if "si" in t or "en caso de" in t:
        # segmentación naive
        partes = re.split(r"\bsi\b|en caso de", t, flags=re.I)
        if len(partes) >= 2:
            condicion = partes[1].split(",")[0].strip()
            cond.append(condicion)
    if "pagar" in t:
        act.append("pagar()")
    if "penaliz" in t:
        nums = _extraer_numeros(t)
        porc = next((n for n in nums if float(n) <= 100), "X")
        act.append(f"aplicar_penalizacion({porc}%)")
    if "resolver el contrato" in t or "resolución" in t:
        act.append("resolver_contrato()")
    if "entrega" in t and "días" in t:
        dias = next(iter(_extraer_numeros(t)), "N")
        act.append(f"entregar_en({dias}_dias)")
    pc = "if (" + " and ".join(cond or ["CONDICION"]) + "):\n    " + "\n    ".join(act or ["ACCION"])
    return pc

def main(st=st):
    st.set_page_config(page_title="Pseudocódigo LegalTech", page_icon="🧠", layout="wide")
    st.title("Generador de pseudocódigo a partir de cláusulas")

    clausula = st.text_area("Cláusula legal", "Si el pago se retrasa más de 7 días, se aplicará una penalización del 5% y podrá resolverse el contrato.")
    pseudocode = _to_pseudocode(clausula)
    flags = _flag_ambig(clausula)

    st.subheader("Pseudocódigo (borrador)")
    st.code(pseudocode, language="python")

    if flags:
        st.warning("Ambigüedades detectadas: " + ", ".join(flags))
    else:
        st.success("No se detectaron ambigüedades comunes.")

    st.divider()
    st.subheader("Síntesis (4–6 líneas)")
    txt = st.text_area("Indica qué campos faltan para una automatización segura (definiciones, umbrales, oráculos, fallback…).")
    md = f"""# S26bis · Pseudocódigo LegalTech
- Fecha: {datetime.utcnow().isoformat()}Z
## Cláusula
{clausula}
## Pseudocódigo (borrador)
