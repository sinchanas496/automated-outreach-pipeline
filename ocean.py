"""Mock Ocean.io-style company discovery module."""

from __future__ import annotations

import logging


class OceanClient:
    """Discovers companies similar to a seed company domain.

    This class intentionally uses deterministic mock data today, while preserving
    a client-style interface that can later call Ocean.io or another discovery API.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._sample_companies = {
            "google.com": ["openai.com", "microsoft.com", "apple.com", "meta.com", "amazon.com"],
            "stripe.com": ["squareup.com", "adyen.com", "paypal.com", "checkout.com", "plaid.com"],
            "salesforce.com": ["hubspot.com", "zoho.com", "pipedrive.com", "freshworks.com", "intercom.com"],
        }

    def find_similar_companies(self, domain: str, limit: int = 5) -> list[str]:
        """Return similar company domains for the provided seed domain."""

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        self.logger.info("Finding similar companies for %s", domain)
        fallback = [
            "hubspot.com",
            "notion.so",
            "slack.com",
            "asana.com",
            "airtable.com",
        ]
        companies = self._sample_companies.get(domain, fallback)
        return companies[:limit]
