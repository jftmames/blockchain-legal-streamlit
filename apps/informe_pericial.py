# apps/informe_pericial.py
import streamlit as st, hashlib, textwrap
from datetime import datetime, timezone
from io import BytesIO

def _utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def _hash_bytes(b:bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def main(st=st):
    st.set_page_config(page_title="Informe pericial", page_icon="📄", layout="wide")
    st.title("Generador de informe pericial (MD) — Estructura estándar")

    perito = st.text_input("Perito / Entidad", "Laboratorio Forense Digital UNIE")
    asunto = st.text_input("Asunto", "Verificación de integridad de evidencias blockchain")
    metodologia = st.text_area("Metodología", "Hash SHA-256, sellos temporales, verificación cruzada en explorador...")
    hallazgos = st.text_area("Hallazgos principales", "- Coincidencia de hash...\n- No se acredita autoría...")
    conclusiones = st.text_area("Conclusiones", "La evidencia muestra integridad, pero se requieren metadatos de autoría...")
    limitaciones = st.text_area("Limitaciones", "Muestras proporcionadas; no acceso a sistemas de origen; ausencia de logs firmados...")
    
    st.subheader("Adjuntar evidencias (opcional)")
    files = st.file_uploader("Sube ficheros para calcular hash (múltiples)", type=None, accept_multiple_files=True)
    evid_rows = []
    if files:
        for f in files:
            content = f.read()
            h = _hash_bytes(content)
            evid_rows.append(f"- `{f.name}` · {len(content)} bytes · SHA-256: `{h}`")
    evid_md = "\n".join(evid_rows) if evid_rows else "- (Sin adjuntos)"

    ts = _utc()
    md = f"""# INFORME PERICIAL
- Fecha: {ts}
- Perito/Entidad: {perito}
- Asunto: {asunto}

## Metodología
{metodologia}

## Hallazgos
{hallazgos}

## Evidencias adjuntas
{evid_md}

## Conclusiones
{conclusiones}

## Limitaciones
{limitaciones}
"""
    st.divider()
    st.subheader("Vista previa")
    st.markdown(md)

    st.download_button("Descargar informe (.md)", md.encode("utf-8"),
                       file_name=f"s18_informe_pericial_{ts[:10]}.md")

if __name__ == "__main__":
    main()
