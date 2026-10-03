#!/usr/bin/env python3
"""Validate the supplied taxonomy and export angles; standard library only."""

import argparse
from collections import Counter
from itertools import groupby
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    "FRESH & LIFTED": 13,
    "AMBER, SPICE & SWEET": 12,
    "FLORAL & FRUITY": 11,
    "EARTHY, WOODY & DEEP": 12,
}
TEXT_FIELDS = (
    "realm", "family", "note", "descriptors",
    "texture_tactile", "reference_material",
)


def validate(document):
    if document.get("schema_version") != 1:
        raise ValueError("Expected taxonomy schema_version 1")
    rows = document.get("notes")
    if not isinstance(rows, list) or len(rows) != 48:
        raise ValueError("Expected exactly 48 notes")
    seen = set()
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"Row {index} must be an object")
        for field in TEXT_FIELDS:
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Row {index}: missing or empty {field}")
            if value != " ".join(value.split()):
                raise ValueError(f"Row {index}: normalize whitespace in {field}")
        if type(row.get("value")) is not int or row["value"] != 1:
            raise ValueError(f"Row {index}: expected integer weight 1")
        path = tuple(row[field] for field in ("realm", "family", "note"))
        if path in seen:
            raise ValueError(f"Duplicate note path: {path}")
        seen.add(path)
    if Counter(row["realm"] for row in rows) != EXPECTED_COUNTS:
        raise ValueError("Realm counts differ from the supplied taxonomy")
    for fields in (("realm",), ("realm", "family")):
        keys = [tuple(row[field] for field in fields) for row in rows]
        runs = [key for key, _ in groupby(keys)]
        if len(runs) != len(set(runs)):
            raise ValueError(f"Non-contiguous groups for {fields}")
    return rows


def grouped_arcs(notes, fields):
    arcs = []
    for key, group in groupby(
        notes, key=lambda row: tuple(row[field] for field in fields)
    ):
        members = list(group)
        arcs.append({
            **dict(zip(fields, key)),
            "note_count": len(members),
            "start_degrees": members[0]["start_degrees"],
            "end_degrees": members[-1]["end_degrees"],
        })
    return arcs


def build(rows):
    width = 360 / sum(row["value"] for row in rows)
    notes = [
        {
            "index": index + 1,
            **row,
            "start_degrees": index * width,
            "end_degrees": (index + 1) * width,
        }
        for index, row in enumerate(rows)
    ]
    return {
        "schema_version": 1,
        "source": "data/taxonomy.json",
        "angle_origin": "12 o'clock",
        "angle_direction": "clockwise",
        "order": "source table order",
        "rings_inside_to_outside": list(TEXT_FIELDS),
        "degrees_per_note": width,
        "physical_diameter_mm": None,
        "ring_radii": None,
        "tile_dimensions": None,
        "tile_overlap": None,
        "realms": grouped_arcs(notes, ("realm",)),
        "families": grouped_arcs(notes, ("realm", "family")),
        "notes": notes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "build" / "layout.json",
        help="Output JSON path (default: this experiment's build/layout.json)",
    )
    args = parser.parse_args()
    try:
        document = json.loads((ROOT / "data" / "taxonomy.json").read_text())
        rows = validate(document)
        layout = build(rows)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(layout, indent=2) + "\n")
    except (OSError, ValueError, TypeError, AttributeError) as error:
        parser.exit(1, f"Layout failed: {error}\n")
    print(
        f"Validated {len(rows)} notes, {len(layout['realms'])} realms, "
        f"{len(layout['families'])} realm-scoped families; "
        f"{layout['degrees_per_note']} degrees per note; 360 degrees total."
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
