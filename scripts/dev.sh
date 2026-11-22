#!/usr/bin/env bash
# Development helper: scripts/dev.sh db|test|run
# Uses a private PostgreSQL cluster (Unix socket only), so no root is needed.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ODOO_HOME="${ODOO_HOME:-$HOME/odoo}"
PG_BIN="${PG_BIN:-/usr/lib/postgresql/18/bin}"
STATE="${XDG_DATA_HOME:-$HOME/.local/share}/odoopayout"
PG_PORT=5442
MODULE=marketplace_payout

start_db() {
    mkdir -p "$STATE"
    if [ ! -d "$STATE/pg" ]; then
        "$PG_BIN/initdb" -D "$STATE/pg" --auth=peer -E UTF8 --locale=C.UTF-8 >/dev/null
    fi
    if ! "$PG_BIN/pg_ctl" -D "$STATE/pg" status >/dev/null; then
        "$PG_BIN/pg_ctl" -D "$STATE/pg" -l "$STATE/pg.log" -w \
            -o "-k $STATE -p $PG_PORT -c listen_addresses=''" start >/dev/null
    fi
}

odoo() {
    "$ODOO_HOME/venv/bin/python" "$ODOO_HOME/odoo-bin" -c "$ROOT/odoo.conf" \
        --addons-path="$ODOO_HOME/addons,$ROOT" --data-dir="$STATE/data" \
        --db_host="$STATE" --db_port="$PG_PORT" --db_user="$(id -un)" "$@"
}

start_db
case "${1:-}" in
    db) echo "PostgreSQL ready: socket $STATE, port $PG_PORT" ;;
    test)
        # Fresh database every time, so installation is tested too.
        "$PG_BIN/dropdb" -h "$STATE" -p "$PG_PORT" --if-exists payout_test
        odoo -d payout_test -i "$MODULE" --test-tags "/$MODULE" --http-port=8071 --stop-after-init ;;
    run) odoo -d payout_dev -i "$MODULE" -u "$MODULE" --dev=xml ;;
    *) echo "usage: $0 db|test|run" >&2; exit 2 ;;
esac
