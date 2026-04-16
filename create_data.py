import os
os.environ['FLASK_ENV'] = 'default'

from app import app, db
from models import Categoria, Utilizador
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    categorias = [
        Categoria(nome='Electrónica', slug='eletronica', descricao='Telemóveis, computadores, Tablets, Acessórios', icone='fa-laptop', ordem=1, ativa=True),
        Categoria(nome='Veículos', slug='veiculos', descricao='Carros, Motos, Bicicletas, Peças', icone='fa-car', ordem=2, ativa=True),
        Categoria(nome='Imóveis', slug='imoveis', descricao='Casas, Apartamentos, Terrenos, Escritórios', icone='fa-home', ordem=3, ativa=True),
        Categoria(nome='Móveis', slug='moveis', descricao='Sofás, Camas, Mesas, Cadeiras', icone='fa-couch', ordem=4, ativa=True),
        Categoria(nome='Moda', slug='moda', descricao='Roupa, Calçado, Acessórios, Relógios', icone='fa-tshirt', ordem=5, ativa=True),
        Categoria(nome='Desporto', slug='desporto', descricao='Fitness, Futebol, Ciclismo, Artigos desportivos', icone='fa-running', ordem=6, ativa=True),
        Categoria(nome='Lazer', slug='lazer', descricao='Jogos, Brinquedos, Música, Livros', icone='fa-gamepad', ordem=7, ativa=True),
        Categoria(nome='Electrodomésticos', slug='electrodomesticos', descricao='Frigoríficos, Máquinas, Fornos, Aspiradores', icone='fa-blender', ordem=8, ativa=True),
        Categoria(nome='Serviços', slug='servicos', descricao='Transportes, Limpeza, Reparações, Aulas', icone='fa-tools', ordem=9, ativa=True),
        Categoria(nome='Outros', slug='outros', descricao='Outros artigos diversos', icone='fa-box', ordem=10, ativa=True),
    ]
    
    for cat in categorias:
        existing = Categoria.query.filter_by(slug=cat.slug).first()
        if not existing:
            db.session.add(cat)
    
    admin = Utilizador.query.filter_by(email='admin@trocas.pt').first()
    if not admin:
        admin = Utilizador(
            nome='Administrador',
            email='admin@trocas.pt',
            password=generate_password_hash('admin123'),
            telefone='910000000',
            tipo='admin'
        )
        db.session.add(admin)
    
    db.session.commit()
    print(f'Categorias criadas: {Categoria.query.count()}')
    print('Admin criado: admin@trocas.pt / admin123')