# 📚 Documentação Completa do Projeto TROCAS

## Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Projeto](#arquitetura-do-projeto)
3. [Estrutura de Ficheiros](#estrutura-de-ficheiros)
4. [Tecnologias Utilizadas](#tecnologias-utilizadas)
5. [Modelo de Dados](#modelo-de-dados)
6. [Funcionalidades](#funcionalidades)
7. [Configuração e Instalação](#configuração-e-instalação)
8. [Descrição dos Ficheiros](#descrição-dos-ficheiros)
9. [Rotas da Aplicação](#rotas-da-aplicação)
10. [Variáveis de Ambiente](#variáveis-de-ambiente)
11. [Credenciais de Teste](#credenciais-de-teste)
12. [Chat de Suporte](#chat-de-suporte)
13. [Histórico de Atualizações](#histórico-de-atualizações)

---

## Visão Geral

**TROCAS** é uma plataforma de classificados online portuguesa, desenvolvida em **Python/Flask**, que permite aos utilizadores comprar, vender e trocar artigos de forma simples e segura. O sistema inclui funcionalidades completas de autenticação, gestão de anúncios, mensagens entre utilizadores e um painel administrativo.

A plataforma foi desenvolvida pela **Alegria Web Studio** e está registada com todos os direitos reservados para 2026.

**Website:** http://localhost:3000

### Paleta de Cores

A paleta de cores original foi alterada durante o redesign:

**Cores Originais (Branco e Laranja):**
- Primary: #f97316 (Laranja)
- Background: #ffffff (Branco)
- Secondary: #ea580c (Laranja escuro)

**Cores Atuais (Azul Moderno):**
- Primary: #3b82f6 (Azul)
- Primary Dark: #2563eb (Azul escuro)
- Primary Light: #60a5fa (Azul claro)
- Background: #f8fafc (Cinza muito claro)
- Surface: #ffffff (Branco)
- Text Main: #1e293b (Cinza escuro)
- Text Secondary: #64748b (Cinza médio)
- Success: #22c55e (Verde)
- Error: #ef4444 (Vermelho)
- Border: #e2e8f0 (Cinza claro)

*Nota: O botão flutuante de chat utiliza um gradiente roxo (#6366f1 → #8b5cf6) para se destacar.*

---

## Arquitetura do Projeto

O projeto utiliza uma arquitetura **MVC (Model-View-Controller)** com as seguintes camadas:

- **Model (Modelos):** Define a estrutura dos dados e interage com a base de dados MySQL
- **View (Views):** Templates HTML com sintaxe Jinja2 para renderização
- **Controller (Routes/Funções):** Lógica de negócio implementada no ficheiro app.py

A aplicação executa no **porto 3000** (configurável através da variável de ambiente PORT).

---

## Estrutura de Ficheiros

```
trocas/
├── app.py                        # Ficheiro principal - aplicação Flask
├── config.py                     # Configurações da aplicação
├── models.py                     # Modelos da base de dados (SQLAlchemy)
├── create_data.py                # Script para criar dados iniciais
├── requirements.txt              # Dependências Python
├── .env                         # Variáveis de ambiente (não commitado)
├── DOCUMENTACAO.md              # Esta documentação
├── README.md                    # Ficheiro README
├── utils/                       # Utilitários
│   └── email_utils.py            # Funções de envio de emails
└── src/                        # Ficheiros públicos e templates
    ├── views/                  # Templates HTML (Jinja2)
    │   ├── index.html          # Página inicial
    │   ├── login.html         # Página de login
    │   ├── register.html     # Página de registo
    │   ├── perfil.html      # Perfil do utilizador
    │   ├── support.html    # Centro de ajuda
    │   ├── create-ad.html   # Criar anúncio
    │   ├── edit-ad.html    # Editar anúncio
    │   ├── search.html     # Pesquisa de anúncios
    │   ├── messages.html # Lista de mensagens
    │   ├── ad.html       # Visualizar anúncio
    │   ├── category.html # Página de categoria
    │   ├── error.html   # Página de erro
    │   ├── forgot-password.html  # Recuperar password
    │   ├── reset-password.html  # Definir nova password
    │   └── admin/           # Painel administrativo
    │       ├── layout.html    # Layout do admin
    │       ├── dashboard.html # Dashboard admin
    │       ├── users.html    # Gestão de utilizadores
    │       ├── ads.html     # Gestão de anúncios
    │       ├── categories.html # Gestão de categorias
    │       ├── reports.html   # Denúncias
    │       ├── logs.html    # Logs administrativos
    │       └── edit-user.html # Editar utilizador
    ├── public/              # Ficheiros estáticos
    │   ├── css/
    │   │   └── style.css  # Folha de estilos principal
    │   ├── js/             # JavaScript (não utilizado)
    │   └── images/
    │       └── uploads/    # Imagens dos anúncios
    └── views/
        └── partials/       # Partes reutilizáveis
            ├── header.html # Cabeçalho (menu, nav, flash messages)
            └── footer.html # Rodapé (links, copyright, JavaScript)
```

---

## Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem de programação
- **Flask** - Framework web ligero
- **SQLAlchemy** - ORM para interação com base de dados
- **Flask-Login** - Gestão de autenticação
- **Flask-WTF** - Formulários com validação e proteção CSRF
- **bcrypt** - Geração de hashes para passwords e tokens

### Base de Dados
- **MySQL** - Sistema de gestão de base de dados relacional
- Porto padrão: 3306
- Base de dados: trocas_db

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilos modernos com variáveis CSS
- **JavaScript** - Interatividade do lado do cliente
- **Font Awesome 6.4** - Ícones

### Servidor de Email
- **Gmail SMTP** - Envio de emails através de Gmail com App Password

---

## Modelo de Dados

A base de dados MySQL contém as seguintes tabelas:

### 1. utilizadores
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| nome | String(100) | Nome do utilizador |
| email | String(120) | Email único |
| password | String(255) | Hash da password |
| telefone | String(20) | Contacto telefónico |
| foto_perfil | String(255) | Foto de perfil |
| tipo | Enum('user','admin') | Tipo de conta |
| ativo | Boolean | Estado da conta |
| token_recuperacao | String(255) | Token para recuperação |
| token_expiracao | DateTime | Validade do token |
| created_at | DateTime | Data de criação |

### 2. categorias
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| nome | String(100) | Nome da categoria |
| slug | String(100) | URL amigável |
| descricao | Text | Descrição |
| icone | String(50) | Ícone Font Awesome |
| ordem | Integer | Ordem de apresentação |
| ativa | Boolean | Estado |

### 3. anuncios
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| titulo | String(200) | Título do anúncio |
| descricao | Text | Descrição completa |
| preco | Decimal(10,2) | Preço em euros |
| tipo | Enum('venda','troca') | Tipo de operação |
| estado | Enum('novo','usado_bueno','usado_regular') | Estado do artigo |
| localizacao | String(150) | Localização |
| status | Enum('ativo','pendente','rejeitado') | Estado do anúncio |
| views | Integer | Número de visualizações |
| categoria_id | Integer | FK para categorias |
| utilizador_id | Integer | FK para utilizadores |
| motivo_rejeicao | Text | Motivo de rejeição |
| created_at | DateTime | Data de criação |

### 4. imagens_anuncio
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| arquivo | String(255) | Nome do ficheiro |
| booleanprincipal | Boolean | Imagem principal |
| ordem | Integer | Ordem das imagens |
| anuncio_id | Integer | FK para anuncios |

### 5. favoritos
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| utilizador_id | Integer | FK para utilizadores |
| anuncio_id | Integer | FK para anuncios |
| created_at | DateTime | Data de criação |

### 6. mensagens
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| mensagem | Text | Texto da mensagem |
| booleanlida | Boolean | Mensagem lida |
| utilizador_de | Integer | Remetente |
| utilizador_para | Integer | Destinatário |
| anuncio_id | Integer | FK para anuncios |
| created_at | DateTime | Data de envio |

### 7. denuncias
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| motivo | String(50) | Tipo de denúncia |
| descricao | Text | Descrição |
| status | Enum('pendente','resolvida') | Estado |
| utilizador_id | Integer | Utilizador que denuncia |
| anuncio_id | Integer | Anúncio denunciado |
| created_at | DateTime | Data da denúncia |

### 8. logs_admin
| Campo | Tipo | Descrição |
|-------|------|----------|
| id | Integer | Chave primária |
| acao | String(100) | Ação realizada |
| tabela_afetada | String(50) | Tabela modificada |
| registro_id | Integer | Registro afetado |
| detalhes | Text | Detalhes |
| admin_id | Integer | Administrador |
| ip_address | String(45) | Endereço IP |
| created_at | DateTime | Data da ação |

---

## Funcionalidades

### Autenticação e Gestão de Conta
- ✅ Registo de novos utilizadores com validação de email
- ✅ Login e logout seguros
- ✅ Recuperação de password por email
- ✅ Edição de perfil (nome, telefone, foto)
- ✅ Envio de email de confirmação na criação de conta

### Gestão de Anúncios
- ✅ Criar anúncios com até 5 imagens
- ✅ Editar anúncios existentes
- ✅ Eliminar anúncios
- ✅ Definir estado do artigo (Novo, Usado Bom, Usado Regular)
- ✅ Definir tipo (Venda ou Troca)
- ✅ Sistema de favoritos
- ✅ Denunciar anúncios inappropriate

### Pesquisa e Navegação
- ✅ Pesquisa por palavras-chave
- ✅ Filtrar por categoria
- ✅ Filtrar por tipo (venda/troca)
- ✅ Filtrar por localização
- ✅ Anúncios relacionados

### Mensagens
- ✅ Enviar mensagens sobre anúncios
- ✅ Caixa de mensagens
- ✅ Conversas agrupadas por contacto
- ✅ Mensagens não lidas

### Painel Administrativo
- ✅ Dashboard com estatísticas
- ✅ Gestão de utilizadores (editar, ativar/desativar, eliminar)
- ✅ Moderação de anúncios (aprovar, rejeitar)
- ✅ Gestão de categorias
- ✅ Verdenúncias
- ✅ Logs de ações

### Chat de Suporte
- ✅ Botão flutuante no canto inferior direito
- ✅ Janela de chat compacta
- ✅ Perguntas frequentes pré-definidas
- ✅ Respostas automáticas por palavras-chave

---

## Configuração e Instalação

### 1. Pré-requisitos
- Python 3.8 ou superior
- MySQL Server 8.0
- Gmail com App Password (para emails)

### 2. Instalação
```bash
# Criar ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Editar ficheiro .env com as configurações
```

### 3. Configurar Base de Dados
```bash
# Criar base de dados no MySQL
mysql -u root -p
CREATE DATABASE trocas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Criar dados iniciais
python create_data.py
```

### 4. Executar a Aplicação
```bash
python app.py
```

A aplicação está disponível em: **http://localhost:3000**

---

## Descrição dos Ficheiros

### Ficheiros Principais

#### app.py
**Descrição:** Ficheiro principal da aplicação Flask que contém todas as rotas, formulários e lógica de negócio.

**Principais secções:**
- Imports de bibliotecas (linhas 1-28)
- Configuração da aplicação Flask (linhas 30-51)
- Formulários WTForms (linhas 59-118)
- Funções auxiliares (linhas 121-176)
- Rotas públicas (linhas 185-311)
- Rotas de autenticação (linhas 313-520)
- Rotas de anúncios (linhas 522-882)
- Rotas de mensagens (linhas 760-882)
- Rotas administrativas (linhas 884-1140)
- Error handlers (linhas 1142-1156)

#### config.py
**Descrição:** Ficheiro de configurações contendo Parameters da aplicação.

**Conteúdo:**
- Configuração da base de dados MySQL
- Configuração do servidor de email
- Configurações de upload de imagens
- Chave secreta para sessões

#### models.py
**Descrição:** Definição dos modelos da base de dados usando SQLAlchemy.

**Modelos:**
- Utilizador
- Categoria
- Anuncio
- ImagemAnuncio
- Favorito
- Mensagem
- Denuncia
- LogAdmin

#### create_data.py
**Descrição:** Script para criar categorias iniciais e administrador.

**Ação:** Criar as 10 categorias base e o utilizador admin.

#### utils/email_utils.py
**Descrição:** Funções para envio de emails.

**Funções:**
- send_welcome_email() - Email de boas-vindas
- send_password_reset_email() - Email de recuperação de password
- send_account_confirmation_with_token() - Email com token de confirmação

### Ficheiros de Templates

#### src/views/index.html
**Descrição:** Página inicial com destaque de anúncios e categorias.

#### src/views/login.html
**Descrição:** Formulário de login com links para registo e recuperação de password.

#### src/views/register.html
**Descrição:** Formulário de registo de novos utilizadores.

#### src/views/support.html
**Descrição:** Centro de ajuda com assistente virtual e FAQ.

**Funcionalidades:**
- 20 perguntas frequentes organizadas por categoria
- Chat interativo live
- Mapeamento de palavras-chave para respostas automáticas

#### src/views/partials/header.html
**Descrição:** Cabeçalho comum a todas as páginas.

**Conteúdo:**
- Meta tags e título
- Estilos inline para botão flutuante e chat widget
- Menu de navegação
- Mensagens flash (sucesso/erro)
- Botão flutuante de chat
- Widget de chat compacto

#### src/views/partials/footer.html
**Descrição:** Rodapé comum a todas as páginas.

**Conteúdo:**
- Links do rodapé
- Copyright - Alegria Web Studio
- JavaScript para interatividade
- JavaScript do chat widget

### Ficheiros de Estilos

#### src/public/css/style.css
**Descrição:** Folha de estilos principal com mais de 1900 linhas.

**Secções principais:**
- Variáveis CSS (cores, espaçamentos)
- Reset e base
- Tipografia
- Cabeçalho (header)
- Menu e dropdowns
- Formulários
- Anúncios
- Mensagens
- Modal
- Painel administrativo
- Responsividade
- Animações

---

## Rotas da Aplicação

### Rotas Públicas
| Rota | Função | Descrição |
|------|-------|----------|
| / | home | Página inicial |
| /suporte | support | Centro de ajuda |
| /pesquisar | search | Pesquisa de anúncios |
| /anuncio/<id> | view_ad | Visualizar anúncio |
| /categoria/<slug> | view_category | Anúncios por categoria |
| /login | login | Página de login |
| /registar | register | Página de registo |
| /recuperar-password | forgot_password | Recuperar password |
| /recuperar-password/<token> | reset_password | Definir nova password |

### Rotas Autenticadas
| Rota | Função | Descrição |
|------|-------|----------|
| /perfil | profile | Perfil do utilizador |
| /anunciar | create_ad | Criar anúncio |
| /anuncio/<id>/editar | edit_ad | Editar anúncio |
| /anuncio/<id>/apagar | delete_ad | Apagar anúncio |
| /anuncio/<id>/favorito | toggle_favorite | Adicionar favorito |
| /anuncio/<id>/denunciar | report_ad | Denunciar anúncio |
| /mensagens | messages | Lista de conversas |
| /mensagens/<id> | conversation | Ver conversa |
| /mensagens/enviar | send_message | Enviar mensagem |
| /anuncio/<id>/mensagem | start_conversation | Nova conversa |

### Rotas Administrativas
| Rota | Função | Descrição |
|------|-------|----------|
| /admin | admin_dashboard | Painel principal |
| /admin/utilizadores | admin_users | Lista de utilizadores |
| /admin/utilizadores/<id>/editar | admin_edit_user | Editar utilizador |
| /admin/utilizadores/<id>/apagar | admin_delete_user | Apagar utilizador |
| /admin/anuncios | admin_ads | Lista de anúncios |
| /admin/anuncios/<id>/moderar | admin_moderate_ad | Aprovar/rejeitar |
| /admin/anuncios/<id>/apagar | admin_delete_ad | Apagar anúncio |
| /admin/categorias | admin_categories | Gerir categorias |
| /admin/denuncias | admin_reports | Ver denúncias |
| /admin/logs | admin_logs | Logs administrativos |

---

## Variáveis de Ambiente

O ficheiro .env deve conter:

```env
# Base de dados MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=teste123
DB_NAME=trocas_db

# Servidor
FLASK_ENV=development
SECRET_KEY=chave-secreta-aqui
PORT=3000

# Email (Gmail App Password)
MAIL_USERNAME=seuemail@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

---

## Credenciais de Teste

### Administrador
| Campo | Valor |
|-------|-------|
| Email | admin@trocas.pt |
| Password | admin123 |
| Tipo | Administrador |

### Utilizadores de Teste
| Email | Password | Tipo |
|-------|----------|------|
| joao@exemplo.pt | password123 | Utilizador |
| maria@exemplo.pt | password123 | Utilizador |
| pedro@exemplo.pt | password123 | Utilizador |

---

## Chat de Suporte

### Botão Flutuante
- **Localização:** Canto inferior direito (30px das bordas)
- **Ícone:** Auricular/headset
- **Cor:** Gradiente roxo (#6366f1 → #8b5cf6)
- **Animação:** Pulse effect contínuo

### Funcionalidades do Chat
- Abrir/fechar ao clicar no botão
- Respostas automáticas por palavras-chave
- 8 perguntas frequentes rápidas
- Link para centro de ajuda completo

### Perguntas Suportadas
O chat reconhece as seguintes palavras-chave:
- Publicar / anúncio / criar / vender
- Mensagem / mensagens / chat / conversa
- Password / recuperar / esqueci
- Perfil / editar / dados
- Favorito / heart / guardar
- Imagem / foto / upload
- Contactar / vendedor
- Eliminar / apagar

---

## Histórico de Atualizações

### 2026-04-16
- ✅ Adicionado botão flutuante de chat
- ✅ Adicionado widget de chat compacto
- ✅ Expandido FAQ para 20 perguntas
- ✅ Atualizado footer para "Alegria Web Studio"
- ✅ Removido texto "Encontre o que procura" do header
- ✅ Corrigido z-index do chat
- ✅ Documentação completa criada

### 2026-04-11
- ✅ Conversão completa de Node.js para Flask
- ✅ Base de dados MySQL configurada
- ✅ Sistema de emails implementado
- ✅ Recuperação de password com tokens
- ✅ CSS moderno criado

---

## Notas Técnicas

1. **Anúncios:** São automaticamente aprovados para utilizadores normais
2. **Imagens:** Armazenadas localmente em src/public/images/uploads/
3. **Tokens:** Têm validade de 24 horas
4. **Porto:** A aplicação corre no porto 3000 (não padrão 5000)
5. **Base de dados:** Nomeada "trocas_db" no MySQL
6. **Email:** Requer Gmail App Password (não password normal)

---

## Suporte

Para questões técnicas ou problemas, contacte através do chat de suporte na aplicação ou edemail de suporte.

---

## Deploy no Render.com

O Render é a plataforma recomendada para fazer deploy da aplicação Flask gratuitamente.

### Passos para Deploy:

#### 1. Preparar o Projeto
Já tens os ficheiros criados:
- `runtime.txt` - Define Python 3.9
- `requirements.txt` - Dependências
- `app.py` - Aplicação principal

#### 2. Criar Base de Dados MySQL no Render
1. Vai a https://render.com e cria conta
2. Cria um novo "MySQL" (free tier)
3. Anota as credenciais:
   - Host
   - Database
   - User
   - Password

#### 3. Criar o Serviço Web
1. Cria um novo "Web Service"
2. Conecta ao teu repositório GitHub
3.Configura:
   - **Build Command:** (vazio)
   - **Start Command:** `gunicorn app:app --workers 1 --timeout 120`
   - **Environment:** `Python 3`

#### 4. Variáveis de Ambiente
Adiciona no Render:
```
DB_HOST=postgres://... (do Render MySQL)
DB_USER=... (do Render MySQL)  
DB_PASSWORD=... (do Render MySQL)
DB_NAME=... (do Render MySQL)
SECRET_KEY=gera-uma-chave-secreta-aqui
FLASK_ENV=production
PORT=3000
MAIL_USERNAME=teuemail@gmail.com
MAIL_PASSWORD=teu-app-password
```

#### 5. Deploy
1. Clica em "Create Web Service"
2. Aguarda o build (pode demorar alguns minutos)
3. Obtens um URL como: `https://trocas.onrender.com`

### Notas:
- O tier gratuito suspende após 15 min de inatividade
- " acorde" automaticamente em 5-15 min após pedido
- Base de dados MySQL gratuita: $0/mês

---

## Deploy no Netlify (Estático)

Se quiseres Netlify, preciso converter para site estático. Queres que сделает isso?

**Documentação criada por:** Alegria Web Studio  
**Última atualização:** 16 de abril de 2026