"""Mock Prospeo-style contact and email enrichment module."""

from __future__ import annotations

import logging

from utils import DecisionMaker


class ProspeoClient:
    """Generates decision makers and realistic work emails for companies."""

    _roles = [
        ("Maya Chen", "VP of Growth"),
        ("Ethan Brooks", "Head of Partnerships"),
        ("Sophia Patel", "Director of Revenue Operations"),
    ]

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_decision_makers(self, company_domain: str) -> list[DecisionMaker]:
        """Return sample decision makers for a company domain."""

        self.logger.info("Generating decision makers for %s", company_domain)
        company_slug = company_domain.split(".")[0]
        contacts: list[DecisionMaker] = []
        for index, (name, designation) in enumerate(self._roles, start=1):
            linkedin_url = f"https://www.linkedin.com/in/{name.lower().replace(' ', '-')}-{company_slug}-{index}"
            contacts.append(
                DecisionMaker(
                    name=name,
                    designation=designation,
                    linkedin_url=linkedin_url,
                )
            )
        return contacts

    def generate_work_email(self, contact: DecisionMaker, company_domain: str) -> DecisionMaker:
        """Attach a realistic sample email address to a decision maker."""

        first, *rest = contact.name.lower().split()
        last = rest[-1] if rest else first
        email = f"{first}.{last}@{company_domain}"
        self.logger.info("Generated email for %s at %s", contact.name, company_domain)
        return DecisionMaker(
            name=contact.name,
            designation=contact.designation,
            linkedin_url=contact.linkedin_url,
            email=email,
        )
