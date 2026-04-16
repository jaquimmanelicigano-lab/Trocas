# 🏠 Trocas - Classificados Online

Plataforma de classificados online estilo OLX, desenvolvida com Flask (Python) e SQLite.

## 🚀 Funcionalidades

### Utilizador
- ✅ Registo e login de utilizadores
- ✅ Perfil de utilizador com informações de contacto
- ✅ Criar, editar e apagar anúncios
- ✅ Upload de múltiplas imagens por anúncio
- ✅ Sistema de pesquisa com filtros (categoria, preço, localização, tipo)
- ✅ Sistema de mensagens entre utilizadores
- ✅ Lista de favoritos
- ✅ Histórico de anúncios

### Administrador
- ✅ Painel administrativo separado
- ✅ Gestão de utilizadores (editar, ativar/desativar, eliminar)
- ✅ Gestão de anúncios (aprovar, rejeitar, eliminar)
- ✅ Gestão de categorias
- ✅ Ver denúncias de anúncios
- ✅ Logs de administração
- ✅ Dashboard com estatísticas

## 🛠️ Tecnologias

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Base de Dados:** SQLite
- **Autenticação:** Flask-Login
- **Upload:** Flask-WTF

## 📋 Pré-requisitos

- Python 3.8+

## 🔧 Instalação

1. **Clonar o repositório**
```bash
cd trocas
```

2. **Instalar dependências**
```bash
pip install -r requirements.txt
```

3. **Configurar base de dados**
A base de dados SQLite será criada automaticamente em `instance/trocas.db`.

4. **Iniciar o servidor**
```bash
python app.py
```

5. **Aceder ao site**
```
http://localhost:3000
```

## 👤 Credenciais de Teste

Crie uma conta através da página de registo.

## 📁 Estrutura do Projeto

```
trocas/
├── app.py                # Servidor principal
├── models.py             # Modelos do SQLAlchemy
├── config.py             # Configurações
├── requirements.txt      # Dependências
├── instance/             # Base de dados SQLite
└── src/
    ├── public/           # Ficheiros estáticos
    └── views/            # Templates HTML
```

## 🔐 Segurança

- Passwords hasheadas com bcrypt
- Proteção CSRF com Flask-WTF
- Validação de formulários

## 🎨 Design

O design é moderno e responsivo, funcionando em dispositivos móveis e desktop.

## 📝 Licença

MIT
