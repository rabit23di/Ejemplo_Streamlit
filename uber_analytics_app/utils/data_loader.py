import streamlit as st
import pandas as pd
import sqlite3
import kagglehub
import os

# Ruta base
DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "uber.db") # Asumiendo que el archivo se llama uber.db

@st.cache_data
def load_data():
    """Descarga el dataset y carga los datos desde SQLite."""
    
    # 1. Descargar dataset si no existe la carpeta o el archivo
    if not os.path.exists(DATA_DIR) or not os.path.exists(DB_PATH):
        with st.spinner("Descargando dataset de Kaggle..."):
            try:
                path = kagglehub.dataset_download("rockyt07/uber-sql-database")
                # Mover o copiar el archivo .db a nuestra carpeta data si es necesario
                # Kagglehub descarga en una ruta temporal, buscamos el archivo .db
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(".db"):
                            src = os.path.join(root, file)
                            # Copiamos a nuestra carpeta local para persistencia
                            import shutil
                            os.makedirs(DATA_DIR, exist_ok=True)
                            shutil.copy(src, DB_PATH)
                            break
            except Exception as e:
                st.error(f"Error descargando: {e}")
                return None

    # 2. Conectar a SQLite y cargar tablas
    try:
        conn = sqlite3.connect(DB_PATH)
        # Leemos todas las tablas disponibles
        tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
        
        data_dict = {}
        for table in tables['name']:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            data_dict[table] = df
            
        conn.close()
        return data_dict
    except Exception as e:
        st.error(f"Error leyendo DB: {e}")
        return None