import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Asegurar que podemos importar utils desde la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_loader import load_data

st.set_page_config(page_title="Dashboard Uber", page_icon="📈", layout="wide")

# Cargar datos
data = load_data()

if data is None:
    st.stop()

# Asumimos que la tabla principal de viajes se llama 'trips' o similar. 
# Ajusta el nombre según el dataset real de Kaggle (ej: 'trips', 'rides')
# Para este ejemplo, buscaremos la primera tabla que tenga más de 100 filas
main_table_name = None
for name, df in data.items():
    if len(df) > 100:
        main_table_name = name
        break

if not main_table_name:
    st.error("No se encontró una tabla de datos principal.")
    st.stop()

df = data[main_table_name]

# --- Preprocesamiento Básico ---
# Intentar detectar columnas de fecha y numéricas automáticamente
date_col = None
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower():
        date_col = col
        df[col] = pd.to_datetime(df[col], errors='coerce')
        break

# Si no hay columna de fecha explícita, usamos el índice o la primera columna como fallback
if date_col is None:
    date_col = df.columns[0] 

# --- Sidebar Filtros ---
st.sidebar.header("🔍 Filtros")

# Filtro de Fecha (si se detectó)
if pd.api.types.is_datetime64_any_dtype(df[date_col]):
    min_date = df[date_col].min()
    max_date = df[date_col].max()
    selected_dates = st.sidebar.date_input(
        "Rango de Fechas",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(selected_dates) == 2:
        df = df[(df[date_col].dt.date >= selected_dates[0]) & (df[date_col].dt.date <= selected_dates[1])]
else:
    st.sidebar.warning("No se detectó columna de fecha para filtrar.")

# Filtro Categórico (si existe)
cat_col = None
for col in df.select_dtypes(include=['object', 'category']).columns:
    if df[col].nunique() < 20: # Si tiene pocos valores únicos, es buen candidato para filtro
        cat_col = col
        break

if cat_col:
    unique_vals = df[cat_col].unique()
    selected_cat = st.sidebar.multiselect(f"Filtrar por {cat_col}", unique_vals, default=unique_vals)
    df = df[df[cat_col].isin(selected_cat)]

# --- KPI Cards ---
st.title(f"📊 Dashboard: {main_table_name}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Registros", f"{len(df):,}")
with col2:
    # Intentar sumar una columna numérica (ej: fare_amount, distance)
    num_col = None
    for c in df.select_dtypes(include=['float', 'int']).columns:
        if c != 'id':
            num_col = c
            break
    total_val = df[num_col].sum() if num_col else 0
    st.metric(f"Total {num_col or 'Valor'}", f"{total_val:,.2f}")
with col3:
    st.metric("Columnas", df.shape[1])
with col4:
    st.metric("Filtras Activos", "Sí" if cat_col or pd.api.types.is_datetime64_any_dtype(df[date_col]) else "No")

st.divider()

# --- Gráficos ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Distribución Temporal")
    if pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df_grouped = df.groupby(df[date_col].dt.date).size().reset_index(name='count')
        fig_line = px.line(df_grouped, x=date_col, y='count', title="Viajes por Día", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No hay datos de tiempo para graficar línea temporal.")

with c2:
    st.subheader("Distribución por Categoría")
    if cat_col:
        fig_bar = px.bar(df, x=cat_col, title=f"Distribución por {cat_col}", color=cat_col)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        # Gráfico alternativo si no hay categoría
        num_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
        if len(num_cols) > 1:
            fig_scatter = px.scatter(df, x=num_cols[0], y=num_cols[1], title=f"Relación {num_cols[0]} vs {num_cols[1]}")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No hay suficientes datos numéricos o categóricos para gráficos secundarios.")

# --- Tabla de Datos ---
with st.expander("Ver Datos Crudos"):
    st.dataframe(df)