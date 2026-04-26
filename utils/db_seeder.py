from models import db, Categoria, Utilizador
from werkzeug.security import generate_password_hash

def seed_db():
    """Insere dados padrão se as tabelas estiverem vazias."""
    
    # 1. Inserir Categorias se não existirem
    if Categoria.query.count() == 0:
        print("Semeando categorias...")
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
        db.session.commit()
        print("[OK] Categorias inseridas.")

    # 2. Inserir Admin se não existir
    if Utilizador.query.filter_by(tipo='admin').count() == 0:
        print("Semeando utilizador administrador...")
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
        print("[OK] Administrador criado (admin@trocas.pt / admin123).")
