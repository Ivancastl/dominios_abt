import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pyfiglet

class DomainHunter:
    def __init__(self):
        self.show_banner()

    def show_banner(self):
        """Muestra el banner ASCII art"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(pyfiglet.figlet_format("DomainHunter", font="slant"))
        print("🔍 Buscador de dominios recién registrados")
        print("👨💻 Creado por @ivancastl | Telegram: t.me/+_g4DIczsuI9hOWZh")
        print("="*60 + "\n")

    def get_domains_from_page(self, url):
        """Obtiene dominios de una página específica"""
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                domain_divs = soup.find_all('div', style=lambda value: value and 'word-wrap: break-word' in value)
                return [div.find('a').text.strip() for div in domain_divs if div.find('a')]
            print(f"⚠️ Error {response.status_code} al acceder a {url}")
            return []
        except Exception as e:
            print(f"❌ Excepción al acceder a {url}: {str(e)}")
            return []

    def buscar_dominios(self, base_url, file_name, palabra_clave=None):
        """Busca dominios en todas las partes de una URL base"""
        part = 1
        dominios_encontrados = []
        
        while True:
            current_url = f"{base_url}{part}/"
            domains = self.get_domains_from_page(current_url)
            
            if not domains:
                print(f"🔍 Fin de resultados en {base_url}")
                break
                
            if palabra_clave:
                dominios_filtrados = [d for d in domains if palabra_clave.lower() in d.lower()]
                dominios_encontrados.extend(dominios_filtrados)
            else:
                dominios_encontrados.extend(domains)
                
            print(f"✅ Página {part}: {len(domains)} dominios encontrados")
            part += 1

        if dominios_encontrados:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write('\n'.join(dominios_encontrados))
            print(f"\n💾 Guardados {len(dominios_encontrados)} dominios en {file_name}")
            if palabra_clave:
                print(f"🔎 Filtrados por palabra clave: '{palabra_clave}'")
        else:
            print("⚠️ No se encontraron dominios para guardar")

        return dominios_encontrados

    def generar_urls_por_fechas(self, inicio, fin):
        """Genera URLs para un rango de fechas"""
        try:
            fecha_inicio = datetime.strptime(inicio, '%Y%m%d')
            fecha_fin = datetime.strptime(fin, '%Y%m%d')
            
            if fecha_fin < fecha_inicio:
                raise ValueError("La fecha final no puede ser anterior a la inicial")
                
            tlds = ['com', 'shop', 'xyz', 'net']
            urls = []
            
            for single_date in (fecha_inicio + timedelta(n) for n in range((fecha_fin - fecha_inicio).days + 1)):
                fecha_str = single_date.strftime('%Y-%m-%d')
                date_id = single_date.strftime('%Y%m%d')
                
                for tld in tlds:
                    url = f'https://newly-registered-domains.abtdomain.com/{fecha_str}-{tld}-newly-registered-domains-part-'
                    filename = f'{date_id}_{tld}.txt'
                    urls.append((url, filename))
                    
            return urls
        except ValueError as e:
            print(f"❌ Error en formato de fechas: {str(e)}")
            return None

    def mostrar_menu(self):
        """Muestra el menú interactivo"""
        self.show_banner()
        print("1. Buscar todos los dominios por rango de fechas")
        print("2. Buscar dominios por palabra clave")
        print("3. Salir\n")
        return input("👉 Seleccione una opción (1-3): ").strip()

    def ejecutar(self):
        """Método principal para ejecutar el programa"""
        while True:
            opcion = self.mostrar_menu()
            
            if opcion == '3':
                print("\n👋 ¡Hasta pronto!")
                break
                
            if opcion not in ('1', '2'):
                print("\n❌ Opción no válida. Intente nuevamente.")
                input("\nPresiona Enter para continuar...")
                continue
                
            try:
                print("\n" + "="*40)
                inicio = input("📅 Fecha inicial (AAAAMMDD): ").strip()
                fin = input("📅 Fecha final (AAAAMMDD): ").strip()
                
                urls = self.generar_urls_por_fechas(inicio, fin)
                if not urls:
                    input("\nPresiona Enter para continuar...")
                    continue
                    
                palabra_clave = None
                if opcion == '2':
                    palabra_clave = input("🔍 Palabra clave a buscar: ").strip()
                    if not palabra_clave:
                        print("❌ Debe ingresar una palabra clave válida")
                        input("\nPresiona Enter para continuar...")
                        continue
                        
                print(f"\n🔎 Iniciando búsqueda desde {inicio} hasta {fin}...")
                for url, filename in urls:
                    print(f"\n🌐 Procesando: {filename.replace('.txt', '')}")
                    self.buscar_dominios(url, filename, palabra_clave)
                    
                input("\n✅ Búsqueda completada. Presiona Enter para continuar...")
                
            except Exception as e:
                print(f"\n❌ Error inesperado: {str(e)}")
                input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    import os
    hunter = DomainHunter()
    hunter.ejecutar()