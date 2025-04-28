import requests
import time


file_path = '../data/countries.txt'

# Leer los países
with open(file_path, 'r', encoding='utf-8') as f:
    countries = [line.strip() for line in f if line.strip()]

# Lista para almacenar los países que fallan
failed_countries = []

# Verificar cada país
for country in countries:
    url = f'https://nominatim.openstreetmap.org/search?q={country}&format=jsonv2'
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()

        # Validar si no encontró resultados
        if not data:
            print(f"No encontrado: {country}")
            failed_countries.append(country)

    except Exception as e:
        print(f"Error consultando {country}: {e}")
        failed_countries.append(country)

    # Esperar 500 ms entre peticiones
    print(f"Consulta para {country} existosa.")
    

# Resultado final
print("\nPaíses que fallaron:")
for failed in failed_countries:
    print(failed)
