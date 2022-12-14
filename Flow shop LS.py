# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 15:47:56 2022

@author: Daniel
"""

import matplotlib.pyplot as plt
import numpy as np
import random
import time
from copy import deepcopy
from numpy.random import randint, seed

def inicializar_gantt(maquinas, ht):
    # Parámetros:
    hbar = 10
    tticks = 10
    nmaq = len(maquinas)

    # Creación de los objetos del plot:
    fig, gantt = plt.subplots()

    # Diccionario con parámetros:
    diagrama = {
        "fig": fig,
        "ax": gantt,
        "hbar": hbar,
        "tticks": tticks,
        "maquinas": maquinas,
        "ht": ht,
        "colores": {}
    }

    # Etiquetas de los ejes:
    gantt.set_xlabel("Tiempo")
    gantt.set_ylabel("Máquinas")

    # Límites de los ejes:
    gantt.set_xlim(0, ht)
    gantt.set_ylim(nmaq*hbar, 0)

    # Divisiones del eje de tiempo:
    gantt.set_xticks(range(0, ht, 1), minor=True)
    gantt.grid(True, axis='x', which='both')

    # Divisiones del eje de máquinas:
    gantt.set_yticks(range(hbar, nmaq*hbar, hbar), minor=True)
    gantt.grid(True, axis='y', which='minor')

    # Etiquetas de máquinas:
    gantt.set_yticks(np.arange(hbar/2, hbar*nmaq - hbar/2 + hbar,
                            hbar))
    gantt.set_yticklabels(maquinas)

    return diagrama

# Función para armar tareas:
def agregar_subtareas(diagrama, t0, d, maq, nombre_tarea, color=None):
    maquinas = diagrama["maquinas"]
    hbar = diagrama["hbar"]
    gantt = diagrama["ax"]
    ht = diagrama["ht"]

    # Color:
    if diagrama["colores"].get(nombre_tarea) == None:
        if color == None:
            r = random.random()
            g = random.random()
            b = random.random()
            color = (r, g, b)

            diagrama["colores"].update({nombre_tarea: color})
    else:
        color = diagrama["colores"].get(nombre_tarea)

    # Índice de la máquina:
    imaq = maquinas.index(maq)
    # Posición de la barra:
    gantt.broken_barh([(t0, d)], (hbar*imaq, hbar),
                      facecolors=(color))
    # Posición del texto:
    gantt.text(x=(t0 + d/2), y=(hbar*imaq + hbar/2),
                  s=f"{nombre_tarea} ({d})", va='center', ha='center', color='white')

def completar_gantt(diagrama, calendario, n_maqs, n_tareas):
    # Agregamos las subtareas:
    for subtarea in calendario:

        agregar_subtareas(
            diagrama,
            subtarea["t0"],
            subtarea["d"],
            n_maqs[subtarea["i_maq"]],
            n_tareas[subtarea["i_tarea"]]
        )

def crear_gantt_fs(calendario, n_maqs, n_tareas):
    # Horizonte temporal:
    ultima_subtarea = calendario[-1]
    ht = ultima_subtarea["t0"] + ultima_subtarea["d"]

    # Creamos el diagrama de gantt:
    diagrama = inicializar_gantt(n_maqs, ht)

    # Completamos el gantt:
    completar_gantt(diagrama, calendario, n_maqs, n_tareas)

    # Retornamos el diagrama:
    return diagrama

def crear_y_mostrar_gantt_fs(calendario, n_maqs, n_tareas):
    # Creamos el gantt:
    crear_gantt_fs(calendario, n_maqs, n_tareas)

    # Plotteamos:
    mostrar()

def mostrar():
    plt.show()
    
    
def calcular_makespan(calendario):
    ultima_subtarea = calendario[-1]
    primera_subtarea = calendario[0]

    return ultima_subtarea['t0'] + ultima_subtarea['d'] - primera_subtarea['t0']    

def agregar_subtarea(calendario, t0, d, i_maq, i_tarea):
    # Diccionario de subtarea:
    subtarea = {'t0': t0, 'd': d, 'i_maq': i_maq, 'i_tarea': i_tarea}

    # Agregar al calendario
    calendario.append(subtarea)

def programar_fs(d_tareas, nombre_maq, nombre_tar, secuencia):
    # Creamos el calendario:
    calendario = []

    # Último t0 para cada etapa:
    tn_etapa = [0]*len(nombre_maq)

    # Para cada tarea en la secuencia:
    for i_tarea in secuencia:
        # Para cada subtarea en la tarea:
        for i_maquina, d_subtarea in enumerate(d_tareas[i_tarea]):
            tn_maq_anterior = tn_etapa[i_maquina-1]
            tn_maq_presente = tn_etapa[i_maquina]

            # Obtenemos el t0:
            if (i_maquina > 0) & (tn_maq_anterior > tn_maq_presente):
                t0 = tn_maq_anterior
            else:
                t0 = tn_maq_presente

            # Agregamos subtarea programada:
            agregar_subtarea(calendario, t0, d_subtarea, i_maquina, i_tarea)

            # Nuevo tn:
            tn_etapa[i_maquina] = t0 + d_subtarea

    return calendario


def leer_archivo(filename: str, k: int) -> zip:

    with open(filename, "r") as f:
        l = f.readlines()

    l = [i.replace("  ", " ").strip() for i in l]
    l

    instancias = dict()
    cantidad_instancias = 10
    instancia = [[int(j) for j in i.split(" ")] for i in l[(((k-1) * 23) + 3) : ((k) * 23)]]

    instancia = list(zip(*instancia))
       
    return instancia

#%%
instancia = leer_archivo("tai500_20.txt", 1)
print(instancia)

#%%
# Datos del problema:
nombre_maq = ["M"+str(i) for i in range(20)]
nombre_tar = ["T"+str(i) for i in range(500)]

d_tareas = np.array(instancia)
#print(d_tareas)
secuencia = list(range(0,500))

calendario1 = programar_fs(d_tareas, nombre_maq, nombre_tar, secuencia)

print(calendario1)

# calculamos el makespan y lo imprimimos:
makespan = calcular_makespan(calendario1)

print(f'\n El makespan es',makespan)


#diagrama = crear_gantt_fs(calendario1, nombre_maq, nombre_tar)
#%%
#Swap
#print(f"Solucion inicial {secuencia}, \n FO {makespan}")

def swap(secuencia, makespan):
    #Tiempo_inicio = time.time()
    incumbente = makespan
    mejor_sec = secuencia
    movimientos = 0
    repite = True
    while repite ==True:
        
        mejora = False
         
        for i in range(len(secuencia)-1):
            primera = secuencia[i]
            
            for j in range(i+1, len(secuencia)):
                segunda = secuencia[j]
                
                nueva_sec = deepcopy(secuencia)
                nueva_sec[i],nueva_sec[j] = segunda,primera
                nuevo_calendario = programar_fs(d_tareas, nombre_maq, nombre_tar, nueva_sec)
                nuevo_makespan =calcular_makespan(nuevo_calendario)
                
                if nuevo_makespan < incumbente:
                    incumbente = nuevo_makespan
                    mejor_sec = nueva_sec
                    mejora = True
                    break
                    
            if mejora == True:
                break
        if mejora == True:
            movimientos += 1
            repite = True
        else:
            repite = False
                    
    return incumbente, mejor_sec

def ls_cross_order(secuencia, makespan, neighborhood = 1000):

    mejora = False
    incumbente = makespan
    mejor_sec = secuencia

    for itera in range(neighborhood):

        rand1 = randint(-1,497)
        rand2 = randint(rand1 + 3, 501)
        new_sol = deepcopy(secuencia)

        if rand1 == -1:
            vec1 = []
            pos1 = 0
        else:
            vec1 = secuencia[:rand1 + 1]
            pos1 = rand1 + 1
        
        if rand2 == 500:
            vec2 = []
            pos2 = 500
        else:
            vec2 = secuencia[rand2:]
            pos2 = rand2
        
        nueva_sol = secuencia[pos1:pos2]   
        nueva_sol = nueva_sol[::-1]

        nueva_sec = vec1 + new_sol + vec2
        nuevo_calendario = programar_fs(d_tareas, nombre_maq, nombre_tar, nueva_sec)
        nuevo_makespan =calcular_makespan(nuevo_calendario)

        if nuevo_makespan < incumbente:
            incumbente = nuevo_makespan
            mejor_sec = nueva_sec
            mejora = True
    
    return incumbente, mejor_sec

#%%


       