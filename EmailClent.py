import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List, Optional


class EmailClient:
    """
    Класс для отправки электронных писем через SMTP сервер
    """

    def __init__(self, smtp_server: str, port: int, email: str, password: str, use_tls: bool = True):
        """
        Инициализация клиента

        Args:
            smtp_server: SMTP сервер (например, 'smtp.gmail.com')
            port: Порт SMTP сервера (например, 587 для TLS, 465 для SSL)
            email: Email адрес отправителя
            password: Пароль или app-пароль
            use_tls: Использовать TLS шифрование
        """
        self.smtp_server = smtp_server
        self.port = port
        self.email = email
        self.password = password
        self.use_tls = use_tls

    def send_email(
            self,
            to_emails: List[str],
            subject: str,
            body: str,
            is_html: bool = False,
            attachments: Optional[List[str]] = None,
            cc_emails: Optional[List[str]] = None,
            bcc_emails: Optional[List[str]] = None
    ) -> bool:
        """
        Отправка email сообщения

        Args:
            to_emails: Список email получателей
            subject: Тема письма
            body: Текст письма
            is_html: Является ли тело письма HTML
            attachments: Список путей к файлам для прикрепления
            cc_emails: Список email для копии
            bcc_emails: Список email для скрытой копии

        Returns:
            bool: Успешно ли отправлено письмо
        """
        try:
            # Создание сообщения
            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = ", ".join(to_emails)
            message["Subject"] = subject

            if cc_emails:
                message["Cc"] = ", ".join(cc_emails)

            # Добавление тела письма
            if is_html:
                message.attach(MIMEText(body, "html"))
            else:
                message.attach(MIMEText(body, "plain"))

            # Добавление вложений
            if attachments:
                for file_path in attachments:
                    self._attach_file(message, file_path)

            # Получатели
            all_recipients = to_emails.copy()
            if cc_emails:
                all_recipients.extend(cc_emails)
            if bcc_emails:
                all_recipients.extend(bcc_emails)

            # Отправка через SMTP
            with self._create_smtp_connection() as server:
                server.sendmail(self.email, all_recipients, message.as_string())

            print(f"Письмо успешно отправлено для {len(all_recipients)} получателей")
            return True

        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")
            return False

    def _create_smtp_connection(self):
        """Создание SMTP соединения с отключенной проверкой SSL"""
        # Создаем контекст SSL с отключенной проверкой сертификатов
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        if self.use_tls:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls(context=context)  # Используем наш контекст без проверки
        else:
            # Для SSL
            server = smtplib.SMTP_SSL(self.smtp_server, self.port, context=context)

        server.login(self.email, self.password)
        return server

    def _attach_file(self, message: MIMEMultipart, file_path: str):
        """Прикрепление файла к сообщению"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            # Получаем имя файла из пути
            filename = os.path.basename(file_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            message.attach(part)
            print(f"Файл {filename} прикреплен к письму")

        except Exception as e:
            print(f"Ошибка при прикреплении файла {file_path}: {e}")
            raise

    def test_connection(self) -> bool:
        """Тестирование подключения к SMTP серверу"""
        try:
            with self._create_smtp_connection() as server:
                print("Подключение к SMTP серверу успешно")
                return True
        except Exception as e:
            print(f"Ошибка подключения к SMTP серверу: {e}")
            return False