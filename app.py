# Importar módulo os para operações de sistema de arquivos
import os
# Importar classes do Flask para criar aplicação web
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
# Importar classes do Flask-Login para autenticação
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# Importar Flask-WTF para formulários
from flask_wtf import FlaskForm
# Importar proteção CSRF
from flask_wtf.csrf import CSRFProtect
# Importar campos de formulário do WTForms
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FileField, DecimalField
# Importar validadores de formulários
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
# Importar função para nome seguro de arquivos
from werkzeug.utils import secure_filename
# Importar funções de hash de passwords
from werkzeug.security import generate_password_hash, check_password_hash
# Importar classes de data/hora
from datetime import datetime, timedelta
# Importar configurações
from config import config
# Importar modelos do banco de dados
from models import db, Utilizador, Categoria, Anuncio, ImagemAnuncio, Favorito, Mensagem, Denuncia, LogAdmin
# Importar utilities de email
from utils.email_utils import send_welcome_email, send_password_reset_email, send_account_confirmation_with_token
# Importar bcrypt para geração de tokens
import bcrypt

# Inicializar Flask - criar aplicação web
# template_folder aponta para pasta de templates HTML
# static_folder aponta para arquivos estáticos (CSS, JS, imagens)
app = Flask(__name__, template_folder='src/views', static_folder='src/public')
# Carregar configurações baseadas no ambiente (desenvolvimento ou produção)
app.config.from_object(config[os.getenv('FLASK_ENV', 'default')])

# Inicializar extensões do Flask
# db - ORM para banco de dados
db.init_app(app)
# Mostrar a URL para debug
print(f"DEBUG: SQLALCHEMY_DATABASE_URI = {app.config.get('SQLALCHEMY_DATABASE_URI')}")
with app.app_context():
    db.create_all()
    print("DEBUG: Base de dados criada/verificada")
# csrf - proteção contra ataques CSRF
csrf = CSRFProtect(app)
# login_manager - gerenciador de autenticação
login_manager = LoginManager()
# Inicializar login_manager com a aplicação
login_manager.init_app(app)
# Definir rota de login como padrão
login_manager.login_view = 'login'
# Mensagem exibida quando utilizador não está autenticado
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# Função para carregar utilizador da sessão
@login_manager.user_loader
def load_user(user_id):
    # Retorna utilizador pelo ID ou None se não existir
    return Utilizador.query.get(int(user_id))

# ==================== FORMULÁRIOS WTForms ====================

# Formulário de registo de novos utilizadores
class RegistrationForm(FlaskForm):
    # Campo nome - obrigatório, entre 2 e 100 caracteres
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    # Campo email - obrigatório, validado como email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Campo telefone - obrigatório
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=9, max=20)])
    # Campo password - obrigatório, mínimo 6 caracteres
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    # Campo confirmação de password - obrigatório, deve ser igual ao campo password
    confirm_password = PasswordField('Confirmar Password', validators=[DataRequired(), EqualTo('password')])

# Formulário de login
class LoginForm(FlaskForm):
    # Campo email - obrigatório, validado como email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Campo password - obrigatório
    password = PasswordField('Password', validators=[DataRequired()])

# Formulário de edição de perfil
class ProfileForm(FlaskForm):
    # Campo nome - obrigatório, entre 2 e 100 caracteres
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    # Campo telefone - opcional
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    # Campo foto de perfil - arquivo opcional
    foto_perfil = FileField('Foto de Perfil', validators=[Optional()])

# Formulário de criação/edição de anúncios
class AdForm(FlaskForm):
    # Campo título - obrigatório, entre 3 e 200 caracteres
    titulo = StringField('Título', validators=[DataRequired(), Length(min=3, max=200)])
    # Campo descrição - obrigatório, mínimo 10 caracteres
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(min=10)])
    # Campo preço - obrigatório, número decimal
    preco = DecimalField('Preço', validators=[DataRequired()])
    # Campo tipo - venda ou troca
    tipo = SelectField('Tipo', choices=[('venda', 'Venda'), ('troca', 'Troca')])
    # Campo estado - novo, usado bom ou usado regular
    estado = SelectField('Estado', choices=[('novo', 'Novo'), ('usado_bueno', 'Usado - Bom'), ('usado_regular', 'Usado - Regular')])
    # Campo categoria - obrigatório, ID da categoria
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    # Campo localização - opcional, máximo 150 caracteres
    localizacao = StringField('Localização', validators=[Optional(), Length(max=150)])

# Formulário de envio de mensagens
class MessageForm(FlaskForm):
    # Campo mensagem - obrigatório, mínimo 1 caractere
    mensagem = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=1)])

# Formulário de recuperação de password
class ForgotPasswordForm(FlaskForm):
    # Campo email - obrigatório, validado como email
    email = StringField('Email', validators=[DataRequired(), Email()])

# ==================== HELPER FUNCTIONS ====================

# Função para verificar se extensão de arquivo é permitida
def allowed_file(filename):
    # Verifica se tem extensão e se está na lista de permitidas
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para salvar imagem no disco
def save_image(file):
    # Verificar se arquivo é válido e tem extensão permitida
    if file and allowed_file(file.filename):
        # Garantir nome seguro do arquivo
        filename = secure_filename(file.filename)
        # Adicionar timestamp para evitar nomes duplicados
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # Criar pasta de upload se não existir
        upload_path = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, exist_ok=True)
        
        # Combinar caminho com nome do arquivo
        filepath = os.path.join(upload_path, filename)
        # Salvar arquivo no disco
        file.save(filepath)
        # Retornar nome do arquivo salvo
        return filename
    # Retornar None se não foi possível salvar
    return None

# Função para registrar ações de administrador
def log_admin_action(acao, tabela_afetada=None, registro_id=None, detalhes=None):
    # Verificar se utilizador está autenticado e é admin
    if current_user.is_authenticated and current_user.is_admin():
        # Criar novo registo de log
        log = LogAdmin(
            admin_id=current_user.id,
            acao=acao,
            tabela_afetada=tabela_afetada,
            registro_id=registro_id,
            detalhes=detalhes,
            ip_address=request.remote_addr
        )
        # Adicionar e salvar no banco de dados
        db.session.add(log)
        db.session.commit()

# Função para obter todas as categorias ativas
def get_categories():
    # Retorna categorias ordenadas por ordem
    return Categoria.query.filter_by(ativa=True).order_by(Categoria.ordem).all()

# Função para verificar se anúncio é favorito do utilizador atual
def is_favorite(anuncio_id):
    # Só verifica se utilizador estiver autenticado
    if current_user.is_authenticated:
        # Consulta se existe favorito para este utilizador e anúncio
        return Favorito.query.filter_by(utilizador_id=current_user.id, anuncio_id=anuncio_id).first() is not None
    return False

# ==================== CONTEXT PROCESSORS ====================

# Injetar categorias em todos os templates automaticamente
@app.context_processor
def inject_categories():
    return dict(categorias=get_categories())

# ==================== ROTAS PÚBLICAS ====================

# Rota da página inicial
@app.route('/')
def home():
    # Buscar anúncios ativos mais recentes - limite de 12
    anuncios = Anuncio.query.filter_by(status='ativo').order_by(Anuncio.created_at.desc()).limit(12).all()
    
    # Buscar categorias ativas
    categorias = get_categories()
    
    # Contagens para estatísticas na homepage
    total_anuncios = Anuncio.query.filter_by(status='ativo').count()
    total_utilizadores = Utilizador.query.filter_by(tipo='user', ativo=True).count()
    
    # Renderizar template da página inicial
    return render_template('index.html',
                          anuncios=anuncios,
                          categorias=categorias,
                          total_anuncios=total_anuncios,
                          total_utilizadores=total_utilizadores)

# Rota do Centro de Suporte / FAQ
@app.route('/suporte')
def support():
    return render_template('support.html')
    
    # Renderizar template com dados
    return render_template('index.html',
                         anuncios=anuncios,
                         categorias=categorias,
                         total_anuncios=total_anuncios,
                         total_utilizadores=total_utilizadores)

# Rota de pesquisa de anúncios
@app.route('/pesquisar', methods=['GET', 'POST'])
def search():
    # Obter parâmetros da query string
    query = request.args.get('q', '')
    categoria_id = request.args.get('categoria', type=int)
    tipo = request.args.get('tipo')
    localizacao = request.args.get('localizacao')
    
    # Começar com anúncios ativos
    ads_query = Anuncio.query.filter_by(status='ativo')
    
    # Filtrar por texto de pesquisa (título ou descrição)
    if query:
        ads_query = ads_query.filter(
            db.or_(
                Anuncio.titulo.ilike(f'%{query}%'),
                Anuncio.descricao.ilike(f'%{query}%')
            )
        )
    
    # Filtrar por categoria se especificada
    if categoria_id:
        ads_query = ads_query.filter_by(categoria_id=categoria_id)
    
    # Filtrar por tipo (venda ou troca)
    if tipo:
        ads_query = ads_query.filter_by(tipo=tipo)
    
    # Filtrar por localização
    if localizacao:
        ads_query = ads_query.filter(Anuncio.localizacao.ilike(f'%{localizacao}%'))
    
    # Ordenar por data de criação (mais recentes primeiro)
    anuncios = ads_query.order_by(Anuncio.created_at.desc()).all()
    categorias = get_categories()
    
    # Renderizar template de pesquisa
    return render_template('search.html',
                         anuncios=anuncios,
                         categorias=categorias,
                         query=query,
                         selected_categoria=categoria_id,
                         selected_tipo=tipo,
                         selected_localizacao=localizacao)

# Rota para visualizar um anúncio específico
@app.route('/anuncio/<int:id>')
def view_ad(id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Incrementar visualizações
    if current_user.is_authenticated:
        # Não contar visualizações próprias do anúncio
        if anuncio.utilizador_id != current_user.id:
            anuncio.views += 1
            db.session.commit()
    else:
        # Contar visualizações de anonymous
        anuncio.views += 1
        db.session.commit()
    
    # Verificar se é favorito do utilizador atual
    favorito = False
    if current_user.is_authenticated:
        favorito = is_favorite(id)
    
    # Buscar anúncios relacionados na mesma categoria
    relacionados = Anuncio.query.filter(
        Anuncio.categoria_id == anuncio.categoria_id,
        Anuncio.id != id,
        Anuncio.status == 'ativo'
    ).limit(4).all()
    
    # Renderizar template do anúncio
    return render_template('ad.html',
                         anuncio=anuncio,
                         favorito=favorito,
                         relacionados=relacionados)

# Rota para visualizar anúncios de uma categoria
@app.route('/categoria/<slug>')
def view_category(slug):
    # Buscar categoria pelo slug ou retornar 404
    categoria = Categoria.query.filter_by(slug=slug, ativa=True).first_or_404()
    # Buscar anúncios ativos dessa categoria
    anuncios = Anuncio.query.filter_by(categoria_id=categoria.id, status='ativo').order_by(Anuncio.created_at.desc()).all()
    
    # Renderizar template da categoria
    return render_template('category.html',
                         categoria=categoria,
                         anuncios=anuncios)

# ==================== ROTAS DE AUTENTICAÇÃO ====================

# Rota de registo de novos utilizadores
@app.route('/registar', methods=['GET', 'POST'])
def register():
    # Se já estiver autenticado, redirecionar para home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Criar instância do formulário
    form = RegistrationForm()
    
    # Preencher choices de categorias para validação (não usado no register)
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Verificar se email já existe no sistema
        existing_user = Utilizador.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Este email já está registado.', 'error')
            return render_template('register.html', form=form)
        
        # Criar hash da password
        hashed_password = generate_password_hash(form.password.data)
        # Criar novo utilizador com dados do formulário
        utilizador = Utilizador(
            nome=form.nome.data,
            email=form.email.data,
            password=hashed_password,
            telefone=form.telefone.data,
            tipo='user'
        )
        
        # Salvar utilizador no banco de dados
        db.session.add(utilizador)
        db.session.commit()
        
        # Gerar token de recuperação para o utilizador
        token = bcrypt.hashpw(datetime.now().strftime('%Y%m%d%H%M%S').encode(), bcrypt.gensalt()).decode()
        utilizador.token_recuperacao = token
        # Token expira em 24 horas (ou nunca se não for usado)
        utilizador.token_expiracao = datetime.now() + timedelta(hours=24)
        db.session.commit()
        
        # Enviar email com token de recuperação
        send_account_confirmation_with_token(utilizador, token)
        
        # Exibir mensagem de sucesso e redirecionar para login
        flash('Conta criada com sucesso! Foi enviado um email com o seu token de recuperação.', 'success')
        return redirect(url_for('login'))
    
    # Renderizar template de registo
    return render_template('register.html', form=form)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver autenticado, redirecionar para home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Criar instância do formulário
    form = LoginForm()
    
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Buscar utilizador pelo email
        utilizador = Utilizador.query.filter_by(email=form.email.data).first()
        
        # Verificar se utilizador existe e password está correta
        if utilizador and check_password_hash(utilizador.password, form.password.data):
            # Verificar se conta está ativa
            if not utilizador.ativo:
                flash('A sua conta foi desativada.', 'error')
                return render_template('login.html', form=form, page='login')
            
            # Fazer login do utilizador
            login_user(utilizador)
            flash('Login realizado com sucesso!', 'success')
            
            # Redirecionar para página seguinte ou home
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Email ou password incorretos.', 'error')
    
    # Renderizar template de login
    return render_template('login.html', form=form, page='login')

# Rota de logout
@app.route('/logout')
@login_required  # Requer autenticação
def logout():
    # Fazer logout do utilizador
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    # Redirecionar para home
    return redirect(url_for('home'))

# Rota de perfil do utilizador
@app.route('/perfil', methods=['GET', 'POST'])
@login_required  # Requer autenticação
def profile():
    # Criar instância do formulário
    form = ProfileForm()
    
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Atualizar dados do utilizador atual
        current_user.nome = form.nome.data
        current_user.telefone = form.telefone.data
        
        # Se nova foto de perfil foi enviada
        if form.foto_perfil.data:
            filename = save_image(form.foto_perfil.data)
            if filename:
                current_user.foto_perfil = filename
        
        # Salvar alterações
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile'))
    
    # Preencher formulário com dados atuais do utilizador
    form.nome.data = current_user.nome
    form.telefone.data = current_user.telefone
    
    # Buscar anúncios criados por este utilizador
    meus_anuncios = Anuncio.query.filter_by(utilizador_id=current_user.id).order_by(Anuncio.created_at.desc()).all()
    
    # Buscar favoritos do utilizador
    favoritos = Favorito.query.filter_by(utilizador_id=current_user.id).all()
    # Extrair anúncios dos favoritos
    anuncios_favoritos = [f.anuncio for f in favoritos]
    
    # Renderizar template de perfil
    return render_template('profile.html',
                         form=form,
                         meus_anuncios=meus_anuncios,
                         favoritos=anuncios_favoritos)

# Rota de recuperação de password
@app.route('/recuperar-password', methods=['GET', 'POST'])
def forgot_password():
    # Criar instância do formulário
    form = ForgotPasswordForm()
    
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Buscar utilizador pelo email
        utilizador = Utilizador.query.filter_by(email=form.email.data).first()
        
        if utilizador:
            # Gerar token de recuperação
            token = bcrypt.hashpw(datetime.now().strftime('%Y%m%d%H%M%S').encode(), bcrypt.gensalt()).decode()
            utilizador.token_recuperacao = token
            # Token expira em 24 horas
            utilizador.token_expiracao = datetime.now() + timedelta(hours=24)
            db.session.commit()
            
            # Enviar email com link de recuperação
            send_password_reset_email(utilizador, token)
            
            flash('Link de recuperação enviado para o seu email.', 'success')
        else:
            flash('Email não encontrado.', 'error')
    
    # Renderizar template de recuperação
    return render_template('forgot-password.html', form=form)

# Rota para redefinir password com token
@app.route('/recuperar-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Buscar utilizador pelo token
    utilizador = Utilizador.query.filter_by(token_recuperacao=token).first()
    
    # Verificar se token é válido
    if not utilizador:
        flash('Token inválido.', 'error')
        return redirect(url_for('forgot_password'))
    
    # Verificar se token não expirou
    if utilizador.token_expiracao and utilizador.token_expiracao < datetime.now():
        flash('Token expirado. Peça um novo link de recuperação.', 'error')
        return redirect(url_for('forgot_password'))
    
    # Se formulário foi submetido
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validar passwords
        if password != confirm_password:
            flash('As passwords não coincidem.', 'error')
        elif len(password) < 6:
            flash('A password deve ter pelo menos 6 caracteres.', 'error')
        else:
            # Atualizar password
            utilizador.password = generate_password_hash(password)
            # Invalidar token após uso
            utilizador.token_recuperacao = None
            utilizador.token_expiracao = None
            db.session.commit()
            
            flash('Password alterada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    
    # Renderizar template com token
    return render_template('reset-password.html', token=token)

# ==================== ROTAS DE ANÚNCIOS ====================

# Rota para criar novo anúncio
@app.route('/anunciar', methods=['GET', 'POST'])
@login_required  # Requer autenticação
def create_ad():
    # Criar instância do formulário
    form = AdForm()
    # Preencher opções de categorias
    form.categoria_id.choices = [(c.id, c.nome) for c in get_categories()]
    
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Criar novo anúncio com dados do formulário
        anuncio = Anuncio(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            tipo=form.tipo.data,
            estado=form.estado.data,
            categoria_id=form.categoria_id.data,
            utilizador_id=current_user.id,
            localizacao=form.localizacao.data,
            status='ativo'  # Auto-aprovado para utilizadores normais
        )
        
        # Salvar anúncio no banco de dados
        db.session.add(anuncio)
        db.session.commit()
        
        # Processar imagens enviadas
        imagens = request.files.getlist('imagens')
        for i, img in enumerate(imagens):
            if img.filename:
                filename = save_image(img)
                if filename:
                    # Criar registro de imagem
                    imagem = ImagemAnuncio(
                        arquivo=filename,
                        anuncio_id=anuncio.id,
                        principal=(i == 0),  # Primeira imagem é principal
                        ordem=i
                    )
                    db.session.add(imagem)
        
        db.session.commit()
        flash('Anúncio criado com sucesso!', 'success')
        # Redirecionar para visualização do anúncio
        return redirect(url_for('view_ad', id=anuncio.id))
    
    # Renderizar template de criação de anúncio
    return render_template('create-ad.html', form=form)

# Rota para editar anúncio existente
@app.route('/anuncio/<int:id>/editar', methods=['GET', 'POST'])
@login_required  # Requer autenticação
def edit_ad(id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Verificar se utilizador é o dono ou admin
    if anuncio.utilizador_id != current_user.id and not current_user.is_admin():
        abort(403)  # Acesso negado
    
    # Criar instância do formulário
    form = AdForm()
    # Preencher opções de categorias
    form.categoria_id.choices = [(c.id, c.nome) for c in get_categories()]
    
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Atualizar dados do anúncio
        anuncio.titulo = form.titulo.data
        anuncio.descricao = form.descricao.data
        anuncio.preco = form.preco.data
        anuncio.tipo = form.tipo.data
        anuncio.estado = form.estado.data
        anuncio.categoria_id = form.categoria_id.data
        anuncio.localizacao = form.localizacao.data
        
        # Processar novas imagens enviadas
        imagens = request.files.getlist('imagens')
        for i, img in enumerate(imagens):
            if img.filename:
                filename = save_image(img)
                if filename:
                    # Se não há imagens principais, definir como principal
                    principal = False
                    if not ImagemAnuncio.query.filter_by(anuncio_id=anuncio.id).first():
                        principal = True
                    
                    # Criar novo registro de imagem
                    imagem = ImagemAnuncio(
                        arquivo=filename,
                        anuncio_id=anuncio.id,
                        principal=principal,
                        ordem=ImagemAnuncio.query.filter_by(anuncio_id=anuncio.id).count() + i
                    )
                    db.session.add(imagem)
        
        db.session.commit()
        flash('Anúncio atualizado com sucesso!', 'success')
        return redirect(url_for('view_ad', id=anuncio.id))
    
    # Preencher formulário com dados atuais do anúncio
    form.titulo.data = anuncio.titulo
    form.descricao.data = anuncio.descricao
    form.preco.data = float(anuncio.preco)
    form.tipo.data = anuncio.tipo
    form.estado.data = anuncio.estado
    form.categoria_id.data = anuncio.categoria_id
    form.localizacao.data = anuncio.localizacao
    
    # Buscar imagens existentes do anúncio
    imagens = ImagemAnuncio.query.filter_by(anuncio_id=anuncio.id).order_by(ImagemAnuncio.ordem).all()
    
    # Renderizar template de edição
    return render_template('edit-ad.html', form=form, anuncio=anuncio, imagens=imagens)

# Rota para excluir anúncio
@app.route('/anuncio/<int:id>/apagar', methods=['POST'])
@login_required  # Requer autenticação
def delete_ad(id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Verificar propriedade ou se é admin
    if anuncio.utilizador_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    # Apagar imagens do disco rígido
    for img in anuncio.imagens:
        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], img.arquivo)
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
    
    # Excluir anúncio do banco de dados
    db.session.delete(anuncio)
    db.session.commit()
    
    flash('Anúncio apagado com sucesso!', 'success')
    return redirect(url_for('profile'))

# Rota para excluir uma imagem específica do anúncio
@app.route('/anuncio/<int:id>/imagem/<int:image_id>/apagar', methods=['POST'])
@login_required  # Requer autenticação
def delete_image(id, image_id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Verificar se é o dono do anúncio
    if anuncio.utilizador_id != current_user.id:
        abort(403)
    
    # Buscar imagem pelo ID ou retornar 404
    imagem = ImagemAnuncio.query.get_or_404(image_id)
    
    # Apagar arquivo do disco
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], imagem.arquivo)
        if os.path.exists(filepath):
            os.remove(filepath)
    except:
        pass
    
    # Se era a imagem principal, definir outra como principal
    if imagem.principal:
        outra = ImagemAnuncio.query.filter_by(anuncio_id=id).filter(ImagemAnuncio.id != image_id).first()
        if outra:
            outra.principal = True
    
    # Excluir imagem do banco de dados
    db.session.delete(imagem)
    db.session.commit()
    
    return redirect(url_for('edit_ad', id=id))

# Rota para adicionar/remover favorito
@app.route('/anuncio/<int:id>/favorito', methods=['POST'])
@login_required  # Requer autenticação
def toggle_favorite(id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Verificar se já é favorito
    favorito = Favorito.query.filter_by(utilizador_id=current_user.id, anuncio_id=id).first()
    
    # Se já for favorito, remover
    if favorito:
        db.session.delete(favorito)
        flash('Removido dos favoritos.', 'success')
    else:
        # Se não for favorito, adicionar
        novo_favorito = Favorito(utilizador_id=current_user.id, anuncio_id=id)
        db.session.add(novo_favorito)
        flash('Adicionado aos favoritos!', 'success')
    
    db.session.commit()
    return redirect(url_for('view_ad', id=id))

# Rota para denunciar um anúncio
@app.route('/anuncio/<int:id>/denunciar', methods=['POST'])
@login_required  # Requer autenticação
def report_ad(id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Obter motivo e descrição do formulário
    motivo = request.form.get('motivo')
    descricao = request.form.get('descricao')
    
    # Validar que motivo foi selecionado
    if not motivo:
        flash('Por favor, selecione um motivo.', 'error')
        return redirect(url_for('view_ad', id=id))
    
    # Não permitir denúncia do próprio anúncio
    if anuncio.utilizador_id == current_user.id:
        flash('Não pode denunciar os seus próprios anúncios.', 'error')
        return redirect(url_for('view_ad', id=id))
    
    # Criar nova denúncia
    denuncia = Denuncia(
        anuncio_id=id,
        utilizador_id=current_user.id,
        motivo=motivo,
        descricao=descricao
    )
    
    db.session.add(denuncia)
    db.session.commit()
    
    flash('Denúncia enviada. Obrigado pela colaboração!', 'success')
    return redirect(url_for('view_ad', id=id))

# ==================== ROTAS DE MENSAGENS ====================

# Rota para listar conversas
@app.route('/mensagens')
@login_required  # Requer autenticação
def messages():
    # Buscar todas as mensagens do utilizador (enviadas ou recebidas)
    mensagens = Mensagem.query.filter(
        db.or_(
            Mensagem.utilizador_de == current_user.id,
            Mensagem.utilizador_para == current_user.id
        )
    ).order_by(Mensagem.created_at.desc()).all()
    
    # Agrupar mensagens por interlocutor
    conversas = {}
    for msg in mensagens:
        # Determinar ID do outro utilizador na conversa
        outro_id = msg.utilizador_de if msg.utilizador_de != current_user.id else msg.utilizador_para
        
        # Se ainda não criou entrada para este interlocutor
        if outro_id not in conversas:
            utilizador = Utilizador.query.get(outro_id)
            ultimo_anuncio = Anuncio.query.get(msg.anuncio_id)
            
            conversas[outro_id] = {
                'utilizador': utilizador,
                'anuncio': ultimo_anuncio,
                'mensagem': msg,
                'nao_lidas': 0
            }
        
        # Contar mensagens não lidas
        if msg.utilizador_para == current_user.id and not msg.lida:
            conversas[outro_id]['nao_lidas'] += 1
    
    return render_template('messages.html', conversas=conversas)

# Rota para ver conversa específica
@app.route('/mensagens/<int:contact_id>')
@login_required  # Requer autenticação
def conversation(contact_id):
    # Buscar mensagens entre os dois utilizadores
    mensagens = Mensagem.query.filter(
        db.or_(
            db.and_(Mensagem.utilizador_de == current_user.id, Mensagem.utilizador_para == contact_id),
            db.and_(Mensagem.utilizador_de == contact_id, Mensagem.utilizador_para == current_user.id)
        )
    ).order_by(Mensagem.created_at.asc()).all()
    
    # Marcar mensagens como lidas
    for msg in mensagens:
        if msg.utilizador_para == current_user.id and not msg.lida:
            msg.lida = True
    
    db.session.commit()
    
    # Buscar dados do contacto
    contacto = Utilizador.query.get_or_404(contact_id)
    
    return render_template('conversation.html', mensagens=mensagens, contacto=contacto)

# Rota para enviar mensagem
@app.route('/mensagens/enviar', methods=['POST'])
@login_required  # Requer autenticação
def send_message():
    # Criar instância do formulário
    form = MessageForm()
    
    # Se formulário foi submetido e é válido
    if form.validate_on_submit():
        # Obter ID do anúncio e do destinatário
        anuncio_id = request.form.get('anuncio_id', type=int)
        utilizador_para = request.form.get('utilizador_para', type=int)
        
        # Criar nova mensagem
        mensagem = Mensagem(
            anuncio_id=anuncio_id,
            utilizador_de=current_user.id,
            utilizador_para=utilizador_para,
            mensagem=form.mensagem.data
        )
        
        db.session.add(mensagem)
        db.session.commit()
        
        flash('Mensagem enviada!', 'success')
    
    # Redirecionar para a conversa
    return redirect(url_for('conversation', contact_id=utilizador_para))

# Rota para iniciar conversa a partir de um anúncio
@app.route('/anuncio/<int:id>/mensagem', methods=['POST'])
@login_required  # Requer autenticação
def start_conversation(id):
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    # Obter texto da mensagem
    mensagem_texto = request.form.get('mensagem')
    
    # Validar que há mensagem
    if not mensagem_texto:
        flash('Por favor, escreva uma mensagem.', 'error')
        return redirect(url_for('view_ad', id=id))
    
    # Não permitir enviar mensagem para si mesmo
    if anuncio.utilizador_id == current_user.id:
        flash('Não pode enviar mensagens para os seus próprios anúncios.', 'error')
        return redirect(url_for('view_ad', id=id))
    
    # Criar nova mensagem
    mensagem = Mensagem(
        anuncio_id=id,
        utilizador_de=current_user.id,
        utilizador_para=anuncio.utilizador_id,
        mensagem=mensagem_texto
    )
    
    db.session.add(mensagem)
    db.session.commit()
    
    flash('Mensagem enviada ao anunciante!', 'success')
    return redirect(url_for('view_ad', id=id))

# ==================== ROTAS DE ADMIN ====================

# Rota do painel de administração
@app.route('/admin')
@login_required  # Requer autenticação
def admin_dashboard():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Estatísticas do sistema
    total_utilizadores = Utilizador.query.count()
    total_anuncios = Anuncio.query.count()
    anuncios_pendentes = Anuncio.query.filter_by(status='pendente').count()
    anuncios_ativos = Anuncio.query.filter_by(status='ativo').count()
    denuncias_pendentes = Denuncia.query.filter_by(status='pendente').count()
    
    # Anúncios recentes
    recentes = Anuncio.query.order_by(Anuncio.created_at.desc()).limit(5).all()
    
    # Renderizar template do dashboard
    return render_template('admin/dashboard.html',
                         total_utilizadores=total_utilizadores,
                         total_anuncios=total_anuncios,
                         anuncios_pendentes=anuncios_pendentes,
                         anuncios_ativos=anuncios_ativos,
                         denuncias_pendentes=denuncias_pendentes,
                         recentes=recentes)

# Rota para listar utilizadores (admin)
@app.route('/admin/utilizadores')
@login_required  # Requer autenticação
def admin_users():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Buscar todos os utilizadores
    utilizadores = Utilizador.query.order_by(Utilizador.created_at.desc()).all()
    return render_template('admin/users.html', utilizadores=utilizadores)

# Rota para editar utilizador (admin)
@app.route('/admin/utilizadores/<int:id>/editar', methods=['GET', 'POST'])
@login_required  # Requer autenticação
def admin_edit_user(id):
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Buscar utilizador pelo ID ou retornar 404
    utilizador = Utilizador.query.get_or_404(id)
    
    # Se foi submetido formulário de edição
    if request.method == 'POST':
        # Atualizar dados do utilizador
        utilizador.nome = request.form.get('nome')
        utilizador.telefone = request.form.get('telefone')
        utilizador.tipo = request.form.get('tipo')
        utilizador.ativo = 'ativo' in request.form
        
        # Se nova password foi fornecida, atualizar
        nova_password = request.form.get('password')
        if nova_password:
            utilizador.password = generate_password_hash(nova_password)
        
        db.session.commit()
        # Registrar ação no log
        log_admin_action('editar_utilizador', 'utilizadores', id, f'Editar utilizador: {utilizador.email}')
        
        flash('Utilizador atualizado!', 'success')
        return redirect(url_for('admin_users'))
    
    # Renderizar template de edição
    return render_template('admin/edit-user.html', utilizador=utilizador)

# Rota para eliminar utilizador (admin)
@app.route('/admin/utilizadores/<int:id>/apagar', methods=['POST'])
@login_required  # Requer autenticação
def admin_delete_user(id):
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Buscar utilizador pelo ID ou retornar 404
    utilizador = Utilizador.query.get_or_404(id)
    
    # Não permitir eliminar a si mesmo
    if utilizador.id == current_user.id:
        flash('Não pode apagar a sua própria conta.', 'error')
        return redirect(url_for('admin_users'))
    
    # Registrar ação no log antes de excluir
    log_admin_action('apagar_utilizador', 'utilizadores', id, f'Apagar utilizador: {utilizador.email}')
    
    # Excluir utilizador
    db.session.delete(utilizador)
    db.session.commit()
    
    flash('Utilizador apagado!', 'success')
    return redirect(url_for('admin_users'))

# Rota para listar anúncios (admin)
@app.route('/admin/anuncios')
@login_required  # Requer autenticação
def admin_ads():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Obter filtro de status
    status = request.args.get('status', 'todos')
    
    # Buscar anúncios conforme filtro
    if status == 'todos':
        anuncios = Anuncio.query.order_by(Anuncio.created_at.desc()).all()
    else:
        anuncios = Anuncio.query.filter_by(status=status).order_by(Anuncio.created_at.desc()).all()
    
    return render_template('admin/ads.html', anuncios=anuncios, status=status)

# Rota para moderar anúncio (aprovar/rejeitar)
@app.route('/admin/anuncios/<int:id>/moderar', methods=['POST'])
@login_required  # Requer autenticação
def admin_moderate_ad(id):
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Obter ação e motivo do formulário
    acao = request.form.get('acao')
    motivo = request.form.get('motivo')
    
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Executar ação de moderação
    if acao == 'aprovar':
        anuncio.status = 'ativo'
        flash('Anúncio aprovado!', 'success')
    elif acao == 'rejeitar':
        anuncio.status = 'rejeitado'
        anuncio.motivo_rejeicao = motivo
        flash('Anúncio rejeitado.', 'success')
    
    # Registrar no log
    log_admin_action('moderar_anuncio', 'anuncios', id, f'{acao}: {anuncio.titulo}')
    
    db.session.commit()
    return redirect(url_for('admin_ads'))

# Rota para excluir anúncio (admin)
@app.route('/admin/anuncios/<int:id>/apagar', methods=['POST'])
@login_required  # Requer autenticação
def admin_delete_ad(id):
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Buscar anúncio pelo ID ou retornar 404
    anuncio = Anuncio.query.get_or_404(id)
    
    # Apagar imagens do disco
    for img in anuncio.imagens:
        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], img.arquivo)
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
    
    # Registrar no log antes de excluir
    log_admin_action('apagar_anuncio', 'anuncios', id, f'Anúncio apagado: {anuncio.titulo}')
    
    # Excluir anúncio
    db.session.delete(anuncio)
    db.session.commit()
    
    flash('Anúncio apagado!', 'success')
    return redirect(url_for('admin_ads'))

# Rota para gerir categorias (admin)
@app.route('/admin/categorias', methods=['GET', 'POST'])
@login_required  # Requer autenticação
def admin_categories():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Se foi submetido formulário de criação
    if request.method == 'POST':
        # Obter dados do formulário
        nome = request.form.get('nome')
        slug = request.form.get('slug')
        descricao = request.form.get('descricao')
        icone = request.form.get('icone')
        
        # Criar nova categoria
        categoria = Categoria(
            nome=nome,
            slug=slug,
            descricao=descricao,
            icone=icone
        )
        
        db.session.add(categoria)
        db.session.commit()
        
        # Registrar no log
        log_admin_action('criar_categoria', 'categorias', categoria.id, f'Categoria: {nome}')
        
        flash('Categoria criada!', 'success')
        return redirect(url_for('admin_categories'))
    
    # Buscar todas as categorias
    categorias = Categoria.query.order_by(Categoria.ordem).all()
    return render_template('admin/categories.html', categorias=categorias)

# Rota para listar denúncias (admin)
@app.route('/admin/denuncias')
@login_required  # Requer autenticação
def admin_reports():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Buscar todas as denúncias
    denuncias = Denuncia.query.order_by(Denuncia.created_at.desc()).all()
    return render_template('admin/reports.html', denuncias=denuncias)

# Rota para listar logs de admin (admin)
@app.route('/admin/logs')
@login_required  # Requer autenticação
def admin_logs():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Buscar últimos 100 logs
    logs = LogAdmin.query.order_by(LogAdmin.created_at.desc()).limit(100).all()
    return render_template('admin/logs.html', logs=logs)

# API para obter estatísticas em JSON
@app.route('/api/admin/stats')
@login_required  # Requer autenticação
def api_admin_stats():
    # Verificar se é admin
    if not current_user.is_admin():
        abort(403)
    
    # Retornar estatísticas em JSON
    return jsonify({
        'total_utilizadores': Utilizador.query.count(),
        'total_anuncios': Anuncio.query.count(),
        'anuncios_pendentes': Anuncio.query.filter_by(status='pendente').count(),
        'anuncios_ativos': Anuncio.query.filter_by(status='ativo').count(),
        'denuncias_pendentes': Denuncia.query.filter_by(status='pendente').count()
    })

# ==================== ERROR HANDLERS ====================

# Tratamento de erro 404 - Página não encontrada
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error='Página não encontrada'), 404

# Tratamento de erro 403 - Acesso negado
@app.errorhandler(403)
def error_403(e):
    return render_template('error.html', error='Acesso negado'), 403

# Tratamento de erro 500 - Erro interno do servidor
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error='Erro interno do servidor'), 500

# ==================== MAIN ====================

# Ponto de entrada da aplicação
if __name__ == '__main__':
    # Criar pastas necessárias para uploads
    upload_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)
    
    # Obter porta do ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    # Iniciar servidor Flask (debug=False para producao)
    debug = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=debug)
