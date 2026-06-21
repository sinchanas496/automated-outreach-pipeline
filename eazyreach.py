"""Mock EazyReach-style personalized outreach generation module."""

from __future__ import annotations

import logging

from utils import DecisionMaker, OutreachEmail, company_name_from_domain


class EazyReachClient:
    """Creates personalized outreach email copy for enriched prospects."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_email(self, contact: DecisionMaker, company_domain: str) -> OutreachEmail:
        """Create a personalized outreach email for one decision maker."""

        if not contact.email:
            raise ValueError(f"Cannot create outreach email for {contact.name}; missing email")

        company_name = company_name_from_domain(company_domain)
        first_name = contact.name.split()[0]
        subject = f"Helping {company_name} scale targeted outreach"
        body = (
            f"Hi {first_name},\n\n"
            f"I noticed your work as {contact.designation} at {company_name}. "
            "I wanted to share a concise idea for improving outbound workflows "
            "without adding extra manual research for your team.\n\n"
            f"Our automated outreach approach can help {company_name} identify "
            "relevant accounts, enrich decision-maker data, and create personalized "
            "messages faster.\n\n"
            "Would you be open to a short conversation next week?\n\n"
            "Best,\nAutomated Outreach Pipeline"
        )
        self.logger.info("Created outreach email for %s", contact.email)
        return OutreachEmail(recipient=contact, company_domain=company_domain, subject=subject, body=body)
