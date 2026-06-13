import pandas as pd

def calcular_fuerzas_liga(df_partidos):
    """
    Calcula los promedios globales de la liga.
    Son la base para medir qué tan bueno es un equipo respecto al promedio.
    """
    prom_goles_local = df_partidos['goles_local'].mean()
    prom_goles_vis = df_partidos['goles_visitante'].mean()
    return prom_goles_local, prom_goles_vis

def calcular_metricas_equipo(df_partidos, equipo):
    """
    Calcula el Poder de Ataque y Defensa de un equipo específico
    basado en sus últimos partidos históricos.
    """
    # Promedios de toda la liga
    prom_g_local, prom_g_vis = calcular_fuerzas_liga(df_partidos)
    
    # 1. Filtrar partidos donde el equipo jugó de LOCAL
    partidos_local = df_partidos[df_partidos['local'] == equipo]
    goles_anotados_local = partidos_local['goles_local'].mean()
    goles_recibidos_local = partidos_local['goles_visitante'].mean()
    
    # 2. Filtrar partidos donde el equipo jugó de VISITANTE
    partidos_vis = df_partidos[df_partidos['visitante'] == equipo]
    goles_anotados_vis = partidos_vis['goles_visitante'].mean()
    goles_recibidos_vis = partidos_vis['goles_local'].mean()
    
    # Calcular Fuerzas Relativas (Tu rendimiento / Rendimiento promedio de la liga)
    # Ataque: Más alto que 1.0 significa que anota más que el promedio
    ataque_local = goles_anotados_local / prom_g_local if prom_g_local > 0 else 1.0
    ataque_vis = goles_anotados_vis / prom_g_vis if prom_g_vis > 0 else 1.0
    
    # Defensa: Menor que 1.0 significa que recibe MENOS goles que el promedio (es mejor defensa)
    defensa_local = goles_recibidos_local / prom_g_vis if prom_g_vis > 0 else 1.0
    defensa_vis = goles_recibidos_vis / prom_g_local if prom_g_local > 0 else 1.0
    
    return {
        "equipo": equipo,
        "ataque_local": ataque_local,
        "ataque_vis": ataque_vis,
        "defensa_local": defensa_local,
        "defensa_vis": defensa_vis
    }