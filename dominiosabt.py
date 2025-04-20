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
            print(f"❌ Error {response.status_code} al acceder a {url}")
            return []
    except Exception as e:
        print(f"⚠️ Error al acceder a {url}: {str(e)}")
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
            print(f"✅ Encontrados {len(domains)} dominios en {current_url}")
            part += 1
        else:
            print(f"🔍 Fin de dominios en {current_url}")
            break

    if dominios_encontrados:
        with open(file_name, 'w', encoding='utf-8') as file:
            for dominio in dominios_encontrados:
                file.write(dominio + '\n')
        
        resultado = f"📥 Guardados {len(dominios_encontrados)} dominios"
        if palabra_clave:
            resultado += f" con '{palabra_clave}'"
        resultado += f" en '{file_name}'"
        print(resultado)
    else:
        print(f"⚠️ No se encontraron dominios para guardar")

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
        print(f"❌ Error en fechas: {str(e)}")
        return None

def mostrar_menu():
    print("\n" + "="*50)
    print("🔍 BUSCADOR DE DOMINIOS RECIÉN REGISTRADOS 🔍".center(50))
    print("="*50)
    print("1️⃣ Buscar TODOS los dominios por fecha")
    print("2️⃣ Buscar dominios por PALABRA CLAVE")
    print("3️⃣ Salir del programa")
    return input("\n👉 Seleccione una opción (1-3): ")

def main():
    print("="*60)
    print(pyfiglet.figlet_format("Domain Hunter", font="slant"))
    print("🛠️ Herramienta para encontrar dominios recién registrados")
    print("👨‍💻 Creado por @ivancastl | Telegram: t.me/+_g4DIczsuI9hOWZh")
    print("="*60)
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == '3':
            print("\n👋 Saliendo del programa...")
            break
            
        if opcion not in ('1', '2'):
            print("\n❌ Opción inválida, intente nuevamente")
            continue
            
        print("\n📅 Ingrese rango de fechas (AAAAMMDD)")
        inicio = input("Fecha inicial: ")
        fin = input("Fecha final: ")
        
        base_urls = generar_urls_por_fechas(inicio, fin)
        if not base_urls:
            continue
            
        palabra_clave = None
        if opcion == '2':
            palabra_clave = input("\n🔎 Ingrese palabra clave a buscar: ").strip()
            if not palabra_clave:
                print("❌ Debe ingresar una palabra clave")
                continue
                
        print(f"\n🚀 Iniciando búsqueda desde {inicio} hasta {fin}...")
        for base_url, file_name in base_urls:
            print(f"\n🌐 Procesando: {base_url}")
            buscar_dominios(base_url, file_name, palabra_clave)

if __name__ == "__main__":
    import pyfiglet
    main()