# apps/sankey_trazabilidad.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import StringIO

EX_CSV = """origen,destino,unidades
Granja A,Procesadora X,100
Granja B,Procesadora X,80
Procesadora X,Distribuidor Y,170
Distribuidor Y,Supermercado Z,160
"""

def _build_sankey(df: pd.DataFrame):
    nodes = pd.unique(df[['origen','destino']].values.ravel('K')).tolist()
    idx = {n:i for i,n in enumerate(nodes)}
    source = df['origen'].map(idx).tolist()
    target = df['destino'].map(idx).tolist()
    value  = df['unidades'].tolist()
    link = dict(source=source, target=target, value=value)
    node = dict(label=nodes, pad=20, thickness=16)
    fig = go.Figure(data=[go.Sankey(link=link, node=node)])
    fig.update_layout(margin=dict(l=10,r=10,t=20,b=10), height=480)
    return fig

def _quiebras(df: pd.DataFrame):
    entradas = df.groupby('destino')['unidades'].sum()
    salidas  = df.groupby('origen')['unidades'].sum()
    all_nodes = sorted(set(entradas.index).union(set(salidas.index)))
    rows=[]
    for n in all_nodes:
        e = entradas.get(n, 0); s = salidas.get(n, 0)
        diff = s - e
        rows.append({"nodo": n, "entradas": e, "salidas": s, "diferencia(s-e)": diff, "alerta": "⚠️" if abs(diff)>0 else "OK"})
    return pd.DataFrame(rows)

def main(st=st):
    st.set_page_config(page_title="Trazabilidad (Sankey)", page_icon="🔎", layout="wide")
    st.title("Trazabilidad en supply chain — Diagrama Sankey")

    st.caption("Sube un CSV con columnas: origen,destino,unidades. O usa el ejemplo.")
    up = st.file_uploader("CSV de eventos", type=["csv"])
    if up:
        df = pd.read_csv(up)
    else:
        df = pd.read_csv(StringIO(EX_CSV))

    st.dataframe(df, use_container_width=True)
    fig = _build_sankey(df)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Control de coherencia")
    tabla = _quiebras(df)
    st.dataframe(tabla, use_container_width=True)
    if (tabla["alerta"]=="⚠️").any():
        st.warning("Hay incoherencias de unidades (posible pérdida/merma o error de registro).")

    st.divider()
    txt = st.text_area("Síntesis (5–7 líneas): valor probatorio de la trazabilidad y límites.")
    md = f"""# S10 · Sankey Trazabilidad
- Fecha: {datetime.utcnow().isoformat()}Z
- N. eventos: {len(df)}
- N. nodos: {len(pd.unique(df[['origen','destino']].values.ravel('K')))}
- Incoherencias: {int((tabla['alerta']=='⚠️').sum())}
## Síntesis
{txt}
"""
    st.download_button("Descargar evidencia (.md)", md.encode("utf-8"), "s10_sankey_trazabilidad.md")

if __name__ == "__main__":
    main()
