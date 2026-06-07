# Approval Card

Task: FPP-001
Stream: funeral-price-pages
Requested by: orchestrator
Risk classification: red
Decision owner: Human Owner or Delegate
Decision: Approve
Decision date: 2026-06-07

## Why Approval Was Needed

Matched rules: first_gpl
Required approver roles: human_owner, delegate

FPP-001 required the first 10 clean seed GPL PDF approvals before any seed
import folder, metadata schema tied to real PDFs, crawler work, or extraction
work proceeded.

## Approval Scope

Approved for FPP-001: use the 10 direct GPL PDF fixtures listed below as the
seed set for local import-folder and metadata-schema work.

This approval covers:

- local PDF fixture storage for the seed set
- GPL metadata indexing
- extraction fixture work
- staging-only verification

This approval does not cover:

- production deploy
- domain selection
- ad or affiliate applications
- broad scraping expansion
- browser challenge bypass
- manual HTML capture
- outreach to providers
- certification that listed prices are accurate or current

Every extracted fact must still cite the source file, include an extraction
timestamp, carry the verify-with-provider notice, and pass confidence gates
before publication.

## Approved PDF Seed Fixtures

| # | Provider name | City, state | Source URL | Local fixture path | SHA-256 | Decision |
|---|---|---|---|---|---|---|
| 1 | Bonney Watson | Seattle, WA | https://bonneywatson.com/wp-content/uploads/2025/06/GPL-June-2025.pdf | fixtures/funeral-price-pages/seed-gpls/bonney_watson_2025_gpl.pdf | c511a3ef6717f1267eed61aa1ff6563512dae57314f4d9b3a5ecf4a071d80607 | approved |
| 2 | Cremation Society of Connecticut | Windsor, CT | https://cremationct.com/resources/generalpricelist/General_Price_List.pdf | fixtures/funeral-price-pages/seed-gpls/cremation_society_connecticut_gpl.pdf | 9ee8acc47fddd2b8021ee6f3c1a3d51ee2bd742cfc96f9401f34de3a4ddcbfc2 | approved |
| 3 | Forest Lawn | Los Angeles / Orange County, CA | https://forest-lawn.s3-us-west-1.amazonaws.com/wp-content/uploads/2025/03/FL-250111-01-LA-OC-GPL-English-v10-0304.pdf | fixtures/funeral-price-pages/seed-gpls/forest_lawn_2025_gpl.pdf | 870fb18294c1caad3ae9a24db8aef2352db98dd8a126fedb55d6efac30b20467 | approved |
| 4 | Goff Mortuary | Midvale / Draper / Sandy / Nephi, UT | https://irp.cdn-website.com/13d11569/files/uploaded/Goff_Mortuary_Price_List.pdf | fixtures/funeral-price-pages/seed-gpls/goff_mortuary_price_list.pdf | 964fe703a9e7855d6be14d89a2fa3ce9dae3f972ca91033558619fa09ce08856 | approved |
| 5 | Joldersma & Klein Funeral Home | Kalamazoo, MI | https://joldersma-klein.com/wp-content/uploads/2023/04/JK-GPL-04.01.23-Letter-Orientation.pdf | fixtures/funeral-price-pages/seed-gpls/joldersma_klein_2023_gpl.pdf | 200067adc221184465bc3fb716a1a5524bd854a41e8193d660b901a6e4e8f6d7 | approved |
| 6 | Kern Funeral Home | Mount Vernon, WA | https://fh-content.s3.amazonaws.com/release/Content/Media/KernFuneralHome/Kern%20GPL%20Dec%201%2C%202025.pdf | fixtures/funeral-price-pages/seed-gpls/kern_funeral_home_2025_gpl.pdf | d5f89c9cd6da41f3f405c609fe6d5961860d9224eeb7ec37eb17a89f010f31ae | approved |
| 7 | Kreamer Funeral Home & Crematory | Annville / Jonestown, PA | https://cdn.f1connect.net/cdn/11390D-6C0/gpl/Kreamer%20Funeral%20Home%20and%20Crematory%20Inc%20GPL.pdf | fixtures/funeral-price-pages/seed-gpls/kreamer_2025_gpl.pdf | 8f8a75aeb7cbbdf4f4c5183ac152e96886bc410040c6048138d6a3dd37e30578 | approved |
| 8 | Legends Tri-County Funeral Services | Seguin, TX | https://s3.amazonaws.com/CFSV2/fileuploads/13269/GPLFall2025PDF.pdf | fixtures/funeral-price-pages/seed-gpls/legends_tri_county_2025_gpl.pdf | f94901e39b337753cfcb65832469f274ef5cc67490a90ae2998d80a5c389440b | approved |
| 9 | Sharp Funeral Homes | Flint / Grand Blanc / Fenton / Swartz Creek, MI | https://irp.cdn-website.com/ae6c5997/files/uploaded/FINAL%202_29%20Sharp_GPL_20p_E.pdf | fixtures/funeral-price-pages/seed-gpls/sharp_funeral_homes_gpl.pdf | d1b9c360daa0ed6ce11a804312416c4cc9671e80b0c56905f05db07b6d5e5c87 | approved |
| 10 | Sinai Memorial | San Francisco, CA | https://sinaimemorial.org/wp-content/uploads/2026/04/2026-GPL-General-Price-List-Sinai.pdf | fixtures/funeral-price-pages/seed-gpls/sinai_memorial_2026_gpl.pdf | 4c310e562efc321c3ccd53813f7497a726e7e2caec2128969501cf2920c36058 | approved |

## Evidence Pack

- Manifest: `fixtures/funeral-price-pages/seed-gpls/manifest.json`
- Metadata schema: `streams/funeral_price_pages/seed_import.py`
- Tests: `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- Quality gate output: `python3 orchestrator/scripts/run_quality_gate.py`
- Rollback plan: revert the seed fixture PR and mark `FPP-001` blocked again.

## Explicit Non-Actions

- No production secrets added.
- No production deploy executed.
- No payment, ad, affiliate, KYC, or domain action executed.
- No broad scraper expansion approved.
