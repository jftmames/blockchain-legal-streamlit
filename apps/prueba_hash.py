# apps/prueba_hash.py
import streamlit as st, hashlib, difflib
from datetime import datetime

def _hash(txt:str) -> str:
    return hashlib.sha256((txt or "").encode("utf-8")).hexdigest()

def _diff(a:str, b:str) -> str:
    a_lines = (a or "").splitlines(keepends=False)
    b_lines = (b or "").splitlines(keepends=False)
    d = difflib.unified_diff(a_lines, b_lines, fromfile="A", tofile="B", lineterm="")
    return "\n".join(d)

def main(st=st):
    st.set_page_config(page_title="Prueba Hash (integridad)", page_icon="🧪", layout="wide")
    st.title("Prueba de integridad mediante hash — Documento A vs Documento B")

    col1, col2 = st.columns(2)
    with col1:
        docA = st.text_area("Documento A (original)", "Acta original del contrato...\nCláusula 1...")
    with col2:
        docB = st.text_area("Documento B (comparado)", "Acta original del contrato...\nCláusula 1...")

    hA, hB = _hash(docA), _hash(docB)

    c1, c2, c3 = st.columns(3)
    c1.code(f"SHA-256 A: {hA}")
    c2.code(f"SHA-256 B: {hB}")
    c3.metric("¿Coinciden?", "Sí" if hA == hB else "No")

    st.subheader("Diferencias (unified diff)")
    diff_txt = _diff(docA, docB)
    st.code(diff_txt or "(No hay diferencias de líneas)")

    st.info("El hash acredita integridad de un contenido exacto en un momento dado, pero **no** acredita autoría ni contenido semántico.")

    st.divider()
    st.subheader("Síntesis (4–6 líneas)")
    sint = st.text_area("Delimita: qué prueba el hash, qué NO prueba y qué evidencia adicional pedirías en juicio.")
    md = f"""# S17 · Prueba Hash
- Fecha: {datetime.utcnow().isoformat()}Z
- Hash A: {hA}
- Hash B: {hB}
- Coinciden: {hA==hB}
## Diff
{diff_txt or '(Sin cambios)'}
## Síntesis
{sint}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s17_prueba_hash.md")

if __name__ == "__main__":
    main()
