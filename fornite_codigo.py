import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fortnite Stats", layout="wide")
st.title("Análisis de Fortnite: Modo Solo")

# 1. Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Fortnite_players_stats.csv")

try:
    df = load_data()

    # --- DISEÑO DE COLUMNAS (Gráfico chico a la izq, Tabla a la der) ---
    col_izquierda, col_derecha = st.columns([1, 2]) 

    # --- COLUMNA IZQUIERDA: EL GRÁFICO PEQUEÑO ---
    with col_izquierda:
        st.subheader("Minutos vs Puntaje")
        
        # Datos y Tendencia
        x = df['Solo minutesPlayed']
        y = df['Solo score']
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # Gráfico compacto
        fig, ax = plt.subplots(figsize=(5, 3.5)) 
        ax.scatter(x, y, alpha=0.5, c='#1f77b4', s=5)
        ax.plot(x, p(x), "r--", linewidth=1, label='Tendencia')

        # Estilos
        ax.set_title("Relación Tiempo/Puntaje", fontsize=9)
        ax.set_xlabel("Minutos", fontsize=7)
        ax.set_ylabel("Puntaje", fontsize=7)
        ax.tick_params(labelsize=6)
        ax.legend(fontsize=6)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig, use_container_width=True)
        
        corr = df['Solo minutesPlayed'].corr(df['Solo score'])
        st.caption(f"Correlación: {corr:.2f}")

    # --- COLUMNA DERECHA: TABLA FILTRADA ---
    with col_derecha:
        st.subheader("Datos del Modo Solitario")
        st.write("Explora las estadísticas detalladas de los jugadores.")

        # --- AQUÍ ESTÁ EL CAMBIO PARA FILTRAR COLUMNAS ---
        # 1. Creamos una lista con 'Player' y todas las columnas que tengan "Solo" en el nombre
        df_filtrado = df[['Player', 'Solo score', 'Solo minutesPlayed']]

        # Ordenamos por puntaje (de mayor a menor) para que se vea como un ranking
        df_filtrado = df_filtrado.sort_values(by='Solo score', ascending=False)

        # hide_index=True quita la columna de números 0,1,2... de la izquierda para que se vea más limpio
        st.dataframe(df_filtrado, height=400, hide_index=True)
except FileNotFoundError:
    st.error("No encuentro el archivo 'Fortnite_players_stats.csv'.")

#--------------grafico de horas x partidas ganadas --------------#


# 2. Procesar datos: Ordenar por 'Solo minutesPlayed' de mayor a menor
df_sorted = df.sort_values(by='Solo minutesPlayed', ascending=False)

# Widget para controlar cuántos jugadores mostrar (para que el gráfico sea legible)
st.sidebar.header("Configuración del Gráfico")
top_n = st.sidebar.slider("Cantidad de jugadores a mostrar (Top N)", min_value=10, max_value=200, value=50)

# Filtramos los top N jugadores según la selección
df_chart = df_sorted.head(top_n).reset_index(drop=True)

# 3. Crear el gráfico con Matplotlib
fig, ax1 = plt.subplots(figsize=(12, 6))

# Eje Y izquierdo: Solo Minutes Played (Línea Azul)
color1 = 'tab:blue'
ax1.set_xlabel('Jugador')
ax1.set_ylabel('Minutos Jugados (Solo)', color=color1, fontsize=12)
ax1.plot(df_chart.index, df_chart['Solo minutesPlayed'], color=color1, marker='o', markersize=4, label='Minutos Jugados')
ax1.tick_params(axis='y', labelcolor=color1)

# Configurar las etiquetas del eje X para mostrar los nombres de los jugadores
ax1.set_xticks(df_chart.index)
ax1.set_xticklabels(df_chart['Player'], rotation=90, fontsize=8)

# Eje Y derecho: Solo Top 1 (Línea Roja)
ax2 = ax1.twinx()  
color2 = 'tab:red'
ax2.set_ylabel('Top 1 (Victorias)', color=color2, fontsize=12)
ax2.plot(df_chart.index, df_chart['Solo top1'], color=color2, linestyle='--', marker='x', markersize=4, label='Top 1')
ax2.tick_params(axis='y', labelcolor=color2)

# Título y ajustes
plt.title(f'Relacion: Minutos Jugados vs Victorias (Top {top_n} jugadores)', fontsize=14)
fig.tight_layout()

# 4. Mostrar en Streamlit
st.pyplot(fig)

# Mostrar tabla de datos opcional
if st.checkbox("Mostrar datos en tabla"):
	st.dataframe(df_chart[['Player', 'Solo minutesPlayed', 'Solo top1']])
