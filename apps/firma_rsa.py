# apps/firma_rsa.py
import streamlit as st
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from datetime import datetime

def _gen_keys(bits:int=2048):
    key = RSA.generate(bits)
    return key, key.publickey()

def _sign(msg:str, priv):
    h = SHA256.new(msg.encode("utf-8"))
    sig = pkcs1_15.new(priv).sign(h)
    return sig.hex()

def _verify(msg:str, sig_hex:str, pub):
    try:
        h = SHA256.new(msg.encode("utf-8"))
        pkcs1_15.new(pub).verify(h, bytes.fromhex(sig_hex))
        return True
    except Exception:
        return False

def main(st=st):
    st.set_page_config(page_title="Firma RSA", page_icon="✍️", layout="wide")
    st.title("Firma y verificación RSA (demo jurídica)")

    bits = st.selectbox("Tamaño de clave", [1024, 2048, 3072, 4096], index=1)
    if st.button("Generar par de claves"):
        priv, pub = _gen_keys(bits)
        st.session_state["priv_pem"] = priv.export_key().decode()
        st.session_state["pub_pem"] = pub.export_key().decode()

    priv_pem = st.session_state.get("priv_pem")
    pub_pem = st.session_state.get("pub_pem")

    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Clave privada (PEM)", priv_pem or "", height=180)
    with col2:
        st.text_area("Clave pública (PEM)", pub_pem or "", height=180)

    mensaje = st.text_area("Mensaje a firmar", "Reconozco haber recibido el bien en perfecto estado.")
    if st.button("Firmar mensaje"):
        if not priv_pem:
            st.error("Genera o pega una clave privada.")
        else:
            priv = RSA.import_key(priv_pem)
            firma = _sign(mensaje, priv)
            st.code(firma)
            st.session_state["firma_hex"] = firma

    firma_hex = st.text_input("Firma (hex)", st.session_state.get("firma_hex", ""))
    if st.button("Verificar firma"):
        if not pub_pem or not firma_hex:
            st.error("Falta clave pública o firma.")
        else:
            pub = RSA.import_key(pub_pem)
            ok = _verify(mensaje, firma_hex, pub)
            st.success("Firma VÁLIDA") if ok else st.error("Firma NO válida")

    st.divider()
    st.subheader("Síntesis (4–6 líneas)")
    txt = st.text_area("Diferencia jurídica entre hash, firma y sello de tiempo.")
    md = f"""# S07 · Firma RSA
- Fecha: {datetime.utcnow().isoformat()}Z
- Clave: {bits} bits
- Mensaje firmado: {len(mensaje)} chars
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"),
                       file_name="s07_firma_rsa.md")

if __name__ == "__main__":
    main()
