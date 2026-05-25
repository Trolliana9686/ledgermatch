# LedgerMatch

LedgerMatch is a transaction reconciliation system designed to identify mismatches between internal financial records and external payment data.

## Problem
Financial institutions and operations teams must reconcile transactions between multiple systems (e.g., internal ledgers vs bank statements). Manual reconciliation is time-consuming and error-prone.

## Solution
LedgerMatch automates this process by:
- Ingesting two datasets (internal vs external)
- Matching transactions based on amount, date, and description
- Detecting mismatches and missing entries
- Producing a reconciliation report

## Tech Stack
- FastAPI (API layer)
- pandas (data processing)
- python-Levenshtein (fuzzy matching)

## Features (Planned)
- Exact and fuzzy transaction matching
- Mismatch classification (missing, duplicate, amount discrepancy)
- REST API for reconciliation jobs
- CSV upload + output reports

## Example Use Case
- Compare internal payment system vs bank export
- Identify missing transactions
- Detect incorrect amounts
- Generate reconciliation summary

## Status
In development
