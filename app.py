from app import create_app
from config import Config
import os
# Crear la aplicación usando la factory function
app = create_app()
if __name__ == '__main__':
    """
    Punto de entrada de la aplicación
    ¿Qué hace if __name__ == '__main__'?
    - Solo se ejecuta si corres este archivo directamente
    - No se ejecuta si importas este archivo desde otro lugar
    - Patrón estándar en Python
    """
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    print(f"Iniciando DevBlog...")
    print(f"Puerto: {port}")
    print(f"Debug: {debug}")
    print(f"Entorno: {os.environ.get('FLASK_ENV', 'development')}")

    # Iniciar el servidor Flask
    app.run(
        host='0.0.0.0', # 0.0.0.0 permite conexiones externas
        port=port, # Puerto configurado (5000 por defecto)
        debug=debug # Modo debug para desarrollo
    )
