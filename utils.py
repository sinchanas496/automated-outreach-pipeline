"""Shared utilities for the Automated Outreach Pipeline CLI."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Iterable


class Colors:
    """ANSI color constants used for friendly terminal output."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


@dataclass(frozen=True)
class DecisionMaker:
    """Represents a target contact at a company."""

    name: str
    designation: str
    linkedin_url: str
    email: str | None = None


@dataclass(frozen=True)
class OutreachEmail:
    """Represents a generated outreach email ready to be sent."""

    recipient: DecisionMaker
    company_domain: str
    subject: str
    body: str


def configure_logging() -> None:
    """Configure application-wide logging with a concise console format."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def colorize(message: str, color: str) -> str:
    """Wrap text in an ANSI color sequence."""

    return f"{color}{message}{Colors.RESET}"


def validate_domain(domain: str) -> str:
    """Validate and normalize a company domain entered by the user.

    Args:
        domain: Raw domain string, such as ``google.com``.

    Returns:
        A normalized lowercase domain.

    Raises:
        ValueError: If the domain is empty or does not resemble a valid domain.
    """

    normalized = domain.strip().lower().removeprefix("https://").removeprefix("http://")
    normalized = normalized.split("/")[0]
    pattern = r"^(?!-)(?:[a-z0-9-]{1,63}\.)+[a-z]{2,}$"
    if not normalized or not re.match(pattern, normalized):
        raise ValueError("Please enter a valid company domain, for example: google.com")
    return normalized


def company_name_from_domain(domain: str) -> str:
    """Convert a domain into a human-readable company name."""

    return domain.split(".")[0].replace("-", " ").title()


def print_section(title: str) -> None:
    """Print a formatted section heading."""

    print("\n" + colorize(f"=== {title} ===", Colors.BOLD + Colors.CYAN))


def summarize_count(label: str, values: Iterable[object]) -> str:
    """Return a human-readable summary line for a collection."""

    return f"{label}: {len(list(values))}"
