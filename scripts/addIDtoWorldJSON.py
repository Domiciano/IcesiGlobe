import json

# Cargar el countries.json
with open('../data/countries.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)
    
# Crear un mapeo de nombre de país a ID
name_to_id = {data['name']: cid for cid, data in countries.items()}

# Cargar el world.json
with open('../worldCopy.json', 'r', encoding='utf-8') as f:
    world = json.load(f)
    
# Insertar el ID correspondiente en cada feature
for feature in world['features']:
    country_name = feature['properties']['name']
    country_id = name_to_id.get(country_name)

    if country_id is not None:
        feature['properties']['id'] = int(country_id)  # Aseguramos que sea int si quieres
    else:
        print(f"[ADVERTENCIA] No se encontró ID para el país: {country_name}")

# Guardar el nuevo archivo
with open('world_with_ids.json', 'w', encoding='utf-8') as f:
    json.dump(world, f, ensure_ascii=False, indent=2)

print("¡Archivo world_with_ids.json generado correctamente!")