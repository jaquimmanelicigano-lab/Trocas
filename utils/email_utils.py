"""
Módulo de Envio de Emails
=========================
Funções utilities para enviar emails via SMTP
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


def send_email(to_email, subject, html_content, text_content=None):
    """
    Envia um email para o destinatário especificado
    
    Args:
        to_email: Email do destinatário
        subject: Assunto do email
        html_content: Conteúdo do email em HTML
        text_content: Conteúdo do email em texto plano (opcional)
    
    Returns:
        bool: True se email foi enviado com sucesso, False caso contrário
    """
    # Configurações do servidor SMTP
    mail_server = current_app.config.get('MAIL_SERVER')
    mail_port = current_app.config.get('MAIL_PORT')
    mail_username = current_app.config.get('MAIL_USERNAME')
    mail_password = current_app.config.get('MAIL_PASSWORD')
    mail_use_tls = current_app.config.get('MAIL_USE_TLS', True)
    
    # Se não houver configuração de email, retorna False
    if not mail_username or not mail_password:
        print(f"[EMAIL] Configuração não encontrada. Email não enviado para {to_email}")
        return False
    
    try:
        # Criar mensagem multipart
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = mail_username
        message["To"] = to_email
        
        # Adicionar versões texto e HTML
        if text_content:
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Criar contexto SSL seguro
        context = ssl.create_default_context()
        
        # Conectar ao servidor SMTP e enviar
        with smtplib.SMTP(mail_server, mail_port) as server:
            if mail_use_tls:
                server.starttls(context=context)
            server.login(mail_username, mail_password)
            server.sendmail(mail_username, to_email, message.as_string())
        
        print(f"[EMAIL] Email enviado com sucesso para {to_email}")
        return True
        
    except Exception as e:
        print(f"[EMAIL] Erro ao enviar email: {str(e)}")
        return False


def send_password_reset_email(utilizador, token):
    """
    Envia email com link para recuperação de password
    
    Args:
        utilizador: Objeto do modelo Utilizador
        token: Token de recuperação
    """
    subject = "Recuperar Password - Trocas.pt"
    
    reset_link = f"http://localhost:3000/recuperar-password/{token}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 30px; border-radius: 10px; text-align: center;">
            <h1 style="color: white; margin: 0;">Recuperar Password</h1>
        </div>
        <div style="padding: 30px; background: #f8fafc; border-radius: 0 0 10px 10px;">
            <p>Olá <strong>{utilizador.nome}</strong>,</p>
            <p>Recebemos um pedido para recuperar a sua password.</p>
            <p>Clique no botão abaixo para criar uma nova password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">Recuperar Password</a>
            </div>
            <p style="color: #64748b; font-size: 14px;">
                Este link expira em 24 horas.<br>
                Se não pediu esta recuperação, ignore este email.
            </p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Recuperar Password - Trocas.pt
    
   Olá {utilizador.nome},
    
    Recebemos um pedido para recuperar a sua password.
    
    Clique no link abaixo para criar uma nova password:
    {reset_link}
    
     Este link expira em 24 horas.
    Se não pediu esta recuperação, ignore este email.
    """
    
    return send_email(utilizador.email, subject, html_content, text_content)


def send_account_confirmation_with_token(utilizador, token):
    """
    Envia email de confirmação de conta com token de recuperação
    
    Args:
        utilizador: Objeto do modelo Utilizador
        token: Token de recuperação incluído no email
    """
    subject = "Confirmação de Conta - Trocas.pt"
    
    reset_link = f"http://localhost:3000/recuperar-password/{token}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 30px; border-radius: 10px; text-align: center;">
            <h1 style="color: white; margin: 0;">Conta Criada com Sucesso!</h1>
        </div>
        <div style="padding: 30px; background: #f8fafc; border-radius: 0 0 10px 10px;">
            <p>Olá <strong>{utilizador.nome}</strong>,</p>
            <p>Obrigado por se registrar no Trocas.pt! A sua conta foi criada com sucesso.</p>
            <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0; border: 1px solid #e2e8f0;">
                <p style="margin: 0;"><strong>Email:</strong> {utilizador.email}</p>
                <p style="margin: 10px 0 0 0;"><strong>Telefone:</strong> {utilizador.telefone}</p>
            </div>
            <p><strong>Guarde o seguinte token:</strong></p>
            <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; text-align: center; font-family: monospace; font-size: 18px; letter-spacing: 2px; margin: 15px 0;">
                {token}
            </div>
            <p style="color: #64748b; font-size: 14px;">
                Este token pode ser usado para recuperar a sua password se a esquecer.<br>
                Guarde-o num local seguro!
            </p>
            <a href="http://localhost:3000/" style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-top: 10px;">Explorar Anúncios</a>
            <p style="margin-top: 30px; color: #64748b; font-size: 14px;">
                Equipa Trocas.pt
            </p>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""Conta Criada com Sucesso!Olá {utilizador.nome},Obrigado por se registrar no Trocas.pt!Email: {utilizador.email}
Telefone: {utilizador.telefone}Seu token: {token}Guarde este token para recuperação de password.
Equipa Trocas.pt"""
    
    return send_email(utilizador.email, subject, html_content, text_content)
