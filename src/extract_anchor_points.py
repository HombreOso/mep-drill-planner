"""Extract candidate ceiling anchor / drill points from an MEP IFC model.

v0 strategy (simple, transparent):
- Find common MEP hanging elements (cable trays, ducts, pipes, hangers if present).
- Use each element's world-space bounding-box top centre as a candidate point.
- Later versions will use explicit hanger geometry and structural clash checks.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Element classes that typically need ceiling hangers / anchors in MEP work.
DEFAULT_TYPES = (
    "IfcCableCarrierSegment",
    "IfcCableCarrierFitting",
    "IfcDuctSegment",
    "IfcDuctFitting",
    "IfcPipeSegment",
    "IfcPipeFitting",
    "IfcFlowSegment",
    "IfcFlowFitting",
    "IfcBuildingElementProxy",  # often used for hangers in messy models
)


def demo_points() -> dict:
    """Synthetic points so the pipeline runs before you have an IFC."""
    return {
        "source": "demo",
        "units": "m",
        "points": [
            {
                "id": "P-0001",
                "element_id": "DEMO-TRAY-1",
                "element_type": "IfcCableCarrierSegment",
                "x": 2.0,
                "y": 1.0,
                "z": 2.85,
                "reason": "demo_hanger",
            },
            {
                "id": "P-0002",
                "element_id": "DEMO-DUCT-1",
                "element_type": "IfcDuctSegment",
                "x": 4.5,
                "y": 3.2,
                "z": 2.90,
                "reason": "demo_hanger",
            },
            {
                "id": "P-0003",
                "element_id": "DEMO-PIPE-1",
                "element_type": "IfcPipeSegment",
                "x": 6.0,
                "y": 0.8,
                "z": 2.70,
                "reason": "demo_hanger",
            },
        ],
    }


def extract_from_ifc(ifc_path: Path, types: tuple[str, ...] = DEFAULT_TYPES) -> dict:
    try:
        import ifcopenshell
        import ifcopenshell.geom
    except ImportError as e:
        raise SystemExit(
            "ifcopenshell is not installed. Run: pip install -r requirements.txt"
        ) from e

    model = ifcopenshell.open(str(ifc_path))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    points = []
    n = 0
    for type_name in types:
        for el in model.by_type(type_name):
            try:
                shape = ifcopenshell.geom.create_shape(settings, el)
            except Exception:
                continue
            verts = shape.geometry.verts  # flat list x,y,z,x,y,z,...
            if len(verts) < 3:
                continue
            xs = verts[0::3]
            ys = verts[1::3]
            zs = verts[2::3]
            n += 1
            points.append(
                {
                    "id": f"P-{n:04d}",
                    "element_id": el.GlobalId,
                    "element_type": el.is_a(),
                    "x": round((min(xs) + max(xs)) / 2.0, 4),
                    "y": round((min(ys) + max(ys)) / 2.0, 4),
                    "z": round(max(zs), 4),  # top of bbox ≈ ceiling side
                    "reason": "bbox_top_centre",
                }
            )

    return {
        "source": ifc_path.name,
        "units": "m",
        "points": points,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ifc", nargs="?", type=Path, help="Path to an MEP IFC file")
    parser.add_argument(
        "--demo", action="store_true", help="Write synthetic demo points (no IFC needed)"
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("examples/out/points.json"),
        help="Output JSON path",
    )
    args = parser.parse_args(argv)

    if args.demo:
        result = demo_points()
    elif args.ifc:
        if not args.ifc.exists():
            print(f"File not found: {args.ifc}", file=sys.stderr)
            return 1
        result = extract_from_ifc(args.ifc)
    else:
        parser.error("Provide an IFC path, or pass --demo")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {len(result['points'])} points → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
