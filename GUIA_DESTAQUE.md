# GUIA RÁPIDO — Sistema de Destaque de Anúncios

## O que foi implementado

✅ **Sistema completo de destaque**:
- Checkbox "Destacar Anúncio" na criação
- Página de pagamento fictícia com MB Way, PayPal e Cartão
- Detecção automática de bandeira (Visa/Mastercard)
- Anúncios destacados mostram badge dourado
- Botão "Destacar Agora" na página do anúncio (para o dono)
- Validade de 7 dias, custo 4,50 €

## Passos para ativar

### 1. Feche a aplicação
- Pare o servidor Flask se estiver rodando (`Ctrl+C` no terminal)
- Feche todos os terminais Python abertos

### 2. Reset do banco de dados
**ATENÇÃO**: Este passo apaga TODOS os anúncios, mensagens e favoritos existentes.
Se quiser preservar dados, faça backup manual do `instance/trocas.db` primeiro.

Abja um **novo** terminal (PowerShell ou CMD) e execute:

```bash
cd C:\Users\clash\Desktop\trocas
python reset_db.py
```

Se `reset_db.py` falhar por banco bloqueado, use o batch:

```bash
RESET_DB.bat
```

Este script vai:
- Apagar `instance/trocas.db`
- Criar novo banco com todas as colunas de destaque

### 3. Reinicie a aplicação

```bash
python app.py
```

O servidor estará em `http://localhost:3000` ou `http://172.16.2.228:3000`

### 4. Teste o sistema

1. Faça login como utilizador normal (não admin)
2. Vá a `/anunciar`
3. Preencha o formulário e **marque a opção "Destacar Anúncio"**
4. Clique em "Publicar Anúncio Agora"
5. Você será redirecionado para a página de **Pagamento**
6. Escolha um método:
   - **MB Way** — apenas selecione
   - **PayPal** — apenas selecione
   - **Cartão** — preencha número (teste: `4242 4242 4242 4242` para Visa, `5555 5555 5555 4444` para Mastercard)
7. Clique "Pagar 4,50 €"
8. Você será redirecionado para a página do anúncio
9. **O anúncio deve mostrar um badge dourado** "Anúncio Destacado" com data de fim
10. No menu do utilizador, pode ver o anúncio em "Os meus anúncios"

## Arquivos criados/modificados

### Backend
- `models.py` — colunas de destaque na classe `Anuncio`
- `app.py` — `AdForm.destacar`, rotas `payment()` e `check_card_band()`
- `models.py` chave `destacado`, `tipo_destaque`, `destaque_inicio`, `destaque_fim`, `destaque_valor`, `metodo_pagamento`, `transacao_id`

### Frontend
- `src/views/create-ad.html` — checkbox de destaque
- `src/views/payment.html` — nova página
- `src/views/ad.html` — badge e botão de destaque
- `src/views/partials/header.html` — CSS chat widget
- `src/views/partials/footer.html` — JS chat widget

### Scripts
- `migrate_schema.py` — migração manual (opcional)
- `reset_db.py` — recria banco (usado no passo 2)
- `RESET_DB.bat` — batch para reset fácil
- `SISTEMA_DESTAQUE.md` — documentação completa

## Observações

- Pagamento é **simulado/fictício** — não há processamento real
- Destaque dura **7 dias** a partir do pagamento
- Custo fixo: **4,50 €**
- Após 7 dias, o anúncio perde o destaque (não há job automático — seria necessário um cron)
- Apenas o dono do anúncio pode destacá-lo
- O anúncio fica `pendente` até pagamento confirmado, depois `ativo`

## Problemas comuns

### Banco bloqueado
Se `reset_db.py` falhar com `PermissionError`:
- Feche todos os terminais Python
- Use o gerenciador de tarefas para matar `python.exe`
- Execute `RESET_DB.bat` como administrador

### Erro "no such column: destacado"
Significa que o banco não tem as novas colunas. Execute `reset_db.py`.

### Erro no pagamento
Verifique que está logado e que o anúncio pertence a você.

## Próximas melhorias (sugestões)

- Integração com pagamento real (Stripe, PayPal API, MB Way API)
- Painel admin para gerenciar destaques
- Job agendado para expirar destaques automaticamente
- Notificação por email quando destaque estiver perto de expirar
- Estatísticas de visualizações antes/depois do destaque
- Tipo "premium" com valor diferente e mais benefícios
- Cupom de desconto para múltiplos destaques

---
Sistema pronto para uso!
