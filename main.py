import os
from src.scrapers.fbref_scraper import obtener_ultimos_partidos_local
from src.predictor import predecir_partido

def buscar_nombre_real(lista_equipos, nombre_buscado):
    """
    Busca de forma flexible un equipo en la lista para evitar errores de idioma
    (ej. si buscas 'Bayern' y en el HTML dice 'Bayern München', lo encuentra).
    """
    for equipo in lista_equipos:
        if nombre_buscado.lower() in equipo.lower():
            return equipo
    return None

def ejecutar_sistema_real():
    # Ruta local hacia el archivo HTML que descargaste
    ruta_datos = os.path.join("data", "raw", "bundesliga.html")
    
    # 1. Extraer los datos desde el archivo local
    df_partidos_reales = obtener_ultimos_partidos_local(ruta_datos)
    
    if df_partidos_reales is not None:
        # Obtener la lista completa de equipos reales en el HTML
        equipos_html = list(df_partidos_reales['local'].unique())
        
        # 2. Búsqueda inteligente de nombres para evitar el error "lam < 0 or lam is NaN"
        # 2. Búsqueda inteligente de nombres para evitar el error "lam < 0 or lam is NaN"
        local_input = "Inter Miami"
        visitante_input = "LA Galaxy"
        
        local = buscar_nombre_real(equipos_html, local_input)
        visitante = buscar_nombre_real(equipos_html, visitante_input)
        
        # Validar que ambos equipos existan en el archivo procesado
        if not local or not visitante:
            print(f"❌ No se pudo emparejar los equipos de búsqueda en el HTML.")
            print(f"Equipos disponibles en tu archivo: {sorted(equipos_html)}")
            return

        print(f"\n🎯 Coincidencias encontradas en el archivo: '{local}' vs '{visitante}'")
        print(f"📊 Analizando histórico y corriendo simulación de Monte Carlo...")
        
        # 3. Correr la predicción y las 10,000 simulaciones de Monte Carlo
        prediccion = predecir_partido(df_partidos_reales, equipo_local=local, equipo_visitante=visitante)
        
        # 4. Mostrar los resultados finales de forma didáctica
        print("\n🚀 ==================== RESULTADOS DE LA SIMULACIÓN REAL ====================")
        print(f"📈 Goles proyectados de {local} (Lambda Local): {prediccion['lambda_local']:.2f}")
        print(f"📈 Goles proyectados de {visitante} (Lambda Visitante): {prediccion['lambda_visitante']:.2f}")
        print("-" * 72)
        print(f"🏠 Probabilidad de que gane {local}: {prediccion['simulacion']['prob_local']:.2f}%")
        print(f"🤝 Probabilidad de Empate: {prediccion['simulacion']['prob_empate']:.2f}%")
        print(f"🚀 Probabilidad de que gane {visitante}: {prediccion['simulacion']['prob_visitante']:.2f}%")
        print(f"⚽ Probabilidad de que haya Más de 2.5 Goles (Over): {prediccion['simulacion']['prob_over_2_5']:.2f}%")
        print("============================================================================\n")
    else:
        print("❌ No se pudieron procesar los datos locales para realizar la predicción.")

if __name__ == "__main__":
    ejecutar_sistema_real()