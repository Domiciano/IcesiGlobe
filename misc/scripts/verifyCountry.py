import json

def readCountries():
    file_path = './countriesSplit.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        countries = [line.strip() for line in f if line.strip()]
    return countries

def readJson():
    file_path = './lotes/merge.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def main():
    countries = readCountries()
    countries_data = readJson()
    
    correct_order = True
    
    # Convertimos las claves en enteros para ordenarlas
    sorted_keys = sorted(countries_data.keys(), key=lambda x: int(x))
    
    for idx, key in enumerate(sorted_keys):
        json_country_name = countries_data[key]['name']
        txt_country_name = countries[idx] if idx < len(countries) else None

        if json_country_name != txt_country_name:
            print(f"Desorden encontrado en índice {idx + 1}: JSON='{json_country_name}' VS TXT='{txt_country_name}'")
            correct_order = False
    
    if correct_order:
        print("¡Todos los países están en el mismo orden!")

if __name__ == "__main__":
    main()
