import pytest
from app import create_app
from app.models import blog_storage
import threading
import time
import os
import stat
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



@pytest.fixture
def app():
    """
    Fixture que crea una instancia de la aplicación para testing
    ¿Qué es un fixture?
    - Función que prepara datos/objetos para las pruebas
    - Se ejecuta antes de cada test que lo necesite
    - Garantiza un estado limpio para cada prueba
    """
    # Crear aplicación en modo testing
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False # Desactivar CSRF para testing
    return app
@pytest.fixture
def client(app):
    """
    Fixture que crea un cliente de testing para hacer peticiones HTTP
    ¿Para qué sirve?
    - Simula un navegador web
    - Permite hacer GET, POST, PUT, DELETE
    - No necesita servidor real corriendo
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Fixture para testing de comandos CLI (si los tuviéramos)
    """
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def reset_storage():
    """
    Fixture que resetea el almacenamiento antes de cada test
    ¿Por qué autouse=True?
    - Se ejecuta automáticamente antes de cada test
    - Garantiza que cada test empiece con datos limpios
    - Evita que los tests se afecten entre sí
    """

    # Limpiar todos los posts
    blog_storage._posts.clear()
    blog_storage._next_id = 1
    
    # Recrear posts de ejemplo para tests consistentes
    blog_storage._create_sample_posts()
    yield # Aquí se ejecuta el test
    # Cleanup después del test (si fuera necesario)
    
    pass

@pytest.fixture(scope="session")
def flask_test_app():
    """Fixture que inicia la aplicación Flask para testing E2E"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    def run_app():
        app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_app, daemon=True)
    server_thread.start()
    time.sleep(3) # Dar más tiempo para que inicie
    yield app

@pytest.fixture
def selenium_driver():
    """Fixture que crea un driver de Chrome para testing"""
    chrome_options = Options()
    # En GitHub Actions y otros entornos CI necesitamos modo headless
    if os.getenv('GITHUB_ACTIONS') or os.getenv('CI'):
        chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_driver_path = ChromeDriverManager().install()
    # webdriver_manager puede devolver una ruta a un archivo dentro del directorio
    # de descarga; buscamos el ejecutable correcto según el sistema.
    if os.path.isdir(chrome_driver_path):
        search_dir = chrome_driver_path
    else:
        search_dir = os.path.dirname(chrome_driver_path)

    executable_names = ['chromedriver.exe', 'chromedriver']
    for exe_name in executable_names:
        candidate = os.path.join(search_dir, exe_name)
        if os.path.exists(candidate):
            chrome_driver_path = candidate
            break

    # Asegurar permisos de ejecución en Linux/Unix
    if os.name != 'nt':
        st = os.stat(chrome_driver_path)
        os.chmod(chrome_driver_path, st.st_mode | stat.S_IEXEC)

        # Usar Chromium en CI si está instalado
        if os.path.exists('/usr/bin/chromium-browser'):
            chrome_options.binary_location = '/usr/bin/chromium-browser'
        elif os.path.exists('/usr/bin/chromium'):
            chrome_options.binary_location = '/usr/bin/chromium'
        elif os.path.exists('/usr/bin/google-chrome-stable'):
            chrome_options.binary_location = '/usr/bin/google-chrome-stable'

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def e2e_base_url():
    """URL base para los tests E2E (nombre diferente para evitar
    conflictos)"""
    return "http://127.0.0.1:5001"






