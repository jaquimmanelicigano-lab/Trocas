# 🏠 Trocas - Classificados Online

Plataforma de classificados online estilo OLX, desenvolvida com Node.js, Express, MySQL e EJS.

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

- **Backend:** Node.js + Express
- **Frontend:** HTML5, CSS3, JavaScript (EJS)
- **Base de Dados:** MySQL
- **Autenticação:** bcryptjs + express-session
- **Upload:** Multer

## 📋 Pré-requisitos

- Node.js 14+
- MySQL 5.7+

## 🔧 Instalação

1. **Clonar o repositório**
```bash
cd trocas
```

2. **Instalar dependências**
```bash
npm install
```

3. **Configurar base de dados**

Edite o ficheiro `.env` com as suas credenciais:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_password
DB_NAME=trocas
PORT=3000
```

4. **Inicializar a base de dados**
```bash
npm run db:init
```

5. **(Opcional) Criar dados de exemplo**
```bash
node database/seeds.js
```

6. **Iniciar o servidor**
```bash
npm start
```

7. **Aceder ao site**
```
http://localhost:3000
```

## 👤 Credenciais

### Administrador
- **Email:** admin@trocas.pt
- **Password:** admin123

### Utilizadores de teste (após executar seeds)
- **Email:** joao@exemplo.pt
- **Password:** password123

## 📁 Estrura do Projeto

```
trocas/
├── database/
│   ├── init.js        # Script de inicialização da BD
│   └── seeds.js       # Dados de exemplo
├── src/
│   ├── config/
│   │   ├── database.js
│   │   └── db.js
│   ├── controllers/
│   │   ├── adminController.js
│   │   ├── adController.js
│   │   ├── authController.js
│   │   ├── mainController.js
│   │   └── messageController.js
│   ├── middleware/
│   │   ├── auth.js
│   │   └── upload.js
│   ├── public/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   │       └── uploads/
│   ├── routes/
│   │   └── index.js
│   ├── views/
│   │   ├── admin/
│   │   ├── partials/
│   │   ├── index.ejs
│   │   └── ...
│   └── server.js
├── .env
├── package.json
└── README.md
```

## 🔐 Segurança

- Passwords hasheadas com bcrypt
- Sessões seguras com httpOnly cookies
- Proteção contra SQL Injection (prepared statements)
- Validação de formulários
- Controlo de acessos (user vs admin)

## 🎨 Design

O design é moderno e responsivo, funcionando em dispositivos móveis e desktop. Utiliza:
- Cores primárias: Indigo (#4F46E5)
- Sistema de grid flexível
- Tipografia limpa (system fonts)
- Ícones Font Awesome

## 📝 Licença

MIT

---

Desenvolvido como projeto de aprendizagem.
