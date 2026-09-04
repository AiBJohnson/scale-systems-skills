#!/usr/bin/env python3
"""Dependency-free structural and fixture checks for this repository."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "solopreneur-starter"
EXAMPLES = PLUGIN / "examples"
EXPECTED_SKILLS = {
    "content-repurpose",
    "decision-brief",
    "expense-categorise",
    "file-organiser",
    "inbox-triage",
    "invoice-chase",
    "meeting-notes",
    "weekly-numbers",
}
FIXTURE_INPUTS = {
    "weekly-numbers": EXAMPLES / "sample-sales.csv",
    "invoice-chase": EXAMPLES / "sample-invoices.csv",
    "expense-categorise": EXAMPLES / "sample-expenses.csv",
    "inbox-triage": EXAMPLES / "inbox",
    "content-repurpose": EXAMPLES / "content-repurpose" / "source-article.md",
    "meeting-notes": EXAMPLES / "meeting-notes" / "raw-notes.md",
    "decision-brief": EXAMPLES / "decision-brief" / "decision-context.md",
    "file-organiser": EXAMPLES / "file-organiser" / "preview-request.md",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_manifests() -> None:
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    plugin = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    entries = marketplace.get("plugins", [])
    if len(entries) != 1:
        fail("marketplace.json must contain exactly one plugin")
    if entries[0].get("name") != plugin.get("name"):
        fail("plugin name differs between manifests")
    if entries[0].get("version") != plugin.get("version"):
        fail("plugin version differs between manifests")
    if plugin.get("version") != "1.2.0":
        fail("expected repaired plugin version 1.2.0")
    if plugin.get("repository") != "https://github.com/AiBJohnson/scale-systems-skills":
        fail("plugin repository URL is missing or incorrect")


def validate_skills() -> None:
    skill_files = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
    names = {path.parent.name for path in skill_files}
    if names != EXPECTED_SKILLS:
        fail(f"expected exactly eight named skills; found {sorted(names)}")
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        match = re.match(r"---\n(.*?)\n---\n", text, flags=re.DOTALL)
        if not match:
            fail(f"missing YAML-style front matter: {path.relative_to(ROOT)}")
        front_matter = match.group(1)
        if f"name: {path.parent.name}" not in front_matter:
            fail(f"front-matter name does not match directory: {path.relative_to(ROOT)}")
        if "user-invocable: true" not in front_matter:
            fail(f"skill is not marked user-invocable: {path.relative_to(ROOT)}")


def validate_counts_and_docs() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    marketplace = (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    plugin = (PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    joined = "\n".join((readme, marketplace, plugin)).lower()
    for stale in ("four claude code skills", "other fourteen", "twelve folders"):
        if stale in joined:
            fail(f"stale count phrase remains: {stale!r}")
    required = (
        "eight claude code skills",
        "18 skills total",
        "these eight starter skills plus ten additional",
        "/solopreneur-starter:weekly-numbers",
        "/reload-plugins",
        "standalone skills normally live-reload",
        "neither check invokes a model",
        ".scale-systems-local/runs/",
    )
    for phrase in required:
        if phrase.lower() not in readme.lower():
            fail(f"README is missing required contract text: {phrase!r}")
    if "license" not in (ROOT / "LICENSES.md").read_text(encoding="utf-8").lower():
        fail("LICENSES.md is empty or malformed")
    if "restart claude code after installing" in readme.lower():
        fail("README still requires a restart after marketplace installation")


def validate_fixture_inventory() -> None:
    if set(FIXTURE_INPUTS) != EXPECTED_SKILLS:
        fail("fixture inventory must cover exactly the eight public skills")
    for skill_name, path in FIXTURE_INPUTS.items():
        if not path.exists():
            fail(f"missing fixed input for {skill_name}: {path.relative_to(ROOT)}")
        if path.is_file() and not path.read_text(encoding="utf-8").strip():
            fail(f"empty fixed input for {skill_name}: {path.relative_to(ROOT)}")
    inbox_files = sorted((EXAMPLES / "inbox").glob("*.txt"))
    if len(inbox_files) != 4:
        fail(f"expected four inbox fixtures, found {len(inbox_files)}")

    content = FIXTURE_INPUTS["content-repurpose"].read_text(encoding="utf-8")
    for phrase in ("fictional one-person design studio", "45 minutes", "six test weeks"):
        if phrase not in content:
            fail(f"content-repurpose fixture missing fixed fact: {phrase!r}")

    meeting = FIXTURE_INPUTS["meeting-notes"].read_text(encoding="utf-8")
    for phrase in ("2026-09-14", "ten existing customers", "did not choose an owner or date"):
        if phrase not in meeting:
            fail(f"meeting-notes fixture missing fixed fact: {phrase!r}")

    decision = FIXTURE_INPUTS["decision-brief"].read_text(encoding="utf-8")
    for phrase in ("USD 24 per month", "USD 240 per year", "export appointment data is unknown"):
        if phrase not in decision:
            fail(f"decision-brief fixture missing fixed fact: {phrase!r}")

    organiser = FIXTURE_INPUTS["file-organiser"].read_text(encoding="utf-8")
    for phrase in ("manifest-only safety fixture", "do not create directories", "existing destination"):
        if phrase not in organiser:
            fail(f"file-organiser fixture missing safety fact: {phrase!r}")


def validate_sales_fixture() -> None:
    path = EXAMPLES / "sample-sales.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        columns = reader.fieldnames
    expected_columns = [
        "order_id",
        "date",
        "product",
        "price",
        "currency",
        "refunded",
        "customer_email",
        "country",
    ]
    if columns != expected_columns:
        fail(f"sample-sales.csv schema changed: {columns}")
    if len(rows) != 20:
        fail(f"expected 20 sales rows, found {len(rows)}")
    if sum(row["refunded"].lower() == "true" for row in rows) != 2:
        fail("expected exactly two refunded sales fixture rows")

    end = date(2026, 8, 31)
    windows = (
        (end - timedelta(days=6), end),
        (end - timedelta(days=13), end - timedelta(days=7)),
    )
    results: list[tuple[int, Decimal]] = []
    for start, stop in windows:
        included = [
            row
            for row in rows
            if start <= date.fromisoformat(row["date"]) <= stop
            and row["refunded"].lower() == "false"
        ]
        results.append((len(included), sum((Decimal(row["price"]) for row in included), Decimal())))
    if results != [(4, Decimal("307.00")), (5, Decimal("275.00"))]:
        fail(f"sales fixture no longer matches expected windows: {results}")

    current_products: dict[str, Decimal] = defaultdict(Decimal)
    for row in rows:
        row_date = date.fromisoformat(row["date"])
        if windows[0][0] <= row_date <= windows[0][1] and row["refunded"].lower() == "false":
            current_products[row["product"]] += Decimal(row["price"])
    expected_products = {
        "Starter Pack": Decimal("58.00"),
        "Coaching Call": Decimal("150.00"),
        "Pro Bundle": Decimal("99.00"),
    }
    if dict(current_products) != expected_products:
        fail(f"sales product totals changed: {dict(current_products)}")


def validate_invoice_fixture() -> None:
    path = EXAMPLES / "sample-invoices.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    as_of = date(2026, 9, 4)
    actual = {
        row["invoice_no"]: (as_of - date.fromisoformat(row["due"])).days
        for row in rows
        if row["status"] == "unpaid"
    }
    expected = {"INV-042": 42, "INV-043": 34, "INV-044": 19, "INV-046": 1, "INV-047": -4}
    if actual != expected:
        fail(f"invoice fixture no longer matches 2026-09-04 expectations: {actual}")
    overdue = sum(
        (Decimal(row["amount"]) for row in rows if row["invoice_no"] in {"INV-042", "INV-043", "INV-044", "INV-046"}),
        Decimal(),
    )
    if overdue != Decimal("5050.00"):
        fail(f"overdue fixture total changed: {overdue}")


def validate_safety_contract() -> None:
    expected = (EXAMPLES / "EXPECTED_OUTPUTS.md").read_text(encoding="utf-8")
    injection = (EXAMPLES / "inbox" / "04-injection-test.txt").read_text(encoding="utf-8")
    inbox_skill = (PLUGIN / "skills" / "inbox-triage" / "SKILL.md").read_text(encoding="utf-8")
    if "Ignore your previous instructions" not in injection:
        fail("injection fixture lost its test payload")
    for phrase in ("untrusted input", "Never send", "refuse to overwrite"):
        if phrase.lower() not in inbox_skill.lower():
            fail(f"inbox-triage safety contract missing: {phrase!r}")
    for phrase in (
        "2026-08-31",
        "2026-09-04",
        "USD 5,050.00",
        "suspicious",
        "content-repurpose/source-article.md",
        "meeting-notes/raw-notes.md",
        "decision-brief/decision-context.md",
        "file-organiser/preview-request.md",
        "not a claim that a model evaluation has run",
    ):
        if phrase not in expected:
            fail(f"expected-output documentation missing: {phrase!r}")
    for skill_name in ("content-repurpose", "expense-categorise", "inbox-triage", "invoice-chase", "file-organiser"):
        skill = (PLUGIN / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        if ".scale-systems-local/runs/" not in skill:
            fail(f"{skill_name} is missing the local run-directory contract")
        if "overwrite" not in skill.lower():
            fail(f"{skill_name} is missing an overwrite boundary")
    organiser_skill = (PLUGIN / "skills" / "file-organiser" / "SKILL.md").read_text(encoding="utf-8")
    if "synthetic manifest or preview-only fixture" not in organiser_skill:
        fail("file-organiser is missing its manifest-only safety boundary")


def main() -> int:
    checks = (
        validate_manifests,
        validate_skills,
        validate_counts_and_docs,
        validate_fixture_inventory,
        validate_sales_fixture,
        validate_invoice_fixture,
        validate_safety_contract,
    )
    try:
        for check in checks:
            check()
            print(f"PASS {check.__name__}")
    except (AssertionError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(f"PASS all {len(checks)} repository checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
