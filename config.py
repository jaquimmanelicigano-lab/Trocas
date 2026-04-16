# Importar módulos necessários do sistema operacional para variáveis de ambiente
import os
# Importar load_dotenv para carregar variáveis do arquivo .env
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Classe de configuração base que contém todas as definições de configuração da aplicação
class Config:
    # Chave secreta usada para sessões e proteção CSRF - usa variável de ambiente ou fallback
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'trocas-flask-secret-key-2024'
    
    # Configurações do banco de dados - usam SQLite para simplicidade
    # MYSQL_HOST = os.environ.get('DB_HOST') or 'localhost'
    # MYSQL_USER = os.environ.get('DB_USER') or 'root'
    # MYSQL_PASSWORD = os.environ.get('DB_PASSWORD') or ''
    # MYSQL_DB = os.environ.get('DB_NAME') or 'trocas_db'
    
    # URI de conexão SQLAlchemy - usa variável DATABASE_URL (PostgreSQL no Render) ou MySQL local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:teste123@127.0.0.1:3306/trocas_db'
    # Desativar rastreamento de modificações para melhor desempenho
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de upload de arquivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'public', 'images', 'uploads')
    # Limite máximo de tamanho de arquivo: 16MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    # Extensões de imagem permitidas para upload
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configurações de sessão
    SESSION_TYPE = 'filesystem'
    # Tempo de vida da sessão: 86400 segundos = 24 horas
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

    # Configurações de email (SMTP)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or ''
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or ''

# Configuração de desenvolvimento - ativa modo debug
class DevelopmentConfig(Config):
    DEBUG = True

# Configuração de produção - desativa modo debug
class ProductionConfig(Config):
    DEBUG = False

# Dicionário de configurações disponíveis para a aplicação
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
