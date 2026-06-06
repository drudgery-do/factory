"""Fixture bid-tab parser for Bid Spec Atlas."""

from __future__ import annotations


def parse_bid_tab_text(text: str, source_file_id: str) -> list[dict[str, object]]:
    metadata: dict[str, str] = {}
    rows: list[dict[str, object]] = []
    in_table = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("ITEM CODE |"):
            in_table = True
            continue

        if not in_table:
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip()
            continue

        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 7:
            raise ValueError(f"unsupported bid-tab row: {line}")

        item_code, description, unit, quantity, bidder, unit_price, total = parts
        rows.append(
            {
                "source_file_id": source_file_id,
                "letting_date": metadata["letting"],
                "state": metadata["state"],
                "project_id": metadata["project"],
                "item_code": item_code,
                "description": description,
                "unit": unit,
                "quantity": float(quantity),
                "bidder": bidder,
                "unit_price": float(unit_price),
                "total": float(total),
            }
        )

    return rows
