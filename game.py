import pygame
import random
import time
import streamlit as st
import pandas as pd

# Función para iniciar Pygame
def init_pygame():
    pygame.init()
    return pygame.display.set_mode((800, 600))

# Función para manejar eventos de teclado
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False

# Función para dibujar la ventana del juego
def draw_window(win, player1, player2, trash, score1, score2, player1_name, player2_name):
    win.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 24)
    text1 = font.render(player1_name, True, (0, 0, 0))
    text2 = font.render(player2_name, True, (0, 0, 0))
    win.blit(text1, (player1.x, player1.y - 20))
    win.blit(text2, (player2.x, player2.y - 20))
    pygame.draw.rect(win, (0, 0, 0), player1)
    pygame.draw.rect(win, (0, 0, 0), player2)
    for t in trash:
        pygame.draw.rect(win, (0, 0, 0), t)
    pygame.display.update()

# Función para manejar el movimiento de los jugadores
def handle_movement(keys, player, keys_mapping):
    if keys[keys_mapping['left']] and player.x - 5 > 0:  # LEFT
        player.x -= 5
    if keys[keys_mapping['right']] and player.x + 5 + 50 < 800:  # RIGHT
        player.x += 5
    if keys[keys_mapping['up']] and player.y - 5 > 0:  # UP
        player.y -= 5
    if keys[keys_mapping['down']] and player.y + 5 + 50 < 600:  # DOWN
        player.y += 5

# Función para verificar colisiones entre jugadores y basura
def check_collision(player, trash):
    for t in trash[:]:
        if player.colliderect(t):
            trash.remove(t)
            # Generar nueva basura en una posición aleatoria
            new_trash = pygame.Rect(random.randint(0, 800 - 30), random.randint(0, 600 - 30), 30, 30)
            trash.append(new_trash)
            return 1
    return 0

# Función para ejecutar el juego
def run_game(player1_name, player2_name, scores_df):
    win = init_pygame()
    clock = pygame.time.Clock()

    player1 = pygame.Rect(100, 300, 50, 50)
    player2 = pygame.Rect(700, 300, 50, 50)
    trash = [pygame.Rect(random.randint(0, 800 - 30), random.randint(0, 600 - 30), 30, 30) for _ in range(10)]

    score1, score2 = 0, 0
    keys_mapping1 = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s}
    keys_mapping2 = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN}

    start_time = time.time()
    run = True

    while run:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        
        if handle_events():
            break

        handle_movement(keys, player1, keys_mapping1)
        handle_movement(keys, player2, keys_mapping2)

        score1 += check_collision(player1, trash)
        score2 += check_collision(player2, trash)

        draw_window(win, player1, player2, trash, score1, score2, player1_name, player2_name)

        if time.time() - start_time > 30:
            run = False

        # Actualizar DataFrame y gráfico cuando se recolecta basura
        if score1 > 0 or score2 > 0:
            # Actualizar DataFrame
            scores_df.loc[len(scores_df)] = [player1_name, score1]
            scores_df.loc[len(scores_df)] = [player2_name, score2]

    pygame.quit()
    return [(player1_name, score1), (player2_name, score2)], scores_df

# Configuración de la página
st.set_page_config(page_title="CESDE Medio Ambiente", layout="wide")

# Título y Descripción
st.title("Juego Interactivo de Medio Ambiente - CESDE")
st.markdown("Recolecta la mayor cantidad de basura en 30 segundos.")

# Input para nombres de jugadores
player1_name = st.text_input("Nombre del Jugador 1", "")
player2_name = st.text_input("Nombre del Jugador 2", "")

# Leer registros anteriores de puntajes
scores_df = pd.DataFrame(columns=['Jugador', 'Puntaje'])

# Botón de inicio del juego
if st.button("Start"):
    if player1_name and player2_name:
        scores, scores_df = run_game(player1_name, player2_name, scores_df)
        st.session_state['scores'] = scores
        st.success("¡El juego ha terminado!")
    else:
        st.warning("Por favor, ingresa los nombres de ambos jugadores.")

# Mostrar puntajes si el juego ha terminado
if 'scores' in st.session_state:
    st.subheader("Tabla de Puntajes")
    st.write(pd.DataFrame(st.session_state['scores'], columns=['Jugador', 'Puntaje']))
