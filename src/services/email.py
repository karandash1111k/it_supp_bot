import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.core.config import Config
import os
import logging

logger = logging.getLogger(__name__)

class EmailService:
    # метод для загрузки шаблона письма
    @staticmethod
    def _load_template(template_name: str, **kwargs) -> str:
        templates_dir = os.path.join(os.path.dirname(__file__), '../../templates')
        template_path = os.path.join(templates_dir, template_name)

        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content.format(**kwargs)

    # метод для отправки email
    @staticmethod
    async def send_email(to: str, subject: str, template_name: str, **kwargs) -> bool:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = Config.SMTP_FROM
            msg['To'] = to

            # html шаблон
            html_content = EmailService._load_template(template_name, **kwargs)
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))

            # установка соединения с SMTP-сервером
            with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    # статический метод для отправки кода подтверждения
    @staticmethod
    async def send_verification_code(email: str, code: str) -> bool:
        subject = "Ваш код подтверждения для IT Support Bot"
        return await EmailService.send_email(
            email,
            subject,
            'index'
            '.html',
            code=code,
            email=email
        )