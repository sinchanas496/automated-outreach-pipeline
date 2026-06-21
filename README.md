# Automated Outreach Pipeline

A complete Python command-line application for an SDE internship assignment. The app accepts a company domain, discovers similar companies using mock data, generates sample decision makers, creates realistic work emails, writes personalized outreach copy, shows a safety checkpoint, and simulates sending emails.

## Project Overview

The goal is to demonstrate a production-minded outreach workflow without requiring paid APIs or external credentials. Every integration is represented by a small client class whose public methods can later be replaced with real API calls.

Pipeline stages:

1. Accept a single company domain.
2. Generate five similar company domains with mock Ocean.io-style data.
3. Generate decision makers for each company with mock Prospeo-style data.
4. Generate realistic work emails for each decision maker.
5. Create personalized outreach emails with company and contact details.
6. Display a safety checkpoint and ask for confirmation.
7. Simulate sending emails if the user confirms.

## Architecture

```text
project/
├── main.py          # CLI entrypoint and pipeline orchestration
├── ocean.py         # Mock company discovery client
├── prospeo.py       # Mock decision-maker and email enrichment client
├── eazyreach.py     # Mock personalized email generation client
├── brevo.py         # Mock email sending client
├── utils.py         # Shared dataclasses, validation, logging, and terminal colors
├── requirements.txt # Runtime dependency notes
└── README.md        # Documentation
```

### Module Responsibilities

- `main.py` owns the command-line flow, user confirmation, error handling, and execution summary.
- `ocean.py` contains `OceanClient`, which returns similar company domains.
- `prospeo.py` contains `ProspeoClient`, which returns decision makers and generates emails.
- `eazyreach.py` contains `EazyReachClient`, which creates personalized outreach messages.
- `brevo.py` contains `BrevoClient`, which simulates email delivery.
- `utils.py` contains reusable dataclasses, input validation, logging setup, and colored output helpers.

## Execution Steps

### 1. Clone or open the project

```bash
cd automated-outreach-pipeline
```

### 2. Optional: create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

No third-party dependencies are required, but this command is safe to run:

```bash
pip install -r requirements.txt
```

### 4. Run the app

Pass the domain as an argument:

```bash
python main.py google.com
```

Or run interactively:

```bash
python main.py
```

When the safety checkpoint appears, enter `Y` to simulate sending or `N` to exit gracefully.

## Future API Integration Points

- Replace `OceanClient.find_similar_companies()` with a real Ocean.io company search request.
- Replace `ProspeoClient.find_decision_makers()` and `generate_work_email()` with Prospeo or another enrichment provider.
- Replace `EazyReachClient.create_email()` with a real AI copy-generation or template-personalization service.
- Replace `BrevoClient.send_email()` with Brevo's transactional email API.
- Add environment-based configuration for API keys, base URLs, timeouts, retries, and rate limiting.

## Error Handling and Logging

The CLI validates domains, handles invalid input gracefully, logs each major integration step, and catches unexpected failures at the top level. This keeps the demo easy to run while showing an architecture that can evolve into a production service.

## Example

```bash
python main.py google.com
```

Expected behavior:

- Prints five similar companies.
- Prints sample decision makers and generated emails.
- Prints personalized outreach email drafts.
- Shows a safety checkpoint.
- Simulates sending only after confirmation.
