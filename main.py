"""Command-line entrypoint for the Automated Outreach Pipeline."""

from __future__ import annotations

import logging
import sys

from brevo import BrevoClient
from eazyreach import EazyReachClient
from ocean import OceanClient
from prospeo import ProspeoClient
from utils import Colors, colorize, configure_logging, print_section, validate_domain


class OutreachPipeline:
    """Coordinates company discovery, prospecting, copywriting, and sending."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ocean = OceanClient()
        self.prospeo = ProspeoClient()
        self.eazyreach = EazyReachClient()
        self.brevo = BrevoClient()

    def run(self, seed_domain: str) -> None:
        """Execute the full outreach pipeline for a single seed domain."""

        domain = validate_domain(seed_domain)
        print_section("Stage 1: Input")
        print(colorize(f"Seed company domain: {domain}", Colors.GREEN))

        print_section("Stage 2: Similar Companies")
        companies = self.ocean.find_similar_companies(domain)
        for company in companies:
            print(f"- {company}")

        print_section("Stage 3-4: Decision Makers and Emails")
        enriched_contacts_by_company = {}
        for company in companies:
            contacts = self.prospeo.find_decision_makers(company)
            enriched_contacts = [self.prospeo.generate_work_email(contact, company) for contact in contacts]
            enriched_contacts_by_company[company] = enriched_contacts
            print(colorize(company, Colors.YELLOW))
            for contact in enriched_contacts:
                print(f"  - {contact.name} | {contact.designation} | {contact.email} | {contact.linkedin_url}")

        print_section("Stage 5: Personalized Outreach Emails")
        outreach_emails = []
        for company, contacts in enriched_contacts_by_company.items():
            for contact in contacts:
                outreach = self.eazyreach.create_email(contact, company)
                outreach_emails.append(outreach)
                print(colorize(f"Subject: {outreach.subject}", Colors.BLUE))
                print(outreach.body)
                print("-" * 72)

        print_section("Stage 6: Safety Checkpoint")
        decision_maker_count = sum(len(contacts) for contacts in enriched_contacts_by_company.values())
        print(f"Companies found: {len(companies)}")
        print(f"Decision makers found: {decision_maker_count}")
        print(f"Emails generated: {len(outreach_emails)}")

        if not self._confirm_outreach():
            print(colorize("Outreach cancelled. Exiting gracefully.", Colors.YELLOW))
            return

        print_section("Stage 7: Simulated Sending")
        sent_count = 0
        for outreach in outreach_emails:
            if self.brevo.send_email(outreach):
                sent_count += 1

        print_section("Execution Summary")
        print(colorize(f"Pipeline completed. Sent {sent_count} of {len(outreach_emails)} emails.", Colors.GREEN))

    @staticmethod
    def _confirm_outreach() -> bool:
        """Ask the user for final confirmation before simulated outreach."""

        while True:
            answer = input(colorize("Proceed with outreach? (Y/N): ", Colors.BOLD)).strip().lower()
            if answer in {"y", "yes"}:
                return True
            if answer in {"n", "no"}:
                return False
            print(colorize("Please enter Y or N.", Colors.RED))


def main() -> int:
    """Parse CLI input and run the pipeline."""

    configure_logging()
    logger = logging.getLogger("main")
    try:
        seed_domain = sys.argv[1] if len(sys.argv) > 1 else input("Enter company domain: ")
        OutreachPipeline().run(seed_domain)
        return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 130
    except ValueError as exc:
        logger.error("Validation error: %s", exc)
        print(colorize(f"Error: {exc}", Colors.RED))
        return 1
    except Exception as exc:  # Defensive top-level handler for a CLI application.
        logger.exception("Unexpected pipeline failure")
        print(colorize(f"Unexpected error: {exc}", Colors.RED))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
