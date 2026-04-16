# Importar SQLAlchemy para ORM do banco de dados
from flask_sqlalchemy import SQLAlchemy
# Importar UserMixin para integração com Flask-Login
from flask_login import UserMixin
# Importar datetime para campos de data/hora
from datetime import datetime

# Inicializar instância do SQLAlchemy
db = SQLAlchemy()

# ==================== MODELOS ====================

# Modelo para utilizadores do sistema (pode ser admin ou usuário normal)
class Utilizador(db.Model, UserMixin):
    # Nome da tabela no banco de dados
    __tablename__ = 'utilizadores'
    
    # Campo ID - chave primária com autoincremento
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Campo nome do utilizador - obrigatório, até 100 caracteres
    nome = db.Column(db.String(100), nullable=False)
    # Campo email - único e obrigatório, até 150 caracteres
    email = db.Column(db.String(150), unique=True, nullable=False)
    # Campo password - obrigatório, até 255 caracteres (armazena hash)
    password = db.Column(db.String(255), nullable=False)
    # Campo telefone - opcional, até 20 caracteres
    telefone = db.Column(db.String(20))
    # Campo foto de perfil - opcional, caminho da imagem
    foto_perfil = db.Column(db.String(255))
    # Campo tipo - enumeração (user ou admin), padrão é 'user'
    tipo = db.Column(db.Enum('user', 'admin'), default='user')
    # Campo ativo - booleano para verificar se conta está ativa
    ativo = db.Column(db.Boolean, default=True)
    # Campo para token de recuperação de password
    token_recuperacao = db.Column(db.String(255))
    # Campo para data de expiração do token
    token_expiracao = db.Column(db.DateTime)
    # Data de criação do registo
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Data de atualização do registo
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos com outras tabelas
    # Um utilizador pode ter vários anúncios (relação um para muitos)
    anuncios = db.relationship('Anuncio', backref='utilizador', lazy='dynamic', cascade='all, delete-orphan')
    # Um utilizador pode ter vários favoritos
    favoritos = db.relationship('Favorito', backref='utilizador', lazy='dynamic', cascade='all, delete-orphan')
    # Mensagens enviadas pelo utilizador
    mensagens_enviadas = db.relationship('Mensagem', foreign_keys='Mensagem.utilizador_de', backref='remetente', lazy='dynamic')
    # Mensagens recebidas pelo utilizador
    mensagens_recebidas = db.relationship('Mensagem', foreign_keys='Mensagem.utilizador_para', backref='destinatario', lazy='dynamic')
    
    # Sobrescrever método get_id para compatibilidade com Flask-Login
    def get_id(self):
        return str(self.id)
    
    # Método para verificar se o utilizador é admin
    def is_admin(self):
        return self.tipo == 'admin'


# Modelo para categorias de anúncios
class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    # ID da categoria - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Nome da categoria - obrigatório
    nome = db.Column(db.String(100), nullable=False)
    # Slug URL - único para identificação na URL
    slug = db.Column(db.String(100), unique=True, nullable=False)
    # Descrição da categoria - opcional
    descricao = db.Column(db.Text)
    # Ícone da categoria - opcional
    icone = db.Column(db.String(50))
    # ID da categoria pai (para subcategorias)
    parent_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    # Ordem de exibição
    ordem = db.Column(db.Integer, default=0)
    # Se a categoria está ativa
    ativa = db.Column(db.Boolean, default=True)
    # Data de criação
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    # Anúncios pertencentes a esta categoria
    anuncios = db.relationship('Anuncio', backref='categoria', lazy='dynamic')
    # Subcategorias desta categoria
    subcategorias = db.relationship('Categoria', backref=db.backref('parent', remote_side='Categoria.id'))
    
    # Representação em string para debugging
    def __repr__(self):
        return f'<Categoria {self.nome}>'


# Modelo para anúncios de venda/troca
class Anuncio(db.Model):
    __tablename__ = 'anuncios'
    
    # ID do anúncio - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Título do anúncio - obrigatório, até 200 caracteres
    titulo = db.Column(db.String(200), nullable=False)
    # Descrição detalhada do anúncio
    descricao = db.Column(db.Text, nullable=False)
    # Preço do item - formato numérico com 2 casas decimais
    preco = db.Column(db.Numeric(10, 2), default=0)
    # Tipo de anúncio: venda ou troca
    tipo = db.Column(db.Enum('venda', 'troca'), default='venda')
    # Estado do item: novo, usado em bom estado, ou usado regular
    estado = db.Column(db.Enum('novo', 'usado_bueno', 'usado_regular'), default='novo')
    # ID da categoria - chave estrangeira obrigatória
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    # ID do utilizador que criou o anúncio
    utilizador_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    # Localização do item - opcional
    localizacao = db.Column(db.String(150))
    # Contagem de visualizações do anúncio
    views = db.Column(db.Integer, default=0)
    # Status do anúncio: pendente, ativo, rejeitado ou expirado
    status = db.Column(db.Enum('pendente', 'ativo', 'rejeitado', 'expirado'), default='pendente')
    # Motivo da rejeição (se aplicável)
    motivo_rejeicao = db.Column(db.Text)
    # Data de criação do anúncio
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Data de atualização do anúncio
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    # Imagens associadas ao anúncio
    imagens = db.relationship('ImagemAnuncio', backref='anuncio', lazy='dynamic', cascade='all, delete-orphan')
    # Favoritos deste anúncio
    favoritos = db.relationship('Favorito', backref='anuncio', lazy='dynamic', cascade='all, delete-orphan')
    # Mensagens relacionadas ao anúncio
    mensagens = db.relationship('Mensagem', backref='anuncio', lazy='dynamic', cascade='all, delete-orphan')
    # Denúncias deste anúncio
    denuncias = db.relationship('Denuncia', backref='anuncio', lazy='dynamic', cascade='all, delete-orphan')
    
    # Representação em string
    def __repr__(self):
        return f'<Anuncio {self.titulo}>'
    
    # Propriedade para obter a imagem principal do anúncio
    @property
    def imagem_principal(self):
        # Primeiro tenta encontrar imagem marcada como principal
        img = self.imagens.filter_by(principal=True).first()
        # Se não houver, pega a primeira imagem disponível
        if not img:
            img = self.imagens.first()
        return img


# Modelo para imagens dos anúncios
class ImagemAnuncio(db.Model):
    __tablename__ = 'imagens_anuncio'
    
    # ID da imagem - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ID do anúncio associado - chave estrangeira obrigatória
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncios.id'), nullable=False)
    # Nome do arquivo no disco - obrigatório
    arquivo = db.Column(db.String(255), nullable=False)
    # Se é a imagem principal do anúncio
    principal = db.Column(db.Boolean, default=False)
    # Ordem da imagem no anúncio
    ordem = db.Column(db.Integer, default=0)
    # Data de upload
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Representação em string
    def __repr__(self):
        return f'<ImagemAnuncio {self.arquivo}>'


# Modelo para favoritos de anúncios
class Favorito(db.Model):
    __tablename__ = 'favoritos'
    
    # ID do favorito - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ID do utilizador que favoritou - chave estrangeira obrigatória
    utilizador_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    # ID do anúncio favoritado - chave estrangeira obrigatória
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncios.id'), nullable=False)
    # Data quando foi favoritado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Restrição única - um utilizador não pode favoritar o mesmo anúncio duas vezes
    __table_args__ = (db.UniqueConstraint('utilizador_id', 'anuncio_id', name='unique_favorito'),)
    
    # Representação em string
    def __repr__(self):
        return f'<Favorito usuario={self.utilizador_id} anuncio={self.anuncio_id}>'


# Modelo para mensagens entre utilizadores
class Mensagem(db.Model):
    __tablename__ = 'mensagens'
    
    # ID da mensagem - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ID do anúncio relacionado à mensagem - chave estrangeira obrigatória
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncios.id'), nullable=False)
    # ID do utilizador que enviou - chave estrangeira obrigatória
    utilizador_de = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    # ID do utilizador que recebeu - chave estrangeira obrigatória
    utilizador_para = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    # Conteúdo da mensagem - obrigatório
    mensagem = db.Column(db.Text, nullable=False)
    # Se a mensagem foi lida
    lida = db.Column(db.Boolean, default=False)
    # Data de envio
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Representação em string
    def __repr__(self):
        return f'<Mensagem {self.id}>'


# Modelo para denúncias de anúncios
class Denuncia(db.Model):
    __tablename__ = 'denuncias'
    
    # ID da denúncia - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ID do anúncio denunciado - chave estrangeira obrigatória
    anuncio_id = db.Column(db.Integer, db.ForeignKey('anuncios.id'), nullable=False)
    # ID do utilizador que fez a denúncia - chave estrangeira obrigatória
    utilizador_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    # Motivo da denúncia - obrigatório
    motivo = db.Column(db.Text, nullable=False)
    # Descrição adicional
    descricao = db.Column(db.Text)
    # Status da denúncia: pendente, em análise, resolvida ou rejeitada
    status = db.Column(db.Enum('pendente', 'analise', 'resolvida', 'rejeitada'), default='pendente')
    # Data da denúncia
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com utilizador que fez a denúncia
    utilizador = db.relationship('Utilizador', backref='denuncias')
    
    # Representação em string
    def __repr__(self):
        return f'<Denuncia {self.id}>'


# Modelo para logs de ações administrativas
class LogAdmin(db.Model):
    __tablename__ = 'logs_admin'
    
    # ID do log - chave primária
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ID do admin que realizou a ação - chave estrangeira obrigatória
    admin_id = db.Column(db.Integer, db.ForeignKey('utilizadores.id'), nullable=False)
    # Descrição da ação realizada - obrigatória
    acao = db.Column(db.String(100), nullable=False)
    # Nome da tabela afetada
    tabela_afetada = db.Column(db.String(50))
    # ID do registo afetado
    registro_id = db.Column(db.Integer)
    # Detalhes adicionais da ação
    detalhes = db.Column(db.Text)
    # Endereço IP do admin
    ip_address = db.Column(db.String(45))
    # Data da ação
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com o admin
    admin = db.relationship('Utilizador', backref='logs')
    
    # Representação em string
    def __repr__(self):
        return f'<LogAdmin {self.acao}>'
