
from typing import Protocol


class EmailService(Protocol):
    async def send_email(self, to: str, subject: str, body: str) -> None:
        pass
class EmailServiceImpl(EmailService):
    def send_email(self, to: str, subject: str, body: str) -> None:
        # Logic to send an email (e.g., using SMTP)
        print(f"Sending email to {to} with subject '{subject}' and body '{body}'")