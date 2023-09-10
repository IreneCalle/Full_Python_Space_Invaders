import pygame
import random
import math
from pygame import mixer


#inicializar pygame
pygame.init()

#crear pantalla
pantalla = pygame.display.set_mode((800,600))
se_ejecuta = True

#titulo, icono
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load("Icon.PNG")
pygame.display.set_icon(icono)
fondo = pygame.image.load("stars_fondo.png")


#Agregar musica de fondo
mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)


#imagen de jugador y coordenadas iniciales
img_jugador = pygame.image.load("cohete.png")

#texto final de juego
fuente_final = pygame.font.Font("CorelDraw.ttf", 35)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))

    #cambio de tamaño
imagen_cohete_small = pygame.transform.scale(img_jugador, (60, 60))
img_jugador = imagen_cohete_small

    #coordenadas jugador
jugador_x = 360
jugador_y = 530
jugador_x_cambio = 0


#definir la situacion del jugador y hacer que aparezca en pantalla
def jugador(x,y):
    pantalla.blit(img_jugador, (x, y))


# variables enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0,752))
    enemigo_y.append(random.randint(50,  200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)







def enemigo(x,y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))



# variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#puntaje

puntuacion = 0
fuente = pygame.font.Font('CorelDraw.ttf', 24,)
texto_x = 10
texto_y = 10




#funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f" SCORE .......... {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))




#funcion dispara bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

#funcion detectar_colisiones
def hay_colision(x_1, x_2, y_1, y_2):
    distancia = math.sqrt(math.pow(x_2-x_1, 2) + math.pow(y_2-y_1, 2))
    if distancia < 60:
        return True
    else:
        return False



#bucle de ejecucion del juego
while se_ejecuta:
    #evento de cierre de programa
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #evento de presion sobre teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        #evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.0


    #imagen de fonto
    pantalla.blit(fondo, (0,0))

    #actualizar la posicion del jugador
    jugador_x += jugador_x_cambio

    #mantener en los bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 740:
        jugador_x = 740

    # actualizar la posicion del enemigo
    for e in range(cantidad_enemigos):
        # check de fin de juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]


    # mantener en los bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 755:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("Golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntuacion += 1
            print(puntuacion)
            enemigo_x[e] = random.randint(0, 752)
            enemigo_y[e] = random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_y[e], e)

    #movimiento bala

    if bala_y <= -64:
        bala_y = 500
        bala_visible = False


    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio




    jugador(jugador_x, jugador_y)

    #mostrar puntuacion
    mostrar_puntaje(texto_x, texto_y)

    #actualizacion de apariencia
    pygame.display.update()



