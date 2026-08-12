import csv
from pathlib import Path

p = Path(__file__).with_name("COMMUNITIES-SOURCE-INVENTORY.csv")
context_ids = {
    "M-0500", "M-0504", "M-0505", "M-0507", "M-0521", "M-0522",
    "M-0526", "M-0545", "M-0546", "M-0548", "M-0549", "M-0552",
    "M-0562", "M-0563", "M-0564", "M-0567", "M-0580", "M-0589",
}
with p.open(newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))
fields = list(rows[0])
seen = set()
for r in rows:
    if r["record_id"] in context_ids:
        r["research_status"] = "contextual close read; no distinct finding"
        seen.add(r["record_id"])
assert seen == context_ids, context_ids - seen
with p.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

ledger = Path(__file__).with_name("COMMUNITIES-EVIDENCE-LEDGER.csv")
text = ledger.read_text(encoding="utf-8-sig")
old = "97 PDFs; 28 relevant or contextual close reads"
assert old in text
ledger.write_text(text.replace(old, "97 PDFs; 25 relevant or contextual close reads", 1), encoding="utf-8")
print(f"context_reads={len(context_ids)}")
