# apps/arbitraje_dao.py
import streamlit as st
import random
from statistics import mean
from datetime import datetime

CAUSAS = [
    "Incumplimiento de entrega", "Pago no recibido", "Bug en smart contract", "Oráculo defectuoso", "Uso indebido de NFT"
]
REGLAS = ["Mayoría simple", "Mayoría cualificada (2/3)", "Quórum 70%"]

def _dao_vote(n_jurados:int, sesgo:float, dispersion:float):
    # sesgo en [0,1]: prob. base de votar A (demandante). dispersion aumenta variabilidad local.
    votos = []
    for _ in range(n_jurados):
        p = min(1, max(0, random.gauss(sesgo, dispersion)))
        votos.append(1 if random.random() < p else 0)  # 1=A, 0=B
    return votos

def _decision(votos, regla:str):
    a = sum(votos); b = len(votos) - a
    if regla == "Mayoría cualificada (2/3)":
        return "A" if a >= (2*len(votos)/3) else "B"
    return "A" if a > b else "B"

def main(st=st):
    st.set_page_config(page_title="Arbitraje DAO", page_icon="⚖️", layout="wide")
    st.title("Simulador de arbitraje DAO vs institucional")

    col1, col2, col3 = st.columns(3)
    with col1:
        causa = st.selectbox("Causa", CAUSAS)
        n_jurados = st.slider("Jurados (stakeadores)", 3, 101, 21, step=2)
    with col2:
        regla = st.selectbox("Reglas de decisión DAO", REGLAS)
        sesgo = st.slider("Sesgo prob. pro-Demandante (A)", 0.0, 1.0, 0.55, step=0.01)
    with col3:
        dispersion = st.slider("Dispersion de opiniones (σ)", 0.00, 0.50, 0.15, step=0.01)
        stake_min = st.number_input("Stake mínimo por jurado (token)", 0.0, 1e9, 100.0, step=10.0)

    votos = _dao_vote(n_jurados, sesgo, dispersion)
    ganador_dao = _decision(votos, regla)
    pct_A = 100*sum(votos)/len(votos)

    st.subheader("Resultado DAO")
    st.metric("Ganador (DAO)", "Demandante (A)" if ganador_dao=="A" else "Demandado (B)")
    st.progress(int(pct_A))
    st.caption(f"Votos por A: {pct_A:.1f}%")

    st.divider()
    st.subheader("Comparativa con arbitraje institucional")
    laudos = st.selectbox("Número de árbitros", [1, 3])
    regla_inst = st.selectbox("Regla institucional", ["Mayoría simple", "Unánime"])
    # Para el institucional simulamos menos ruido
    votos_inst = _dao_vote(laudos, sesgo, dispersion/2)
    if regla_inst == "Unánime":
        ganador_inst = "A" if sum(votos_inst)==laudos else "B"
    else:
        ganador_inst = "A" if sum(votos_inst) > laudos/2 else "B"

    colA, colB = st.columns(2)
    colA.metric("Ganador (Institucional)", "Demandante (A)" if ganador_inst=="A" else "Demandado (B)")
    colB.write(f"Votos institucionales: {sum(votos_inst)}/{laudos} a favor de A")

    divergencia = ganador_dao != ganador_inst
    if divergencia:
        st.warning("💡 Divergencia DAO vs Institucional: fundamento y ejecutabilidad podrían diferir.")
    else:
        st.success("Coherencia entre ambos modelos en este escenario.")

    st.divider()
    st.subheader("Síntesis (6–8 líneas)")
    txt = st.text_area("Analiza legitimidad, sesgos por stake y ejecutabilidad transfronteriza de laudo DAO.")
    md = f"""# S22 · Arbitraje DAO
- Fecha: {datetime.utcnow().isoformat()}Z
- Causa: {causa}
- DAO: jurados={n_jurados}, regla={regla}, sesgo={sesgo}, σ={dispersion}, stake_min={stake_min}
- Resultado DAO: {'A' if ganador_dao=='A' else 'B'} ({pct_A:.1f}% votos A)
- Resultado Institucional: {'A' if ganador_inst=='A' else 'B'} (laudos={laudos}, regla={regla_inst})
- Divergencia: {divergencia}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s22_arbitraje_dao.md")

if __name__ == "__main__":
    main()
