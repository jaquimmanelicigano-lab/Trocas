"""
Script para recriar o banco de dados com o novo schema.
Isso apagará TODOS os dados existentes.
"""
import os
from app import app, db
from models import Utilizador, Categoria, Anuncio, ImagemAnuncio, Favorito, Mensagem, Denuncia, LogAdmin
from werkzeug.security import generate_password_hash

with app.app_context():
    print("=== RECRIANDO BANCO DE DADOS ===\n")
    
    # Remover todas as tabelas e recriar
    print("Removendo todas as tabelas...")
    db.drop_all()
    print("[OK] Todas as tabelas removidas.")
    
    # Criar todas as tabelas com o novo schema
    db.create_all()
    print("[OK] Tabelas criadas com novo schema.\n")
    
    # Inserir categorias padrão
    categorias_padrao = [
        {'nome': 'Eletrónicos', 'slug': 'eletronicos', 'icone': 'fa-laptop', 'ordem': 1},
        {'nome': 'Vestuário e Acessórios', 'slug': 'roupas-acessorios', 'icone': 'fa-tshirt', 'ordem': 2},
        {'nome': 'Mobiliário e Decoração', 'slug': 'moveis-decoracao', 'icone': 'fa-couch', 'ordem': 3},
        {'nome': 'Veículos', 'slug': 'veiculos', 'icone': 'fa-car', 'ordem': 4},
        {'nome': 'Livros e Revistas', 'slug': 'livros-revistas', 'icone': 'fa-book', 'ordem': 5},
        {'nome': 'Desporto e Lazer', 'slug': 'esportes-lazer', 'icone': 'fa-futbol', 'ordem': 6},
        {'nome': 'Bebés e Crianças', 'slug': 'bebes-criancas', 'icone': 'fa-child', 'ordem': 7},
        {'nome': 'Música e Instrumentos', 'slug': 'musica-instrumentos', 'icone': 'fa-music', 'ordem': 8},
        {'nome': 'Ferramentas', 'slug': 'ferramentas', 'icone': 'fa-wrench', 'ordem': 9},
        {'nome': 'Outros', 'slug': 'outros', 'icone': 'fa-ellipsis-h', 'ordem': 10}
    ]
    
    for cat_data in categorias_padrao:
        categoria = Categoria(
            nome=cat_data['nome'],
            slug=cat_data['slug'],
            icone=cat_data['icone'],
            ordem=cat_data['ordem'],
            ativa=True
        )
        db.session.add(categoria)
    
    # Criar utilizador administrador padrão
    admin_password = generate_password_hash('admin123')
    admin_user = Utilizador(
        nome='Administrador',
        email='admin@trocas.pt',
        password=admin_password,
        telefone='000000000',
        tipo='admin',
        ativo=True
    )
    db.session.add(admin_user)
    
    db.session.commit()
    print("[OK] Categorias padrão inseridas.")
    print("[OK] Utilizador administrador criado:")
    print("     Email: admin@trocas.pt")
    print("     Password: admin123")
    print("     !! ALTERAR A PASSWORD APÓS O PRIMEIRO ACESSO !!\n")
    
    # Verificar colunas da tabela anuncios
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    cols = inspector.get_columns('anuncios')
    print(f"Colunas de 'anuncios' ({len(cols)}):")
    for col in cols:
        print(f"  - {col['name']:25s} {col['type']}")
    
    print("\n[SUCCESS] Database recreated successfully!")
    print("\nPróximo passo: reiniciar a aplicação.")
