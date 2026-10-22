#!/usr/bin/env python3
"""Validate the dataset without external dependencies.

Checks required fields, enum values, unique IDs, and that every entry carries
at least one evidence link and that all URLs are http(s).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "founders.json"

REQUIRED = [
    "id", "person", "birth_place", "birth_country", "birth_year",
    "arrival_year", "company", "company_founded_year", "sector",
    "company_status", "confidence", "evidence", "news", "notes",
]
STATUS = {"listed", "private", "sold", "defunct"}
CONFIDENCE = {"high", "medium"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    entries = doc["entries"]

    if doc["meta"]["count"] != len(entries):
        fail(f"meta.count is {doc['meta']['count']} but there are {len(entries)} entries")

    seen = set()
    for i, e in enumerate(entries):
        where = f"entry[{i}] ({e.get('id', 'no id')})"
        for key in REQUIRED:
            if key not in e:
                fail(f"{where} missing required key: {key}")
        if not ID_RE.match(e["id"]):
            fail(f"{where} id is not kebab-case")
        if e["id"] in seen:
            fail(f"{where} duplicate id")
        seen.add(e["id"])
        if e["company_status"] not in STATUS:
            fail(f"{where} bad company_status: {e['company_status']}")
        if e["confidence"] not in CONFIDENCE:
            fail(f"{where} bad confidence: {e['confidence']}")
        if not e["evidence"]:
            fail(f"{where} has no evidence")
        for ev in e["evidence"]:
            for key in ("claim", "source", "url"):
                if not ev.get(key):
                    fail(f"{where} evidence missing {key}")
            if not ev["url"].startswith(("http://", "https://")):
                fail(f"{where} evidence url is not http(s): {ev['url']}")
        for n in e["news"]:
            for key in ("outlet", "title", "url"):
                if not n.get(key):
                    fail(f"{where} news item missing {key}")
            if not n["url"].startswith(("http://", "https://")):
                fail(f"{where} news url is not http(s): {n['url']}")
        if e["birth_year"] is not None and e["arrival_year"] is not None:
            if e["arrival_year"] < e["birth_year"]:
                fail(f"{where} arrival year precedes birth year")

    print(f"OK: {len(entries)} entries, {sum(len(e['news']) for e in entries)} news links")


if __name__ == "__main__":
    main()
