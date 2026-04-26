# Sistema de Destaque de Anúncios — Implementação

## Funcionalidades implementadas

### 1. Modelo de Dados (models.py)
- Campos adicionados à tabela `anuncios`:
  - `destacado` (Boolean) — se o anúncio está destacado
  - `tipo_destaque` (Enum: 'destaque', 'premium')
  - `destaque_inicio` (DateTime) — início do período de destaque
  - `destaque_fim` (DateTime) — fim do período de destaque (7 dias)
  - `destaque_valor` (Numeric) — valor pago (4.50 €)
  - `metodo_pagamento` (String) — 'mbway', 'paypal' ou 'cartao'
  - `transacao_id` (String) — referência da transação

### 2. Formulário (app.py → AdForm)
- Campo `destacar` (BooleanField) adicionado — checkbox para solicitar destaque.

### 3. Rota de Criação (`/anunciar`)
- Quando o checkbox `destacar` está marcado:
  - O anúncio é criado com `status = 'pendente'`
  - Redireciona para a página de pagamento
- Quando não marcado:
  - O anúncio é criado normalmente com `status = 'ativo'`

### 4. Rota de Pagamento (`/destaque/pagamento/<anuncio_id>`)
- Página de pagamento fictício com opções:
  - **MB Way** — pagamento instantâneo
  - **PayPal** — pagamento via conta PayPal
  - **Cartão (Visa/Mastercard)** — cartão de crédito/débito
- Para cartão:
  - Campos: número, validade, CVV
  - Detecção automática da bandeira (Visa/Mastercard) via API AJAX `/destaque/check-band`
- Ao submeter:
  - Gera ID de transação aleatório (TRXxxxxxxxxxxxx)
  - Marca `anuncio.destacado = True`
  - Define `destaque_inicio = agora`, `destaque_fim = agora + 7 dias`
  - Define `destaque_valor = 4.50`
  - Salva método de pagamento e transacao_id
  - Redireciona para a página do anúncio com flash de sucesso

### 5. API de Detecção de Cartão (`/destaque/check-band`)
- Endpoint POST que recebe JSON `{numero: string}`
- Detecta bandeira:
  - Começa com `4` → Visa
  - Começa com `51-55` → Mastercard
- Retorna JSON `{bandeira: 'visa' | 'mastercard' | null}`

### 6. Templates

#### `src/views/create-ad.html`
- Adicionada seção de opção de destaque:
  - Checkbox "Destacar Anúncio"
  - Texto: "Aumente a visibilidade do seu anúncio por apenas 4,50 €"
  - Informação extra: anúncios destacados aparecem no topo

#### `src/views/payment.html` (novo)
- Página de pagamento com:
  - Resumo do pedido (título do anúncio, serviço, total)
  - Seleção de método de pagamento (radio buttons)
  - Campos de cartão (aparecem apenas se "Cartão" selecionado)
  - Detecção de bandeira com ícone colorido
  - Máscaras de entrada (formatação automática de número e validade)
  - Botões "Pagar 4,50 €" e "Cancelar"
  - Mensagem de segurança

#### `src/views/ad.html`
- Modificações:
  - Se o anúncio está **destacado**: mostra badge dourado com ícone de estrela e data de fim
  - Se o utilizador é o dono e o anúncio **não está destacado**: mostra bloco CTA com botão "Destacar Agora" que leva à página de pagamento
  - Se não é o dono: não mostra nada (apenas ações normais)

### 7. Estilos (inline nos templates)
- Botão flutuante de chat: `.floating-chat-btn` (já existia)
- Chat widget: `.chat-widget` (já existia)
- **Novos estilos inline** (para evitar editar style.css):
  - Badge de destaque: gradiente dourado com sombra
  - CTA de destaque: gradiente roxo com botão branco

## Como testar

1. **Reinicie a aplicação** — para carregar o novo modelo (db.create_all() aplica as colunas novas automaticamente)
2. **Faça login** como utilizador normal
3. **Crie um anúncio** e marque a opção "Destacar Anúncio"
4. Será redirecionado para `/destaque/pagamento/<id>`
5. Escolha MB Way, PayPal ou Cartão
6. Para Cartão, preencha número (Visa começa com 4, Mastercard começa com 51-55)
7. Clique "Pagar 4,50 €"
8. Será redirecionado para a página do anúncio
9. O anúncio deve mostrar o **badge dourado "Anúncio Destacado"**
10. O destaque dura 7 dias

## Notas técnicas

- Valor do destaque: **4,50 € fixos** (pode ser alterado no código)
- Duração: **7 dias** (`timedelta(days=7)`)
- Pagamento é **simulado/fictício** — não há integração real
- O anúncio fica `status='pendente'` até pagamento confirmado
- Apenas o dono do anúncio pode destacá-lo
- Um anúncio só pode ser destacado uma vez (campo `destacado` booleano)
- A detecção de bandeira funciona apenas com números de cartão válidos (6+ dígitos)

## Arquivos modificados

### Backend
- `models.py` — colunas de destaque na classe `Anuncio`
- `app.py`:
  - Importado `random` e `string`
  - Adicionado campo `destacar` no `AdForm`
  - Rota `create_ad` atualizada para redirecionar para pagamento
  - Novas rotas: `payment()` e `check_card_band()`
  - Rota `view_ad` agora passa `pode_destacar` para o template

### Frontend
- `src/views/create-ad.html` — checkbox de destaque adicionada
- `src/views/payment.html` — Nova página de pagamento (criada)
- `src/views/ad.html` — Badge de destaque e botão CTA

## Migração de banco de dados

**Se você já tem dados no banco**, precisa executar a migração:

```bash
python migrate_schema.py
```

Se houver erro de bloqueio, pare o servidor e execute:

```bash
python reset_db.py   # APAGA TODOS OS DADOS e recria schema
```

Após migrar/recriar, reinicie a aplicação.
