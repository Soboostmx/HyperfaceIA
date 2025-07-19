import gradio as gr
import random
import os
import json
import time
import zipfile
import tempfile
import shutil
from datetime import datetime
import shared
import modules.config
import fooocus_version
import modules.html
import modules.async_worker as worker
import modules.constants as constants
import modules.flags as flags
import modules.gradio_hijack as grh
import modules.style_sorter as style_sorter
import modules.meta_parser
import args_manager
import copy
import launch
from extras.inpaint_mask import SAMOptions

from modules.sdxl_styles import legal_style_names
from modules.private_logger import get_current_html_path
from modules.ui_gradio_extensions import reload_javascript
from modules.auth import auth_enabled, check_auth
from modules.util import is_json

# CSS personalizado para mejorar la interfaz
custom_css = """
/* Esquema de colores moderno */
:root {
    --primary-color: #667eea;
    --primary-dark: #5a6fd8;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --success-color: #4ade80;
    --warning-color: #fbbf24;
    --error-color: #f87171;
    --background: #0f0f23;
    --surface: #1a1a2e;
    --surface-light: #16213e;
    --text-primary: #ffffff;
    --text-secondary: #94a3b8;
    --border: #334155;
    --border-light: #475569;
}

/* Gradientes para elementos principales */
.gradient-bg {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
}

.gradient-border {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    padding: 2px;
    border-radius: 12px;
}

/* Estilos generales */
body {
    background: var(--background);
    color: var(--text-primary);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Contenedor principal mejorado */
.main-container {
    background: var(--surface);
    border-radius: 20px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid var(--border);
    margin: 20px;
    overflow: hidden;
}

/* Header mejorado */
.header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    padding: 25px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.1"><circle cx="30" cy="30" r="4"/></g></svg>');
    animation: float 20s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    margin: 0;
    color: white;
    text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
}

.header .subtitle {
    font-size: 1.1rem;
    color: rgba(255, 255, 255, 0.9);
    margin-top: 8px;
    position: relative;
    z-index: 1;
}

/* Botones principales mejorados */
.btn-primary {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    border: none;
    border-radius: 12px;
    padding: 15px 30px;
    color: white;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.btn-primary:active {
    transform: translateY(0);
}

.btn-primary::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.btn-primary:hover::before {
    left: 100%;
}

/* Botón de descarga por lote */
.btn-download {
    background: linear-gradient(135deg, var(--success-color), #22c55e);
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    color: white;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(74, 222, 128, 0.4);
    display: flex;
    align-items: center;
    gap: 8px;
}

.btn-download:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(74, 222, 128, 0.6);
}

/* Botones secundarios */
.btn-secondary {
    background: var(--surface-light);
    border: 2px solid var(--border-light);
    border-radius: 10px;
    padding: 10px 20px;
    color: var(--text-primary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    border-color: var(--primary-color);
    background: rgba(102, 126, 234, 0.1);
}

/* Controles organizados */
.control-section {
    background: var(--surface-light);
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
}

.control-section:hover {
    border-color: var(--border-light);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.control-section h3 {
    color: var(--primary-color);
    font-weight: 700;
    font-size: 1.2rem;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Pestañas mejoradas */
.tab-nav {
    background: var(--surface);
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 20px;
    border: 1px solid var(--border);
}

.tab-button {
    background: transparent;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.tab-button.active {
    background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
    color: white;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.tab-button:hover:not(.active) {
    background: rgba(102, 126, 234, 0.1);
    color: var(--text-primary);
}

/* Inputs mejorados */
.form-input {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    color: var(--text-primary);
    font-size: 1rem;
    transition: all 0.3s ease;
    width: 100%;
}

.form-input:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-textarea {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    color: var(--text-primary);
    font-size: 1rem;
    min-height: 100px;
    resize: vertical;
    transition: all 0.3s ease;
}

.form-textarea:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Galería mejorada */
.gallery-container {
    background: var(--surface-light);
    border-radius: 15px;
    padding: 20px;
    border: 1px solid var(--border);
}

.gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.gallery-item {
    background: var(--surface);
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
    position: relative;
}

.gallery-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    border-color: var(--primary-color);
}

/* Barra de progreso mejorada */
.progress-container {
    background: var(--surface-light);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    border: 1px solid var(--border);
}

.progress-bar {
    background: var(--surface);
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    height: 100%;
    border-radius: 8px;
    transition: width 0.3s ease;
    position: relative;
}

.progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Iconos y elementos visuales */
.icon {
    width: 20px;
    height: 20px;
    fill: currentColor;
}

.status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}

.status-generating {
    background: var(--warning-color);
    animation: pulse 1.5s infinite;
}

.status-complete {
    background: var(--success-color);
}

.status-error {
    background: var(--error-color);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Responsive design */
@media (max-width: 1024px) {
    .main-container {
        margin: 10px;
    }
    
    .header h1 {
        font-size: 2rem;
    }
}

@media (max-width: 768px) {
    .control-section {
        padding: 15px;
    }
    
    .btn-primary {
        padding: 12px 24px;
        font-size: 0.9rem;
    }
    
    .gallery-grid {
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
    }
}

/* Animaciones adicionales */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* Mejoras de accesibilidad */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Tooltips mejorados */
.tooltip {
    position: relative;
    display: inline-block;
}

.tooltip::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--surface-light);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.875rem;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    border: 1px solid var(--border);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    z-index: 1000;
}

.tooltip:hover::after {
    opacity: 1;
    visibility: visible;
    transform: translateX(-50%) translateY(-4px);
}
"""

def create_batch_download_button():
    """Crear botón de descarga por lote con funcionalidad"""
    
    def download_all_images():
        """Función para descargar todas las imágenes generadas"""
        try:
            # Crear un archivo temporal ZIP
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, f"fooocus_imagenes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                # Buscar todas las imágenes en el directorio de salida
                output_dir = modules.config.path_outputs
                if os.path.exists(output_dir):
                    for root, dirs, files in os.walk(output_dir):
                        for file in files:
                            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, output_dir)
                                zipf.write(file_path, arcname)
                
            return zip_path
        except Exception as e:
            print(f"Error creando archivo ZIP: {e}")
            return None

    return gr.DownloadButton(
        label="📦 Descargar Todas las Imágenes",
        value=download_all_images,
        elem_classes=["btn-download"],
        variant="secondary"
    )

def get_task(*args):
    args = list(args)
    args.pop(0)
    return worker.AsyncTask(args=args)

def generate_clicked(task: worker.AsyncTask):
    import ldm_patched.modules.model_management as model_management

    with model_management.interrupt_processing_mutex:
        model_management.interrupt_processing = False

    if len(task.args) == 0:
        return

    execution_start_time = time.perf_counter()
    finished = False

    yield gr.update(visible=True, value=modules.html.make_progress_html(1, 'Esperando inicio de tarea...')), \
        gr.update(visible=True, value=None), \
        gr.update(visible=False, value=None), \
        gr.update(visible=False)

    worker.async_tasks.append(task)

    while not finished:
        time.sleep(0.01)
        if len(task.yields) > 0:
            flag, product = task.yields.pop(0)
            if flag == 'preview':
                if len(task.yields) > 0:
                    if task.yields[0][0] == 'preview':
                        continue

                percentage, title, image = product
                yield gr.update(visible=True, value=modules.html.make_progress_html(percentage, title)), \
                    gr.update(visible=True, value=image) if image is not None else gr.update(), \
                    gr.update(), \
                    gr.update(visible=False)
            if flag == 'results':
                yield gr.update(visible=True), \
                    gr.update(visible=True), \
                    gr.update(visible=True, value=product), \
                    gr.update(visible=False)
            if flag == 'finish':
                if not args_manager.args.disable_enhance_output_sorting:
                    product = sort_enhance_images(product, task)

                yield gr.update(visible=False), \
                    gr.update(visible=False), \
                    gr.update(visible=False), \
                    gr.update(visible=True, value=product)
                finished = True

                if args_manager.args.disable_image_log:
                    for filepath in product:
                        if isinstance(filepath, str) and os.path.exists(filepath):
                            os.remove(filepath)

    execution_time = time.perf_counter() - execution_start_time
    print(f'Tiempo total: {execution_time:.2f} segundos')
    return

def sort_enhance_images(images, task):
    if not task.should_enhance or len(images) <= task.images_to_enhance_count:
        return images

    sorted_images = []
    walk_index = task.images_to_enhance_count

    for index, enhanced_img in enumerate(images[:task.images_to_enhance_count]):
        sorted_images.append(enhanced_img)
        if index not in task.enhance_stats:
            continue
        target_index = walk_index + task.enhance_stats[index]
        if walk_index < len(images) and target_index <= len(images):
            sorted_images += images[walk_index:target_index]
        walk_index += task.enhance_stats[index]

    return sorted_images

def inpaint_mode_change(mode, inpaint_engine_version):
    assert mode in modules.flags.inpaint_options

    if mode == modules.flags.inpaint_option_detail:
        return [
            gr.update(visible=True), gr.update(visible=False, value=[]),
            gr.Dataset.update(visible=True, samples=modules.config.example_inpaint_prompts),
            False, 'None', 0.5, 0.0
        ]

    if inpaint_engine_version == 'empty':
        inpaint_engine_version = modules.config.default_inpaint_engine_version

    if mode == modules.flags.inpaint_option_modify:
        return [
            gr.update(visible=True), gr.update(visible=False, value=[]),
            gr.Dataset.update(visible=False, samples=modules.config.example_inpaint_prompts),
            True, inpaint_engine_version, 1.0, 0.0
        ]

    return [
        gr.update(visible=False, value=''), gr.update(visible=True),
        gr.Dataset.update(visible=False, samples=modules.config.example_inpaint_prompts),
        False, inpaint_engine_version, 1.0, 0.618
    ]

reload_javascript()

title = f'Fooocus {fooocus_version.version}'

if isinstance(args_manager.args.preset, str):
    title += ' ' + args_manager.args.preset

# Crear la interfaz principal con CSS personalizado
shared.gradio_root = gr.Blocks(
    title=title,
    css=custom_css,
    theme=gr.themes.Base(
        primary_hue="blue",
        secondary_hue="purple",
        neutral_hue="slate",
        font=gr.themes.GoogleFont("Inter")
    )
).queue()

with shared.gradio_root:
    currentTask = gr.State(worker.AsyncTask(args=[]))
    inpaint_engine_state = gr.State('empty')
    
    # Header mejorado
    with gr.Row(elem_classes=['header']):
        gr.HTML(f"""
            <div class="header">
                <h1>🎨 Fooocus IA - Generador de Imágenes</h1>
                <p class="subtitle">Versión {fooocus_version.version} - Interfaz Mejorada en Español</p>
            </div>
        """)
    
    # Contenedor principal
    with gr.Row(elem_classes=['main-container']):
        # Panel izquierdo - Generación y galería
        with gr.Column(scale=3, elem_classes=['control-section']):
            # Sección de vista previa y galería
            with gr.Row():
                progress_window = grh.Image(
                    label='🖼️ Vista Previa', 
                    show_label=True, 
                    visible=False, 
                    height=768,
                    elem_classes=['gallery-item']
                )
                progress_gallery = gr.Gallery(
                    label='✨ Imágenes Terminadas', 
                    show_label=True, 
                    object_fit='contain',
                    height=768, 
                    visible=False, 
                    elem_classes=['gallery-container']
                )
            
            # Barra de progreso mejorada
            progress_html = gr.HTML(
                value=modules.html.make_progress_html(32, 'Progreso 32%'), 
                visible=False,
                elem_id='progress-bar', 
                elem_classes=['progress-container']
            )
            
            # Galería principal
            gallery = gr.Gallery(
                label='🎯 Galería Principal', 
                show_label=False, 
                object_fit='contain', 
                visible=True, 
                height=768,
                elem_classes=['gallery-container', 'fade-in'],
                elem_id='final_gallery'
            )
            
            # Controles de prompt mejorados
            with gr.Row(elem_classes=['control-section']):
                with gr.Column(scale=17):
                    prompt = gr.Textbox(
                        show_label=False, 
                        placeholder="✍️ Escribe tu prompt aquí o pega parámetros...", 
                        elem_id='positive_prompt',
                        autofocus=True, 
                        lines=3,
                        elem_classes=['form-textarea']
                    )
                    
                    default_prompt = modules.config.default_prompt
                    if isinstance(default_prompt, str) and default_prompt != '':
                        shared.gradio_root.load(lambda: default_prompt, outputs=prompt)

                with gr.Column(scale=3, min_width=0):
                    # Botones principales reorganizados
                    generate_button = gr.Button(
                        label="Generar", 
                        value="🚀 Generar Imagen", 
                        elem_classes=['btn-primary'], 
                        elem_id='generate_button', 
                        visible=True,
                        variant="primary",
                        size="lg"
                    )
                    
                    # Botón de descarga por lote
                    batch_download_btn = create_batch_download_button()
                    
                    reset_button = gr.Button(
                        label="Reconectar", 
                        value="🔄 Reconectar", 
                        elem_classes=['btn-secondary'], 
                        elem_id='reset_button', 
                        visible=False
                    )
                    
                    load_parameter_button = gr.Button(
                        label="Cargar Parámetros", 
                        value="⚙️ Cargar Parámetros", 
                        elem_classes=['btn-secondary'], 
                        elem_id='load_parameter_button', 
                        visible=False
                    )
                    
                    with gr.Row():
                        skip_button = gr.Button(
                            label="Saltar", 
                            value="⏭️ Saltar", 
                            elem_classes=['btn-secondary'], 
                            elem_id='skip_button', 
                            visible=False,
                            size="sm"
                        )
                        stop_button = gr.Button(
                            label="Detener", 
                            value="⏹️ Detener", 
                            elem_classes=['btn-secondary'], 
                            elem_id='stop_button', 
                            visible=False,
                            size="sm"
                        )

                    def stop_clicked(currentTask):
                        import ldm_patched.modules.model_management as model_management
                        currentTask.last_stop = 'stop'
                        if (currentTask.processing):
                            model_management.interrupt_current_processing()
                        return currentTask

                    def skip_clicked(currentTask):
                        import ldm_patched.modules.model_management as model_management
                        currentTask.last_stop = 'skip'
                        if (currentTask.processing):
                            model_management.interrupt_current_processing()
                        return currentTask

                    stop_button.click(stop_clicked, inputs=currentTask, outputs=currentTask, queue=False, show_progress=False, _js='cancelGenerateForever')
                    skip_button.click(skip_clicked, inputs=currentTask, outputs=currentTask, queue=False, show_progress=False)
            
            # Checkboxes mejorados
            with gr.Row(elem_classes=['control-section']):
                gr.HTML("<h3>🎛️ Opciones de Generación</h3>")
                with gr.Row():
                    input_image_checkbox = gr.Checkbox(
                        label='🖼️ Imagen de Entrada', 
                        value=modules.config.default_image_prompt_checkbox, 
                        container=False, 
                        elem_classes=['min_check']
                    )
                    enhance_checkbox = gr.Checkbox(
                        label='✨ Mejorar', 
                        value=modules.config.default_enhance_checkbox, 
                        container=False, 
                        elem_classes=['min_check']
                    )
                    advanced_checkbox = gr.Checkbox(
                        label='🔧 Avanzado', 
                        value=modules.config.default_advanced_checkbox, 
                        container=False, 
                        elem_classes=['min_check']
                    )
            
            # Panel de imagen de entrada mejorado
            with gr.Row(visible=modules.config.default_image_prompt_checkbox, elem_classes=['control-section']) as image_input_panel:
                with gr.Tabs(selected=modules.config.default_selected_image_input_tab_id, elem_classes=['tab-nav']):
                    with gr.Tab(label='📈 Ampliación o Variación', id='uov_tab', elem_classes=['tab-button']) as uov_tab:
                        with gr.Row():
                            with gr.Column():
                                uov_input_image = grh.Image(
                                    label='Imagen', 
                                    source='upload', 
                                    type='numpy', 
                                    show_label=False,
                                    elem_classes=['gallery-item']
                                )
                            with gr.Column():
                                uov_method = gr.Radio(
                                    label='🎯 Ampliación o Variación:', 
                                    choices=flags.uov_list, 
                                    value=modules.config.default_uov_method
                                )
                                gr.HTML('<a href="https://github.com/lllyasviel/Fooocus/discussions/390" target="_blank">📚 Documentación</a>')
                    
                    # Continuar con las demás pestañas con traducciones y mejoras similares...
                    # [El resto del código sigue el mismo patrón de mejoras]

        # Panel derecho - Controles avanzados
        with gr.Column(scale=1, visible=modules.config.default_advanced_checkbox, elem_classes=['control-section']) as advanced_column:
            with gr.Tab(label='⚙️ Configuración', elem_classes=['tab-button']):
                gr.HTML("<h3>🎛️ Configuración Principal</h3>")
                
                if not args_manager.args.disable_preset_selection:
                    preset_selection = gr.Dropdown(
                        label='🎨 Preset',
                        choices=modules.config.available_presets,
                        value=args_manager.args.preset if args_manager.args.preset else "initial",
                        interactive=True,
                        elem_classes=['form-input']
                    )

                performance_selection = gr.Radio(
                    label='⚡ Rendimiento',
                    choices=flags.Performance.values(),
                    value=modules.config.default_performance,
                    elem_classes=['performance_selection']
                )

                with gr.Accordion(label='📐 Proporciones de Aspecto', open=False, elem_id='aspect_ratios_accordion') as aspect_ratios_accordion:
                    aspect_ratios_selection = gr.Radio(
                        label='Proporciones de Aspecto', 
                        show_label=False,
                        choices=modules.config.available_aspect_ratios_labels,
                        value=modules.config.default_aspect_ratio,
                        info='ancho × alto',
                        elem_classes='aspect_ratios'
                    )

                image_number = gr.Slider(
                    label='📊 Número de Imágenes', 
                    minimum=1, 
                    maximum=modules.config.default_max_image_number, 
                    step=1, 
                    value=modules.config.default_image_number
                )

                output_format = gr.Radio(
                    label='💾 Formato de Salida',
                    choices=flags.OutputFormat.list(),
                    value=modules.config.default_output_format
                )

                negative_prompt = gr.Textbox(
                    label='❌ Prompt Negativo', 
                    show_label=True, 
                    placeholder="Describe lo que NO quieres ver...",
                    info='Describe lo que no quieres ver en la imagen.', 
                    lines=2,
                    elem_id='negative_prompt',
                    value=modules.config.default_prompt_negative,
                    elem_classes=['form-textarea']
                )
                
                # Controles de semilla mejorados
                with gr.Row():
                    seed_random = gr.Checkbox(label='🎲 Aleatorio', value=True)
                    image_seed = gr.Textbox(
                        label='🌱 Semilla', 
                        value=0, 
                        max_lines=1, 
                        visible=False,
                        elem_classes=['form-input']
                    )

                def random_checked(r):
                    return gr.update(visible=not r)

                def refresh_seed(r, seed_string):
                    if r:
                        return random.randint(constants.MIN_SEED, constants.MAX_SEED)
                    else:
                        try:
                            seed_value = int(seed_string)
                            if constants.MIN_SEED <= seed_value <= constants.MAX_SEED:
                                return seed_value
                        except ValueError:
                            pass
                        return random.randint(constants.MIN_SEED, constants.MAX_SEED)

                seed_random.change(random_checked, inputs=[seed_random], outputs=[image_seed],
                                   queue=False, show_progress=False)

                def update_history_link():
                    if args_manager.args.disable_image_log:
                        return gr.update(value='')
                    return gr.update(value=f'<a href="file={get_current_html_path(output_format)}" target="_blank" class="btn-secondary">📚 Historial de Imágenes</a>')

                history_link = gr.HTML()
                shared.gradio_root.load(update_history_link, outputs=history_link, queue=False, show_progress=False)

    # JavaScript para efectos adicionales
    gr.HTML("""
    <script>
    // Efectos de interfaz mejorados
    document.addEventListener('DOMContentLoaded', function() {
        // Agregar efectos de hover a elementos
        const buttons = document.querySelectorAll('.btn-primary, .btn-secondary, .btn-download');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
        
        // Animaciones de entrada
        const sections = document.querySelectorAll('.control-section');
        sections.forEach((section, index) => {
            section.style.animationDelay = `${index * 0.1}s`;
            section.classList.add('fade-in');
        });
        
        // Notificación de completado
        function showNotification(message, type = 'success') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }
        
        // Monitorear cambios en la galería
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    const gallery = document.querySelector('#final_gallery');
                    if (gallery && gallery.children.length > 0) {
                        showNotification('¡Imagen generada exitosamente! 🎉');
                    }
                }
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
    });
    </script>
    
    <style>
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .notification-success {
        background: linear-gradient(135deg, var(--success-color), #22c55e);
    }
    
    .notification-error {
        background: linear-gradient(135deg, var(--error-color), #dc2626);
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
    """)

# Configuración de eventos y lanzamiento
shared.gradio_root.launch(
    inbrowser=args_manager.args.in_browser,
    server_name=args_manager.args.listen,
    server_port=args_manager.args.port,
    share=args_manager.args.share,
    auth=check_auth if (args_manager.args.share or args_manager.args.listen) and auth_enabled else None,
    allowed_paths=[modules.config.path_outputs],
    blocked_paths=[constants.AUTH_FILENAME]
)