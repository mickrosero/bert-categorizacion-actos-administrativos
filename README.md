# 🤖 Clasificador de Actos Administrativos con BERT

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![BERT](https://img.shields.io/badge/BERT-BETO-green.svg)
![spaCy](https://img.shields.io/badge/spaCy-3.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descripción

Proyecto de clasificación automática de actos administrativos usando **BERT en español (BETO)** con técnicas avanzadas de **Procesamiento de Lenguaje Natural (NLP)** y limpieza de texto con **spaCy**.

Este sistema permite categorizar automáticamente documentos administrativos en múltiples categorías utilizando un modelo de transformer pre-entrenado en español, fine-tuned con datos específicos del dominio legal/administrativo.

## 🎯 Objetivos

- ✅ Automatizar la clasificación de actos administrativos
- ✅ Reducir el tiempo de categorización manual
- ✅ Mejorar la precisión en la clasificación de documentos legales
- ✅ Proporcionar un sistema escalable y reutilizable
- ✅ Reclasificar documentos con categoría "OTROS" de forma inteligente

## 🚀 Características Principales

### 🔹 Arquitectura Híbrida Local-Cloud
- **Parte 1 (Local)**: Preparación y limpieza de datos desde MariaDB/MySQL
- **Parte 2 (Colab)**: Entrenamiento con GPU (T4) en Google Colab

### 🔹 Procesamiento de Texto Avanzado
- **Lematización** con spaCy
- **Eliminación de stopwords** en español
- **Normalización** de texto (minúsculas, puntuación, números)
- **Tokenización** optimizada para BERT

### 🔹 Modelo de Machine Learning
- **Modelo Base**: `dcc.uchile/bert-base-spanish-wwm-cased` (BETO)
- **Fine-tuning** para clasificación multi-clase
- **Métricas**: Accuracy, F1-Score (macro)
- **Gestión de clases desbalanceadas**

## 📊 Categorías de Clasificación

El modelo clasifica documentos en **17 categorías**, incluyendo:

1. REQUERIMIENTO DE INFORMACIÓN
2. REVENIDO QUÍMICO
3. ACTO URGENTE SIN INDICIOS DELICTIVOS
4. IDENTIFICACIÓN BIENES RETENIDOS
5. ACTO URGENTE PARA EL EJERCICIO DE LA ACCIÓN PRIVADA
6. MUERTE NO DELICTIVA
7. IDENTIFICACIÓN BIENES ABANDONADOS
8. Y más...

## 🛠️ Tecnologías Utilizadas

### Backend & Processing
- **Python 3.8+**
- **Transformers** (Hugging Face)
- **PyTorch** (GPU acceleration)
- **spaCy 3.0+** (`es_core_news_md`)
- **scikit-learn**

### Data Management
- **Pandas** (manipulación de datos)
- **PyArrow/Fastparquet** (formato Parquet)
- **SQLAlchemy** + **PyMySQL** (conexión a bases de datos)
- **Google Drive API** (PyDrive2)

### Cloud Infrastructure
- **Google Colab** (entrenamiento con GPU T4)
- **Google Drive** (almacenamiento de modelos y datos)

## 📁 Estructura del Proyecto

```
bert-categorizacion-actos-administrativos/
│
├── README.md                              # Este archivo
├── .gitignore                             # Archivos ignorados por Git
│
├── NLP_berto_AA_COLAB_local.ipynb        # Notebook principal (híbrido)
├── NLP_berto_AA_COLAB.ipynb              # Notebook solo Colab
│
├── aa.xlsx                                # Dataset de ejemplo
│
├── models/                                # Modelos entrenados (no versionado)
│   └── modelo-clasificador-final/
│
├── data/                                  # Datos procesados (no versionado)
│   ├── datos-procesados.parquet
│   └── predicciones-OTROS.csv
│
└── notebooks/                             # Notebooks adicionales
    └── exploratory_analysis.ipynb
```

## 🔧 Instalación

### Requisitos Previos

#### Para Parte 1 (Local)
```bash
pip install pandas pyarrow fastparquet openpyxl
pip install SQLAlchemy pymysql
pip install pydrive2
```

#### Para Parte 2 (Colab)
```bash
pip install transformers datasets accelerate torch
pip install spacy
python -m spacy download es_core_news_md
```

### Configuración de Google Drive API

1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar la API de Google Drive
3. Crear credenciales OAuth 2.0
4. Descargar el archivo JSON y renombrarlo a `client_secrets.json`
5. Colocar el archivo en la misma carpeta del notebook

## 📖 Uso del Sistema

### PARTE 1: Preparación de Datos (Kernel Local)

```python
# 1. Configurar la conexión a tu base de datos
MARIADB_USUARIO = "tu_usuario"
MARIADB_CONTRASEÑA = "tu_contraseña"
MARIADB_HOST = "192.168.x.x"
MARIADB_BDD = "tu_base_datos"

# 2. Definir las columnas
COLUMNA_TEXTO = "OBSERVACION"       # Columna con el texto
COLUMNA_ETIQUETA = "AA"             # Columna con la categoría
ETIQUETA_A_EXCLUIR = "OTROS"        # Categoría a reclasificar

# 3. Ejecutar celdas 1.1 a 1.6
# Resultado: datos-procesados.parquet en Google Drive
```

### PARTE 2: Entrenamiento (Kernel Colab con GPU)

```python
# 1. Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. Cargar el archivo Parquet
RUTA_ARCHIVO_PARQUET = '/content/drive/MyDrive/ColabData/datos-procesados.parquet'

# 3. Ejecutar celdas 2.1 a 2.9
# Resultado: Modelo entrenado + predicciones CSV
```

## 📈 Resultados y Métricas

### Desempeño del Modelo

| Métrica | Valor |
|---------|-------|
| **Accuracy** | ~83.3% |
| **F1-Score (Macro)** | ~66.2% |
| **Epoch óptimo** | 3 |
| **Training Loss** | 0.321 |
| **Validation Loss** | 0.506 |

### Ejemplo de Predicciones

| Texto Original | Predicción | Confianza |
|---------------|-----------|----------|
| "Se adjunta oficio sobre requerimiento..." | REQUERIMIENTO DE INFORMACIÓN | 98.2% |
| "Solicitud de examen médico legal..." | ACTO URGENTE PARA EJERCICIO... | 92.5% |

## 🔍 Pipeline de Limpieza de Texto

El sistema aplica los siguientes pasos de preprocesamiento:

```python
def limpiar_texto_spacy(texto):
    """
    1. Convertir a minúsculas
    2. Procesar con spaCy
    3. Eliminar stopwords (de, la, el, etc.)
    4. Eliminar puntuación y números
    5. Filtrar solo tokens alfabéticos
    6. Lematizar (corriendo → correr)
    7. Retornar texto limpio
    """
    pass
```

## 🎓 Aplicaciones

- ✅ **Sector Legal**: Clasificación automática de documentos judiciales
- ✅ **Administración Pública**: Categorización de trámites y solicitudes
- ✅ **Fiscalías**: Organización de actos administrativos
- ✅ **Archivos Digitales**: Indexación inteligente de documentos

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Notas Importantes

### ⚠️ Limitaciones

- El modelo está entrenado específicamente para el dominio legal/administrativo ecuatoriano
- Requiere GPU para entrenamiento eficiente (~15-45 min en T4)
- Los datos sensibles no deben ser compartidos públicamente

### 🔐 Consideraciones de Seguridad

- No versionar archivos con credenciales (`client_secrets.json`)
- No subir datos personales o confidenciales al repositorio
- Usar variables de entorno para información sensible

## 📚 Referencias

- [BETO: Spanish BERT](https://github.com/dccuchile/beto)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [spaCy Documentation](https://spacy.io/)
- [Google Colab](https://colab.research.google.com/)

## 📧 Contacto

**Desarrollado por**: [Tu Nombre]
**Email**: tu.email@ejemplo.com
**GitHub**: [@mickrosero](https://github.com/mickrosero)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

⭐ Si este proyecto te fue útil, ¡no olvides darle una estrella! ⭐
