"""Utility helpers for populating dealership demo data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class DealershipRecord:
    """Simple dealership payload used by local population scripts."""

    id: int
    name: str
    city: str
    state: str


def build_seed_records() -> List[DealershipRecord]:
    """Return a small deterministic set of records for local development."""

    return [
        DealershipRecord(id=1, name="Prime Autos", city="New York", state="NY"),
        DealershipRecord(id=2, name="Sunset Motors", city="Los Angeles", state="CA"),
        DealershipRecord(id=3, name="Lakeview Cars", city="Chicago", state="IL"),
    ]


def to_dicts(records: Iterable[DealershipRecord]) -> List[dict]:
    """Convert `DealershipRecord` items into serializable dictionaries."""

    return [
        {
            "id": record.id,
            "name": record.name,
            "city": record.city,
            "state": record.state,
        }
        for record in records
    ]
