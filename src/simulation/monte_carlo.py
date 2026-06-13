import numpy as np

def simular_partido(lambda_local, lambda_visitante):
    """
    Simula los goles de un solo partido generando números aleatorios
    basados en la distribución de Poisson de cada equipo.
    """
    goles_local = np.random.poisson(lambda_local)
    goles_visitante = np.random.poisson(lambda_visitante)
    return goles_local, goles_visitante

def ejecutar_monte_carlo(lambda_local, lambda_visitante, iteraciones=10000):
    """
    Ejecuta el partido miles de veces para recopilar estadísticas y
    calcular las probabilidades de victoria, empate o derrota.
    """
    victorias_local = 0
    empates = 0
    victorias_visitante = 0
    total_goles_simulados = []

    for _ in range(iteraciones):
        goles_l, goles_v = simular_partido(lambda_local, lambda_visitante)
        total_goles_simulados.append(goles_l + goles_v)
        
        # Evaluar el resultado del partido simulado
        if goles_l > goles_v:
            victorias_local += 1
        elif goles_l == goles_v:
            empates += 1
        else:
            victorias_visitante += 1

    # Calcular porcentajes finales
    prob_local = (victorias_local / iteraciones) * 100
    prob_empate = (empates / iteraciones) * 100
    prob_visitante = (victorias_visitante / iteraciones) * 100
    
    # Métrica extra didáctica: Probabilidad de Over 2.5 goles
    over_2_5 = sum(1 for goles in total_goles_simulados if goles > 2.5)
    prob_over_2_5 = (over_2_5 / iteraciones) * 100

    return {
        "prob_local": prob_local,
        "prob_empate": prob_empate,
        "prob_visitante": prob_visitante,
        "prob_over_2_5": prob_over_2_5
    }