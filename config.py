# Configuración de Base de Datos MySQL - Hardcoded
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DB = 'LIAN_REPUESTOS'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306

# SQLAlchemy URI
SQLALCHEMY_DATABASE_URI = (
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}'
    f'@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret Key para sesiones Flask
SECRET_KEY = 'lian_repuestos_secret_key_2024'
