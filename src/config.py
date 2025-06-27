class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST= 'localhost'
    MYSQL_USER= 'Administrador'
    MYSQL_PASSWORD= '1234'
    MYSQL_PORT = 3307
    MYSQL_DB= 'tpi_programacion'
    
config = {
    'development': DevelopmentConfig
}