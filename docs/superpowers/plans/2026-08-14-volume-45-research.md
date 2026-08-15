# Volume 45 source-audit execution plan

Date: 2026-08-14 (Africa/Dakar)
Mode: P0 research only; no article prose
Intended branch: `agent/volume-45-research`
Intended base: `agent/volume-44-research`

## Boundary

Process the final journal unit in the current source inventory: *Communal Societies* volume 45, issue 1, fifteen PDFs (M-0116 through M-0130). Preserve the eight standalone sources as a separate evidence stream.

The source container is the Google Drive object named `vol41-45.zip`. Its 55,770,584-byte payload must match saved D-003 SHA-256 `e2fa3989d489ace25ce12c29aa6d523ec3e9918282f032bcb4caa5a40fcdcc5c`. Verify the ZIP, its internal `SHA256SUMS.txt`, each pre-existing inventory hash, PDF page count, and nonempty text extraction.

## Procedure

1. Restore the fifteen members by saved hash identity; do not rely on browser filenames.
2. Run the locked six-family discovery score and five-family process screen across all texts.
3. Inspect every child-danger proximity candidate separately from the general ranking.
4. Close-read all eleven substantive records and disposition all four functional metadata records.
5. Promote only materially distinct findings; keep source fact, author interpretation, alternative interpretation, process, outcome, transferability, and verification needs separate.
6. Reconcile findings into the existing eighteen-item gap bank without creating duplicate categories.
7. Update the cumulative handoff, inventory, README, report, and verification workflow.
8. Keep PDFs, ZIPs, full extracted text, private Drive IDs, and raw context dumps outside Git.

## Expected checkpoint

- Journal boundary: volumes 1-45 complete, 984 PDFs total
- Close reads: 443
- Additional title/keyword triages: 207
- Metadata triages: 334
- Findings: F-001 through F-162
- Volume 45 additions: F-159 through F-162
- Gap bank: 18 items, unchanged at 8 B, 7 C, 3 D
- Remaining journal PDFs: zero
- Next evidence stream: eight standalone sources

## Validation

```bash
python recovered/test_v45_workflow.py
python recovered/verify_v45.py --archive /path/to/vol41-45.zip
python -m compileall recovered
git diff --check
```

Do not publish the branch or open the draft pull request until the owner explicitly authorizes publication.
