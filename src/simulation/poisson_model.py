import numpy as np
from scipy.stats import poisson

def calcular_probabilidad_goles(lambda_equipo, goles):
    """
    Calcula la probabilidad exacta de que un equipo anote una cantidad
    específica de goles basándose en su media esperada (lambda).
    """
    return poisson.pmf(goles, lambda_equipo)

def generar_matriz_marcador(lambda_local, lambda_visitante, max_goles=5):
    """
    Genera una matriz con las probabilidades de resultados exactos del partido.
    Limita el cálculo hasta un número máximo de goles por equipo (por defecto 5).
    """
    # Creamos una matriz de ceros de tamaño (max_goles+1) x (max_goles+1)
    matriz_probabilidades = np.zeros((max_goles + 1, max_goles + 1))
    
    # Iteramos filas (goles local) y columnas (goles visitante)
    for i in range(max_goles + 1): 
        for j in range(max_goles + 1): 
            prob_local = calcular_probabilidad_goles(lambda_local, i)
            prob_visitante = calcular_probabilidad_goles(lambda_visitante, j)
            
            # La probabilidad de que ocurran ambos eventos independientes a la vez
            matriz_probabilidades[i, j] = prob_local * prob_visitante
            
    return matriz_probabilidades