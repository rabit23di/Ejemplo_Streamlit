# 🚖 Uber SQL Analytics App

Una aplicación web interactiva construida con **Streamlit** para visualizar y analizar el dataset de Uber extraído de una base de datos SQL.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## 📋 Características

- **Descarga Automática:** Utiliza `kagglehub` para obtener el dataset automáticamente al iniciar.
- **Dashboard Interactivo:** Tarjetas con KPIs (Key Performance Indicators).
- **Visualización:** Gráficos de líneas y barras con Plotly.
- **Filtros:** Sidebar para filtrar por fechas y categorías.
- **Arquitectura:** Estructura modular separando lógica de datos y vista.

## 🚀 Instalación y Ejecución

1. **Clonar o crear la estructura:**
   ```bash
   mkdir -p uber_analytics_app/{pages,data,utils}
   cd uber_analytics_app