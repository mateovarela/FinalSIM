import sys
import os
import random
from support import clasificar_numero_aleatorio, get_table, determinar_vpn_y_probabilidades

sys.path.append(os.getcwd())


# -- SIMULACION --

def fila(a, b, c):
    
    # Esta funcion no devuelve ninguna metrica, solo devuelve los valores simulados de la fila actual

    fila = [None, None, None, None, None, None, 0.0]

    i = 0
    # Se determina el VPN de cada proyecto
    for x in [a, b, c]:
        if x is not None:
            rnd = random.random()
            fila[i] = rnd
            fila[i+1] = clasificar_numero_aleatorio(rnd, x[0], x[1])
        i += 2
        
    # Se calcula el VPN total
    fila[-1] = sum(fila[i] for i in (1, 3, 5) if fila[i] is not None)

    return fila


def simular_fila(iteracion, fila_anterior, a, b, c):
    
    # En esta funcion se toma la memoria de una fila, y se van calculando las metricas segun la fila actual y la anterior

    # Tomamos lo que puede quedar igual que la fila anterior
    vpn_acumulado_anterior = fila_anterior[-2]

    fila_simulada = fila(a, b, c)

    vpn_acumulado = vpn_acumulado_anterior + fila_simulada[-1]
    vpn_promedio = vpn_acumulado/(iteracion+1)

    fila_actual = [iteracion+1] + fila_simulada + [vpn_acumulado, vpn_promedio]

    return fila_actual


def simular_tabla(n, i, j, inversiones):
    # Inicializamos el vector estado a retornar
    vector_estado = []

    # Definimos los proyectos A, B y C
    # [clases, probabilidades]
    a = determinar_vpn_y_probabilidades('Proyecto A', inversiones[0])
    b = determinar_vpn_y_probabilidades('Proyecto B', inversiones[1])
    c = determinar_vpn_y_probabilidades('Proyecto C', inversiones[2])

    # Definimos la fila anterior para trabajar con memoria de 2 filas
    # [iteracion, rnd_A, VPN_A, rnd_B, VPN_B, rnd_C, VPN_C, VPN, VPN_acumulado, VPN_promedio]
    fila_anterior = [None, 0.0, None, 0.0, None, 0.0, None, 0.0, 0.0, 0.0]
    
    for iteracion in range(n):

        fila_actual = simular_fila(iteracion, fila_anterior, a, b, c)
        
        # Actualizar la fila anterior
        fila_anterior = fila_actual

        # Agregar fila al vector estado si esta en el rango seleccionado
        if j-1 <= iteracion <= j+i-2:
            vector_estado.append(fila_actual)
        
        # Guardar la última fila
        if iteracion == n-1:
            ultima_fila = fila_actual[:]
    
    # Retornamos 
    return vector_estado, ultima_fila


def simulacion(n, i, j):

    tablas = []

    combinaciones = [
        [2000000, 0, 0],
        [0, 2000000, 0],
        [0, 0, 2000000],
        [1500000, 500000, 0],
        [1500000, 0, 500000],
        [500000, 1500000, 0],
        [0, 1500000, 500000],
        [500000, 0, 1500000],
        [0, 500000, 1500000],
        [1000000, 1000000, 0],
        [1000000, 0, 1000000],
        [0, 1000000, 1000000],
        [1000000, 500000, 500000],
        [500000, 1000000, 500000],
        [500000, 500000, 1000000],
    ]

    mejor_combinacion = None
    mejor_combinacion_vpn = 0

    for inversiones in combinaciones:
            
        v_e, u_f = simular_tabla(n, i, j, inversiones)

        tabla_mejorada = (v_e, u_f, inversiones)
        
        tablas.append(tabla_mejorada)
        
        if mejor_combinacion is None or u_f[-1] > mejor_combinacion_vpn:
            mejor_combinacion = inversiones
            mejor_combinacion_vpn = u_f[-1]

    return tablas, mejor_combinacion, mejor_combinacion_vpn


if __name__ == "__main__":

    n = 100000
    i = 10
    j = 500
    
    """
    inversiones = [500000, 1000000, 500000]
    
    v_e, u_f = simular_tabla(n, i, j, inversiones)

    for e in v_e:
        print(e)
    
    print(u_f)
    """

    tablas, mejor_combinacion, mejor_combinacion_vpn = simulacion(n, i, j)

    print(mejor_combinacion)
    print(mejor_combinacion_vpn)



    # print(len(v_e[0]))

    get_table(tablas)
