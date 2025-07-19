# 🎭 Guía Completa: Face Swap en Fooocus

## 📋 Resumen Ejecutivo

Esta guía te lleva paso a paso para configurar y usar la funcionalidad de intercambio de rostros (Face Swap) en Fooocus usando los scripts maestros proporcionados.

## 🚀 Configuración Inicial

### Opción 1: Configuración Automática Completa (Recomendada)

```bash
# 1. Guarda el script maestro como 'fooocus_faceswap_maestro.py'
# 2. Ejecuta desde la terminal:
python fooocus_faceswap_maestro.py --fooocus-path "./Fooocus"

# Si Fooocus está en otra ubicación:
python fooocus_faceswap_maestro.py --fooocus-path "/ruta/a/tu/fooocus"
```

### Opción 2: Configuración Rápida e Interactiva

```bash
# 1. Guarda el script rápido como 'quick_faceswap_setup.py'
# 2. Ejecuta:
python quick_faceswap_setup.py

# 3. Sigue el menú interactivo
```

## 📁 Lo Que Se Crea Automáticamente

Después de ejecutar cualquier script, tendrás esta estructura:

```
Fooocus/
├── models/faceswap/              # 🤖 Modelos de IA
│   ├── inswapper/               # Modelo principal de intercambio
│   ├── face_detection/          # Detección de rostros
│   └── face_recognition/        # Reconocimiento facial
├── inputs/face_images/          # 📸 Coloca aquí rostros fuente
├── outputs/faceswap/           # 🎨 Resultados generados
├── extensions/                 # 🔧 Extensiones personalizadas
├── config/                    # ⚙️ Archivos de configuración
├── temp/faceswap/            # 📂 Archivos temporales
├── launch_faceswap.py        # 🚀 Lanzador Python
├── run_faceswap.bat         # 🎯 Lanzador Windows
└── README_FaceSwap.md       # 📖 Documentación detallada
```

## 🎯 Cómo Usar Face Swap

### Paso 1: Preparar Imágenes

1. **Imagen Fuente** (rostro a copiar):
   - Colócala en `Fooocus/inputs/face_images/`
   - Formato: JPG, PNG, WEBP
   - Resolución recomendada: 512px+ 
   - El rostro debe estar bien iluminado y frontal

2. **Imagen Objetivo** (donde aplicar el rostro):
   - Puede estar en cualquier carpeta
   - Mismas especificaciones de formato
   - Mejor si el rostro objetivo es similar en ángulo

### Paso 2: Ejecutar Fooocus con Face Swap

**Windows:**
```cmd
# Doble clic en:
run_faceswap.bat

# O desde cmd:
cd "C:\ruta\a\Fooocus"
run_faceswap.bat
```

**Linux/Mac:**
```bash
cd /ruta/a/Fooocus
python launch_faceswap.py

# O con argumentos:
python launch_faceswap.py --share --listen 0.0.0.0 --port 7865
```

### Paso 3: Usar la Interfaz

1. **Abrir navegador**: Ve a `http://localhost:7865`

2. **Cargar imágenes**:
   - Imagen objetivo en el campo principal
   - Imagen fuente en la sección "Face Swap"

3. **Ajustar configuración**:
   - Intensidad del swap (0.5-1.0)
   - Mezcla con original (0.5-0.9)
   - Restauración facial (recomendado: ON)

4. **Generar**: Haz clic en "Generate"

5. **Resultado**: Se guarda en `outputs/faceswap/`

## ⚙️ Configuración Avanzada

### Ajustar Parámetros en `config/faceswap_config.json`:

```json
{
  "settings": {
    "face_detection_threshold": 0.5,    // Más bajo = detecta más rostros
    "face_swap_strength": 0.8,          // Intensidad del intercambio
    "blend_ratio": 0.7,                 // Mezcla con imagen original
    "upscale_faces": true,              // Mejora calidad facial
    "restore_faces": true               // Restaura detalles perdidos
  }
}
```

### Optimización de Rendimiento:

```python
# En launch_faceswap.py, agregar argumentos:
os.environ["FOOOCUS_FACE_SWAP_GPU"] = "true"        # Usar GPU
os.environ["FOOOCUS_FACE_SWAP_BATCH"] = "4"         # Procesar en lotes
os.environ["FOOOCUS_MEMORY_OPTIMIZATION"] = "true"   # Optimizar memoria
```

## 🔧 Solución de Problemas

### Problema: "Modelos no encontrados"
```bash
# Solución: Re-descargar modelos
python fooocus_faceswap_maestro.py --fooocus-path "./Fooocus"
```

### Problema: "Error de dependencias"
```bash
# Solución: Instalar manualmente
pip install onnxruntime opencv-python insightface numpy Pillow

# Para GPU (NVIDIA):
pip install onnxruntime-gpu
```

### Problema: "Face Swap no aparece en interfaz"
```bash
# Verificar que se ejecutó correctamente:
python quick_faceswap_setup.py
# Seleccionar opción 3 (verificar instalación)
```

### Problema: "Resultados de baja calidad"
1. **Usar imágenes de mayor resolución** (1024px+)
2. **Ajustar configuración**:
   ```json
   {
     "face_swap_strength": 0.9,
     "blend_ratio": 0.8,
     "upscale_faces": true,
     "restore_faces": true
   }
   ```
3. **Verificar que las caras sean similares** en ángulo e iluminación

## 📊 Requisitos del Sistema

### Mínimos:
- **CPU**: 4 núcleos, 2.5GHz+
- **RAM**: 8GB
- **Storage**: 10GB libres
- **Python**: 3.8+

### Recomendados:
- **GPU**: NVIDIA RTX 2060+ con 8GB VRAM
- **RAM**: 16GB+
- **Storage**: SSD con 20GB+ libres
- **CPU**: 8 núcleos, 3.0GHz+

### Óptimos:
- **GPU**: NVIDIA RTX 4070+ con 12GB+ VRAM
- **RAM**: 32GB+
- **Storage**: NVMe SSD
- **CPU**: 12+ núcleos, 3.5GHz+

## 🎨 Consejos para Mejores Resultados

### Preparación de Imágenes:
1. **Iluminación uniforme** en ambas imágenes
2. **Rostros frontales** o ángulos similares
3. **Evitar oclusiones** (lentes, gorros, máscaras)
4. **Resolución alta** (mínimo 512px, ideal 1024px+)
5. **Formato sin pérdida** (PNG mejor que JPG)

### Configuración Óptima por Escenario:

**Rostros muy similares:**
```json
{
  "face_swap_strength": 0.9,
  "blend_ratio": 0.6,
  "face_detection_threshold": 0.3
}
```

**Rostros diferentes:**
```json
{
  "face_swap_strength": 0.7,
  "blend_ratio": 0.8,
  "face_detection_threshold": 0.6
}
```

**Máxima calidad:**
```json
{
  "face_swap_strength": 0.8,
  "blend_ratio": 0.7,
  "upscale_faces": true,
  "restore_faces": true
}
```

## 🔄 Mantenimiento y Actualizaciones

### Actualizar Modelos:
```bash
# 1. Eliminar modelos antiguos:
rm -rf Fooocus/models/faceswap/

# 2. Re-ejecutar configuración:
python fooocus_faceswap_maestro.py
```

### Limpiar Cache:
```bash
# Eliminar archivos temporales:
rm -rf Fooocus/temp/faceswap/*
```

### Backup de Configuración:
```bash
# Respaldar configuraciones personalizadas:
cp Fooocus/config/faceswap_config.json faceswap_config_backup.json
```

## 🚨 Consideraciones Éticas y Legales

### ⚠️ Uso Responsable:
- **NO crear contenido engañoso** o deepfakes maliciosos
- **Respetar derechos de imagen** de las personas
- **No usar para suplantación** de identidad
- **Cumplir leyes locales** sobre manipulación de imágenes

### ✅ Usos Legítimos:
- Efectos creativos en arte digital
- Pruebas de concepto en desarrollo
- Educación sobre tecnología IA
- Entretenimiento personal responsable

### 📝 Recomendaciones:
- Siempre **obtén consentimiento** antes de usar rostros ajenos
- **Marca claramente** contenido generado con IA
- **No uses para noticias falsas** o desinformación
- **Respeta la privacidad** de las personas

## 📞 Soporte y Recursos

### Enlaces Útiles:
- **Fooocus Oficial**: https://github.com/lllyasviel/Fooocus
- **Documentación IA**: https://huggingface.co/deepinsight
- **Comunidad**: Reddit r/StableDiffusion

### Archivos de Log:
- **Logs de ejecución**: `Fooocus/logs/faceswap.log`
- **Errores de modelos**: `Fooocus/temp/faceswap/errors.log`

### Contacto:
- **Issues técnicos**: Revisa primero README_FaceSwap.md
- **Problemas de instalación**: Ejecuta verificación en script rápido
- **Errores persistentes**: Documenta pasos y logs

---

## 🎉 ¡Listo para Empezar!

Con esta configuración tendrás un sistema completo de Face Swap funcionando en Fooocus. 

**Recuerda**: 
- Usa la tecnología responsablemente
- Experimenta con diferentes configuraciones
- Mantén los modelos actualizados
- ¡Diviértete creando arte digital increíble!

---
*Guía creada por el Sistema de Configuración Automática de Face Swap* 🤖