# apps/licitacion_trazable.py
import streamlit as st, hashlib, json
from datetime import datetime, timezone

def _utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def main(st=st):
    st.set_page_config(page_title="Licitación trazable", page_icon="📑", layout="wide")
    st.title("Licitación trazable — Sello de integridad de expediente")

    exp = st.text_input("ID Expediente", "LC-2025-001")
    org = st.text_input("Órgano de contratación", "Ayuntamiento de Demo")
    resumen = st.text_area("Resumen del expediente", "Contrato de suministro de equipos...")
    base_pdf = st.file_uploader("Anexo (PDF) opcional", type=["pdf"])

    contenido = resumen
    if base_pdf:
        contenido += f"|FICHERO:{base_pdf.name}|TAM:{base_pdf.size}"

    if st.button("Generar sello de expediente"):
        payload = {"expediente": exp, "organo": org, "created_at": _utc()}
        digest = hashlib.sha256((contenido or "").encode("utf-8")).hexdigest()
        evidencia = {"hash": digest, **payload}
        st.success("Sello generado")
        st.code(json.dumps(evidencia, ensure_ascii=False, indent=2))
        st.caption("Prueba integridad y momento temporal. No acredita autoría por sí misma.")

        st.download_button("Descargar evidencia (.json)",
                           data=json.dumps(evidencia, ensure_ascii=False, indent=2),
                           file_name=f"s11_{exp}_sello.json", mime="application/json")

    st.divider()
    txt = st.text_area("Síntesis (4–6 líneas): utilidad y límites en contratación pública.")
    st.download_button("Descargar síntesis (.md)", f"# S11 · Licitación trazable\n\n{txt}".encode("utf-8"),
                       "s11_licitacion_trazable.md")

if __name__ == "__main__":
    main()
