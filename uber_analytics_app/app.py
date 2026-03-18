import streamlit as st

st.set_page_config(page_title="Uber Analytics", page_icon="🚖", layout="wide")

st.title("🚖 Uber Data Analytics")
st.markdown("""
    ### Bienvenido al Dashboard de Análisis de Viajes
    Esta aplicación visualiza datos extraídos de una base de datos SQL de Uber.
    Utiliza **Streamlit**, **Pandas** y **Plotly** para ofrecer insights interactivos.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 **Visualización**\nGráficos interactivos de viajes por hora y tipo de vehículo.")
with col2:
    st.success("🔍 **Filtros**\nFiltra por rango de fechas y tipo de servicio.")
with col3:
    st.warning("⚡ **Rendimiento**\nDatos cargados desde SQLite optimizados con caché.")

st.divider()

if st.button("Ir al Dashboard", type="primary", use_container_width=True):
    st.switch_page("pages/dashboard.py")