# Buscador de Dominios Recién Registrados

Herramienta para buscar dominios recién registrados en abtdomain.com por rango de fechas o por palabra clave.

## Características

- Búsqueda por rango de fechas (AAAAMMDD)
- Filtrado por palabra clave
- Soporte para múltiples TLDs (.com, .shop, .xyz, .net)
- Generación de archivos de texto con resultados
- Interfaz de consola interactiva

## Requisitos

- Python

## Instalación

### **Paso 1:**
Clona este repositorio
```bash
git clone https://github.com/Ivancastl/dominios_abt.git
```

### **Paso 2:**
Accede al directorio del proyecto
```bash
cd dominios_abt
```

### **Paso 3:**
Instala los requisitos del proyecto:
```bash
pip install -r requirements.txt
```

### **Paso 4:**
Ejecuta el script:
```bash
python dominiosabt.py
```


## Sigue las instrucciones en pantalla:

Selecciona el modo de búsqueda (todos los dominios o por palabra clave)

Ingresa el rango de fechas (formato AAAAMMDD)

Si es búsqueda por palabra clave, ingresa el término a buscar

Los resultados se guardarán en archivos .txt con el formato AAAAMMDD_TLD.txt