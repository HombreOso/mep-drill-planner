# mep-drill-planner

Turn an MEP IFC model into a list of ceiling anchor / drill points that a construction robot (or a human installer) can execute.

**Mission fit**
1. Pre-construction design automation: rule-check spacing, edge distances, and clashes before anyone drills.
2. Construction-site robotics: feed the same points into a ROS 2 simulation (later), then into robots such as Hilti Jaibot or fischer BauBot.

## Status (v0)

- [x] Project scaffold
- [ ] Parse an MEP IFC and extract candidate hanging / anchor locations
- [ ] Export points as JSON (`x, y, z`, element id, type)
- [ ] Rule checks (spacing, edge distance, structure clash)
- [ ] HTML report
- [ ] ROS 2 / Gazebo simulation that visits the points

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Put an anonymised MEP IFC next to the command, then:
python -m src.extract_anchor_points path/to/model.ifc --out examples/out/points.json
```

Without an IFC yet, generate demo points:

```bash
python -m src.extract_anchor_points --demo --out examples/out/points.json
```

## Point JSON schema

```json
{
  "source": "model.ifc",
  "units": "m",
  "points": [
    {
      "id": "P-0001",
      "element_id": "3Abc...",
      "element_type": "IfcCableCarrierSegment",
      "x": 12.40,
      "y": 3.15,
      "z": 2.85,
      "reason": "hanger_from_bbox_top"
    }
  ]
}
```

## Roadmap

| Milestone | What |
|-----------|------|
| v0.1 | IFC → points JSON from hangers / trays / ducts (this week) |
| v0.2 | Spacing + edge-distance rule checks + HTML report |
| v0.3 | ROS 2 Jazzy sim: mobile base + arm visits points |
| later | Perception / PyImageSearch: verify as-built holes from site photos |

## Notes

- Never commit real project IFCs. Use anonymised / public sample models only.
- Built for Arthur Emig's portfolio path: computational MEP → BIM-to-robot.
