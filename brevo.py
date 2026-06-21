"""Mock Brevo-style email sending module."""

from __future__ import annotations

import logging

from utils import OutreachEmail


class BrevoClient:
    """Simulates sending outreach emails.

    The public method mirrors what a real transactional email provider wrapper
    would expose, making future Brevo API integration straightforward.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_email(self, email: OutreachEmail) -> bool:
        """Simulate sending one email and return whether it succeeded."""

        if not email.recipient.email:
            raise ValueError("Recipient email is required before sending")

        self.logger.info("Simulated send to %s", email.recipient.email)
        print(f"Email sent successfully to {email.recipient.email}")
        return True
