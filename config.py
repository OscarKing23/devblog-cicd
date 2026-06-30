import os

class Config:
    # Clave secreta para sesiones y formularios
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # configuracion para el modo debug
    # true = muestra errores detallados, recarga automatica
    # false = modo producción, no muestra errores detallados
    DEBUG = os.environ.get('FLASK_DEBUG') or True

    # Puerto donde correra la aplicación
    PORT = int(os.environ.get('PORT', 5000))

    # Host - 0.0.0.0 permite conexiones externas (necesario para docker)
    HOST = os.environ.get('HOST', '0.0.0.0')
    

    
