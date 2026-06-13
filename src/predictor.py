import pandas as pd
from src.features.team_metrics import calcular_metricas_equipo, calcular_fuerzas_liga
from src.simulation.monte_carlo import ejecutar_monte_carlo

def predecir_partido(df_partidos, equipo_local, equipo_visitante, iteraciones=10000):
    """
    Orquesta todo el flujo: toma los datos históricos, calcula los lambdas
    de ambos equipos y ejecuta la simulación de Monte Carlo.
    """
    # 1. Obtener los promedios globales de la liga
    prom_g_local, prom_g_vis = calcular_fuerzas_liga(df_partidos)
    
    # 2. Calcular las fuerzas de ataque y defensa de cada equipo
    metricas_local = calcular_metricas_equipo(df_partidos, equipo_local)
    metricas_visitante = calcular_metricas_equipo(df_partidos, equipo_visitante)
    
    # 3. Aplicar la fórmula cruzada para obtener los lambdas (Goles Esperados)
    lambda_local = (metricas_local['ataque_local'] * metricas_visitante['defensa_vis'] * prom_g_local)
    
    lambda_visitante = (metricas_visitante['ataque_vis'] * metricas_local['defensa_local'] * prom_g_vis)
    
    # 4. Enviar los lambdas calculados al motor de Monte Carlo
    resultados_simulacion = ejecutar_monte_carlo(
        lambda_local=lambda_local, 
        lambda_visitante=lambda_visitante, 
        iteraciones=iteraciones
    )
    
    # Retornamos los resultados junto con los lambdas calculados (útil para la interfaz)
    return {
        "lambda_local": lambda_local,
        "lambda_visitante": lambda_visitante,
        "simulacion": resultados_simulacion
    }
