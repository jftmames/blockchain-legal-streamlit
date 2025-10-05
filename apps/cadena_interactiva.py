# apps/cadena_interactiva.py
import streamlit as st, hashlib, time
import pandas as pd

def _mine_block(index:int, data:str, prev_hash:str, difficulty:int=2, max_steps:int=50_000):
    prefix = "0"*difficulty
    nonce = 0
    while nonce < max_steps:
        raw = f"{index}|{data}|{prev_hash}|{nonce}"
        h = hashlib.sha256(raw.encode()).hexdigest()
        if h.startswith(prefix):
            return h, nonce
        nonce += 1
        if nonce % 1000 == 0:
            time.sleep(0.0005)  # no bloquear UI
    return None, None

def main(st=st):
    st.set_page_config(page_title="Cadena interactiva", page_icon="🔗", layout="wide")
    st.title("Cadena de 5 bloques — encadenamiento y ruptura")

    dif = st.slider("Dificultad (ceros iniciales del hash)", 1, 3, 2)
    datos = []
    prev = "GENESIS"
    tabla = []
    for i in range(5):
        d = st.text_input(f"Bloque {i+1} · datos", f"Transacción {i+1}")
        h, n = _mine_block(i+1, d, prev, difficulty=dif)
        if h is None:
            st.error("No se pudo minar el bloque dentro del límite de pasos. Baja la dificultad.")
            return
        tabla.append({"#": i+1, "prev_hash": prev, "hash": h, "nonce": n, "datos": d})
        prev = h

    df = pd.DataFrame(tabla)
    st.dataframe(df, use_container_width=True)
    st.info("Modifica cualquier dato y observa cómo cambian los bloques posteriores (efecto dominó).")

    st.divider()
    st.subheader("Comprobación de integridad")
    idx = st.number_input("Bloque a alterar", 1, 5, 3)
    nuevo = st.text_input("Nuevo dato", "Pago modificado 300€")
    if st.button("Probar ruptura"):
        # recomputar desde idx
        prev = df.loc[idx-2, "hash"] if idx > 1 else "GENESIS"
        h, n = _mine_block(idx, nuevo, prev, difficulty=dif)
        st.write("Nuevo hash en bloque alterado:", h)
        st.warning("La alteración obliga a recomputar a partir de este bloque para mantener consistencia.")

    st.divider()
    sint = st.text_area("Síntesis (5–7 líneas): ¿Qué hace verificable la cadena para terceros independientes?")
    st.download_button("Descargar síntesis (.md)", f"# S03 Cadena\n\n{sint}".encode("utf-8"),
                       file_name="s03_sintesis.md", mime="text/markdown")

if __name__ == "__main__":
    main()
