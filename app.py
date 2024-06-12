import streamlit as st
import pandas as pd
from game_advanced import run_game
import altair as alt

# Configuración de la página
st.set_page_config(page_title="CESDE Medio Ambiente", layout="wide")

# Título y Descripción
st.title("Juego Interactivo de Medio Ambiente - CESDE")
st.markdown("Recolecta la mayor cantidad de basura en 30 segundos.")

# Leer registros anteriores de puntajes
scores_file = "game_scores.csv"
scores_df = pd.read_csv(scores_file) if st.session_state.get('scores_df') is None else st.session_state['scores_df']

# Input para nombres de jugadores
player1_name = st.text_input("Nombre del Jugador 1", "")
player2_name = st.text_input("Nombre del Jugador 2", "")

# Botón de inicio del juego
if st.button("Start"):
    if player1_name and player2_name:
        # Ejecutar el juego y obtener los puntajes
        scores = run_game(player1_name, player2_name, scores_df, scores_file)
        st.success("¡El juego ha terminado!")
        
        # Actualizar DataFrame con nuevos puntajes
        new_scores_df = pd.DataFrame(scores, columns=['Jugador', 'Puntaje'])
        scores_df = pd.concat([scores_df, new_scores_df], ignore_index=True)
        scores_df.drop_duplicates(subset=['Jugador'], keep='first', inplace=True)
        
        # Guardar registros en archivo CSV
        scores_df.to_csv(scores_file, index=False)
        
        # Mostrar puntajes si el juego ha terminado
        st.subheader("Tabla de Puntajes")
        st.write(scores_df)
        
        # Gráfico de barras
        st.subheader("Gráfico de Puntajes")
        chart = alt.Chart(scores_df).mark_bar().encode(
            x='Puntaje:Q',
            y=alt.Y('Jugador:N', sort='-x')
        )
        st.altair_chart(chart, use_container_width=True)
        
        # Almacenar en sesión para persistencia
        st.session_state['scores_df'] = scores_df
        
    else:
        st.warning("Por favor, ingresa los nombres de ambos jugadores.")

# Filtros de búsqueda
st.subheader("Filtros de Búsqueda")
filter_option = st.selectbox("Selecciona una opción", ["Todos", "Más recogieron", "Menos recogieron", "Empates"])
if filter_option == "Más recogieron":
    st.write(scores_df[scores_df['Puntaje'] == scores_df['Puntaje'].max()])
    st.subheader("Gráfico de Puntajes (Más recogieron)")
    chart = alt.Chart(scores_df[scores_df['Puntaje'] == scores_df['Puntaje'].max()]).mark_bar().encode(
        x='Puntaje:Q',
        y=alt.Y('Jugador:N', sort='-x')
    )
    st.altair_chart(chart, use_container_width=True)
elif filter_option == "Menos recogieron":
    st.write(scores_df[scores_df['Puntaje'] == scores_df['Puntaje'].min()])
    st.subheader("Gráfico de Puntajes (Menos recogieron)")
    chart = alt.Chart(scores_df[scores_df['Puntaje'] == scores_df['Puntaje'].min()]).mark_bar().encode(
        x='Puntaje:Q',
        y=alt.Y('Jugador:N', sort='-x')
    )
    st.altair_chart(chart, use_container_width=True)
elif filter_option == "Empates":
    st.write(scores_df[scores_df.duplicated('Puntaje', keep=False)])
    st.subheader("Gráfico de Puntajes (Empates)")
    chart = alt.Chart(scores_df[scores_df.duplicated('Puntaje', keep=False)]).mark_bar().encode(
        x='Puntaje:Q',
        y=alt.Y('Jugador:N', sort='-x')
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.write(scores_df)
    st.subheader("Gráfico de Puntajes (Todos)")
    chart = alt.Chart(scores_df).mark_bar().encode(
        x='Puntaje:Q',
        y=alt.Y('Jugador:N', sort='-x')
    )
    st.altair_chart(chart, use_container_width=True)

