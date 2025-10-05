from datetime import datetime

def stamp_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"

def md_download_button(st, filename:str, content:str, label="Descargar (.md)"):
    st.download_button(label, content.encode("utf-8"), file_name=filename, mime="text/markdown")
