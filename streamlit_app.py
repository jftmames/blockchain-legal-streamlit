# streamlit_app.py
import streamlit as st
import importlib
from urllib.parse import urlencode

st.set_page_config(page_title="Blockchain & Derecho · Portal docente", page_icon="⚖️", layout="wide")

st.title("Portal docente · Blockchain: fundamentos técnicos y problemática jurídica")
st.caption("Selecciona semana y sesión para cargar la mini-app correspondiente.")

# ------------------------------
# Mapa Semana → Sesión → módulo
# ------------------------------
MAP = {
    "Semana 1": {
        "S1 · Hash Visual": "apps.hash_visual_demo",
        "S2 · Sello de tiempo": "apps.sello_tiempo",
    },
    "Semana 2": {
        "S3 · Cadena interactiva (5 bloques)": "apps.cadena_interactiva",
        "S4 · PoW energía": "apps.pow_energia",
    },
    "Semana 3": {
        "S5 · Comparador PoW/PoS/BFT (radar)": "apps.consenso_radar",
        "S6 · Explorador BIP sintético": "apps.bip_explorador",
    },
    "Semana 4": {
        "S7 · Firma y verificación RSA": "apps.firma_rsa",
        "S8 · Matriz RGPD–Trazabilidad": "apps.rgpd_matriz",
    },
    "Semana 5": {
        "S9 · Selector de red": "apps.selector_red",
        "S10 · Trazabilidad Supply Chain (Sankey)": "apps.sankey_trazabilidad",
    },
    "Semana 6": {
        "S11 · Licitación trazable (hash + sello)": "apps.licitacion_trazable",
        "S12 · Mapa de riesgos (heatmap)": "apps.mapa_riesgos",
    },
    "Semana 7": {
        "S13 · Flujo oferta–aceptación–pago": "apps.flujo_contrato",
        "S14 · Comparador de gas + Etherscan": "apps.gas_comparador",
    },
    "Semana 8": {
        "S15 · Checklist de validez (SC)": "apps.checklist_validez_sc",
        "S16 · Simulador de oráculo": "apps.oraculo_simulador",
    },
    "Semana 9": {
        "S17 · Prueba hash (integridad)": "apps.prueba_hash",
        "S18 · Informe pericial (MD/PDF)": "apps.informe_pericial",
    },
    "Semana 10": {
        "S19 · Matriz RGPD (roles/bases)": "apps.rgpd_roles_bases",
        "S20 · Evaluador de anonimización": "apps.anonimizador_eval",
    },
    "Semana 11": {
        "S21 · Ficha legal de token/NFT": "apps.ficha_token",
        "S22 · Arbitraje DAO (Kleros/Aragon)": "apps.arbitraje_dao",
    },
    "Semana 12": {
        "S23 · Mapa de cumplimiento (MiCA/DORA/AML)": "apps.mapa_cumplimiento",
        "S24 · Simulador de incidentes": "apps.incidentes_simulador",
    },
    "Semana 13": {
        "S25 · Semáforo regulatorio global": "apps.semaforo_regulatorio",
        "S26 · Explorador de licencias (OSS)": "apps.explorador_licencias",
        "S26bis · Pseudocódigo LegalTech": "apps.pseudocodigo_legaltech",
    },
    "Semana 14": {
        "S27 · Canvas de proyecto": "apps.canvas_proyecto",
        "S28 · Rúbrica EEE (peer review)": "apps.rubrica_eee",
    },
    "Semana 15": {
        "S29 · Checklist de defensa": "apps.checklist_defensa",
        "S30 · Autoevaluación radar RA": "apps.auto_radar_ra",
    },
}

# ------------------------------
# Sidebar: navegación y deep-link
# ------------------------------
with st.sidebar:
    st.header("Navegación")
    semanas = list(MAP.keys())
    sem_idx = st.session_state.get("sem_idx", 0)
    sem = st.selectbox("Semana", semanas, index=sem_idx)
    sesiones = list(MAP[sem].keys())
    ses_idx = st.session_state.get("ses_idx", 0)
    ses = st.selectbox("Sesión", sesiones, index=ses_idx)

    # Botón para copiar URL con parámetros (deep-link)
    params = urlencode({"week": sem, "session": ses})
    deeplink = f"{st.get_option('server.baseUrlPath') or ''}?{params}"
    st.caption("Deep-link a la vista actual (añadido a la URL):")
    st.code(deeplink or "?"+params, language="bash")

# Cargar módulo seleccionado
mod_name = MAP[sem][ses]
st.divider()
st.subheader(ses)

def _run_module(mod_path: str):
    """Carga el módulo y ejecuta main(st) si existe; si no, hace fallback al código top-level."""
    try:
        mod = importlib.import_module(mod_path)
        if hasattr(mod, "main"):
            mod.main(st)
        else:
            # Fallback: ejecutar el archivo directamente (top-level code)
            exec(open(mod.__file__, "r", encoding="utf-8").read(), {})
    except ModuleNotFoundError as e:
        st.error(f"Mini-app no encontrada: {mod_path}\n{e}")
    except Exception as e:
        st.exception(e)

_run_module(mod_name)

# ------------------------------
# Leer parámetros para deep-link (si el usuario entra con ?week=…&session=…)
# ------------------------------
query = st.query_params
if "week" in query and "session" in query:
    w = query.get("week")
    s = query.get("session")
    if isinstance(w, list): w = w[0]
    if isinstance(s, list): s = s[0]
    if w in MAP and s in MAP[w]:
        # Actualiza selección en sesión para que queden persistentes al recargar
        st.session_state["sem_idx"] = list(MAP.keys()).index(w)
        st.session_state["ses_idx"] = list(MAP[w].keys()).index(s)
