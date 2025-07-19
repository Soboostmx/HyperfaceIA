# Fooocus Face Swap - Configuración Completa

## 🎭 Descripción
Este setup habilita la funcionalidad de intercambio de rostros (face swap) en Fooocus.

## 🚀 Uso Rápido

### Windows:
```bash
run_faceswap.bat
```

### Linux/Mac:
```bash
python launch_faceswap.py
```

## 📁 Estructura de Archivos

```
Fooocus/
├── models/faceswap/           # Modelos de IA
│   ├── inswapper/            # Modelo principal
│   ├── face_detection/       # Detección de rostros
│   └── face_recognition/     # Reconocimiento facial
├── inputs/face_images/       # Imágenes de rostros fuente
├── outputs/faceswap/         # Resultados generados
├── extensions/               # Extensiones
├── config/                   # Configuraciones
└── temp/faceswap/           # Archivos temporales
```

## ⚙️ Configuración

### Ajustar configuración en `config/faceswap_config.json`:

```json
{
  "settings": {
    "face_detection_threshold": 0.5,    // Sensibilidad detección
    "face_swap_strength": 0.8,          // Intensidad del swap
    "blend_ratio": 0.7,                 // Mezcla con original
    "upscale_faces": true,              // Mejorar calidad
    "restore_faces": true               // Restaurar detalles
  }
}
```

## 🎯 Cómo Usar Face Swap

1. **Preparar imágenes:**
   - Coloca la imagen con el rostro fuente en `inputs/face_images/`
   - Ten lista la imagen objetivo donde aplicar el rostro

2. **Ejecutar:**
   - Inicia Fooocus con `run_faceswap.bat`
   - En la interfaz, selecciona "Face Swap" en las opciones
   - Carga imagen fuente y objetivo
   - Ajusta configuraciones si es necesario
   - Genera imagen

3. **Resultados:**
   - Las imágenes procesadas se guardan en `outputs/faceswap/`

## 🔧 Solución de Problemas

### Error de modelos no encontrados:
- Verifica que los modelos se descargaron en `models/faceswap/`
- Re-ejecuta el script de configuración

### Error de dependencias:
```bash
pip install onnxruntime opencv-python insightface
```

### Performance lento:
- Asegúrate de tener CUDA instalado para usar GPU
- Ajusta `face_detection_threshold` a un valor más alto (0.7-0.9)

## 📊 Requisitos del Sistema

- **RAM:** Mínimo 8GB, recomendado 16GB+
- **GPU:** NVIDIA con CUDA (opcional pero recomendado)
- **Storage:** 10GB+ libres para modelos
- **Python:** 3.8+

## 🎨 Consejos para Mejores Resultados

1. **Calidad de imagen:**
   - Usa imágenes de alta resolución (1024px+)
   - Rostros bien iluminados y frontales
   - Evita rostros con oclusiones (lentes, máscaras)

2. **Configuración óptima:**
   - `face_swap_strength`: 0.7-0.9 para rostros similares
   - `blend_ratio`: 0.6-0.8 para mezcla natural
   - Habilita `restore_faces` para mejor calidad

3. **Post-procesamiento:**
   - Usa herramientas adicionales para refinar bordes
   - Ajusta colores y contraste si es necesario

## 🔄 Actualizaciones

Para actualizar los modelos:
1. Elimina la carpeta `models/faceswap/`
2. Re-ejecuta el script de configuración

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en la consola
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que los modelos se descargaron correctamente

## ⚠️ Consideraciones Éticas

- Usa esta tecnología de manera responsable
- Respeta los derechos de imagen de las personas
- No uses para crear contenido engañoso o malicioso
- Cumple con las leyes locales sobre deepfakes

---
*Configurado automáticamente por el Script Maestro de Face Swap* 🤖
