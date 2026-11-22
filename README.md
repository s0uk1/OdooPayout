# OdooPayout

Marketplace payouts for Odoo 19: track what each seller is owed, group it into
payout batches, get them approved, and send them to a payment provider safely.

The addon lives in `marketplace_payout/`. See [ROADMAP.md](ROADMAP.md) for progress.

## Development

Needs an Odoo 19 checkout in `~/odoo` (override with `ODOO_HOME`), with its
virtualenv in `venv/`, and the PostgreSQL 18 binaries.

    scripts/dev.sh test   # fresh install + tests
    scripts/dev.sh run    # http://localhost:8070
