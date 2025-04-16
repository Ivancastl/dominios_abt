import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def get_domains_from_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            domain_divs = soup.find_all('div', style=lambda value: value and 'word-wrap: break-word' in value)
            domains = []
            for div in domain_divs:
                a_tag = div.find('a')
                if a_tag and a_tag.text.strip():
                    domains.append(a_tag.text.strip())
            return domains
        else:
            print(f"[ERROR] Código {response.status_code} al acceder a {url}")
            return []
    except Exception as e:
        print(f"[EXCEPCIÓN] No se pudo acceder a {url}: {e}")
        return []

def buscar_dominios(base_url, file_name, palabra_clave=None):
    part = 1
    dominios_encontrados = []
    total_dominios_recorridos = 0

    while True:
        current_url = f"{base_url}{part}/"
        domains = get_domains_from_page(current_url)

        if domains:
            if palabra_clave:
                dominios_filtrados = [d for d in domains if palabra_clave.lower() in d.lower()]
                dominios_encontrados.extend(dominios_filtrados)
            else:
                dominios_encontrados.extend(domains)
                
            total_dominios_recorridos += len(domains)
            print(f"✅ Recuperados {len(domains)} dominios de {current_url}")
            part += 1
        else:
            print(f"🔍 No se encontraron más dominios en {current_url}")
            break

    if dominios_encontrados:
        with open(file_name, 'w', encoding='utf-8') as file:
            for dominio in dominios_encontrados:
                file.write(dominio + '\n')
        msg = f"💾 Guardados {len(dominios_encontrados)} dominios"
        if palabra_clave:
            msg += f" que contienen '{palabra_clave}'"
        msg += f" en '{file_name}'"
        print(msg)
    else:
        print(f"⚠️ No se encontraron dominios para guardar en '{file_name}'")

    return dominios_encontrados

def generar_urls_por_fechas(inicio, fin):
    try:
        fecha_inicio = datetime.strptime(inicio, '%Y%m%d')
        fecha_fin = datetime.strptime(fin, '%Y%m%d')
        
        if fecha_fin < fecha_inicio:
            raise ValueError("La fecha final no puede ser anterior a la inicial")
            
        delta = timedelta(days=1)
        base_urls = []

        while fecha_inicio <= fecha_fin:
            fecha_str = fecha_inicio.strftime('%Y-%m-%d')
            date_id = fecha_inicio.strftime('%Y%m%d')

            tlds = ['com', 'shop', 'xyz', 'net']
            for tld in tlds:
                url = f'https://newly-registered-domains.abtdomain.com/{fecha_str}-{tld}-newly-registered-domains-part-'
                filename = f'{date_id}_{tld}.txt'
                base_urls.append((url, filename))

            fecha_inicio += delta

        return base_urls
    except ValueError as e:
        print(f"❌ Error en formato de fechas: {e}")
        return None

def mostrar_menu():
    print("\n" + "="*50)
    print("BUSCADOR DE DOMINIOS RECIÉN REGISTRADOS".center(50))
    print("="*50)
    print("1. Buscar todos los dominios por rango de fechas")
    print("2. Buscar dominios por palabra clave")
    print("3. Salir")
    return input("Seleccione una opción (1-3): ")

def main():
    while True:
        opcion = mostrar_menu()
        
        if opcion == '3':
            print("Saliendo del programa...")
            break
            
        if opcion not in ('1', '2'):
            print("❌ Opción no válida. Por favor seleccione 1, 2 o 3.")
            continue
            
        inicio = input("Ingrese fecha inicial (AAAAMMDD): ")
        fin = input("Ingrese fecha final (AAAAMMDD): ")
        
        base_urls = generar_urls_por_fechas(inicio, fin)
        if not base_urls:
            continue
            
        palabra_clave = None
        if opcion == '2':
            palabra_clave = input("Ingrese palabra clave a buscar: ").strip()
            if not palabra_clave:
                print("❌ Debe ingresar una palabra clave válida")
                continue
                
        print(f"\nIniciando búsqueda desde {inicio} hasta {fin}...")
        for base_url, file_name in base_urls:
            print(f"\n🔎 Procesando: {base_url}")
            buscar_dominios(base_url, file_name, palabra_clave)

if __name__ == "__main__":
    main()