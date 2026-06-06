"""Pay item schema for Bid Spec Atlas."""

from __future__ import annotations

from dataclasses import dataclass


REQUIRED_PAY_ITEM_COLUMNS = (
    "pay_item_id",
    "source_file_id",
    "item_code",
    "description",
    "unit",
    "quantity",
    "unit_price",
    "total",
)


@dataclass(frozen=True)
class PayItemRow:
    pay_item_id: str
    source_file_id: str
    item_code: str
    description: str
    unit: str
    quantity: float
    unit_price: float
    total: float
    letting_date: str
    state: str
    project_id: str
    bidder: str

    @classmethod
    def from_parser_row(cls, row: dict[str, object]) -> "PayItemRow":
        source_file_id = str(row["source_file_id"])
        item_code = str(row["item_code"])
        return cls(
            pay_item_id=f"{source_file_id}:{item_code}",
            source_file_id=source_file_id,
            item_code=item_code,
            description=str(row["description"]),
            unit=str(row["unit"]),
            quantity=float(row["quantity"]),
            unit_price=float(row["unit_price"]),
            total=float(row["total"]),
            letting_date=str(row["letting_date"]),
            state=str(row["state"]),
            project_id=str(row["project_id"]),
            bidder=str(row["bidder"]),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        for field_name in REQUIRED_PAY_ITEM_COLUMNS:
            value = getattr(self, field_name)
            if value == "":
                errors.append(f"{field_name} is required")
        return errors


def pay_item_schema_sql() -> str:
    return """
CREATE TABLE IF NOT EXISTS pay_items (
  pay_item_id TEXT PRIMARY KEY,
  source_file_id TEXT NOT NULL,
  item_code TEXT NOT NULL,
  description TEXT NOT NULL,
  unit TEXT NOT NULL,
  quantity REAL NOT NULL,
  unit_price REAL NOT NULL,
  total REAL NOT NULL,
  letting_date TEXT NOT NULL,
  state TEXT NOT NULL,
  project_id TEXT NOT NULL,
  bidder TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (source_file_id) REFERENCES source_files (source_file_id)
);

CREATE INDEX IF NOT EXISTS idx_pay_items_item_code
  ON pay_items (item_code);

CREATE INDEX IF NOT EXISTS idx_pay_items_source_file_id
  ON pay_items (source_file_id);
""".strip()
