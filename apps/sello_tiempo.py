# apps/sello_tiempo.py
import streamlit as st, hashlib, json
from datetime import datetime, timezone

def _utcnow_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def main(st=st):
    st.set_page_config(page_title="Sello de tiempo", page_icon="🕒", layout="wide")
    st.title("Sello de tiempo simulado — Hash + Timestamp (RFC 3161-like)")

    texto = st.text_area("Texto / Acta / Evidencia", "Acta de reunión del 05/10/2025 ...", height=160)
    sujeto = st.text_input("Identificador (opt.)", "Oficina 12 · Expediente 2025/001")
    if st.button("Generar sello"):
        payload = {"subject": sujeto, "text": texto, "created_at": _utcnow_iso()}
        payload_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        digest = hashlib.sha256(payload_bytes).hexdigest()

        st.success("Sello generado")
        st.code(json.dumps({"hash": digest, "timestamp": payload["created_at"]}, ensure_ascii=False, indent=2))
        st.caption("Este sello prueba integridad y marca temporal, no autoría. Úsalo como apoyo probatorio.")

        # Descarga JSON de evidencia
        ev_json = json.dumps({"subject": sujeto, "hash": digest, "timestamp": payload["created_at"]}, ensure_ascii=False, indent=2)
        st.download_button("Descargar evidencia (.json)", data=ev_json, file_name="sello_tiempo.json", mime="application/json")

    st.divider()
    st.subheader("Síntesis (5–7 líneas)")
    sint = st.text_area("Diferencias entre: firma electrónica, sello de tiempo y hash.")
    st.download_button("Descargar síntesis (.md)", data=f"# Sello de tiempo\n\n{sint}".encode("utf-8"),
                       file_name="s02_sintesis.md", mime="text/markdown")

if __name__ == "__main__":
    main()
