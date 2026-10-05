# mep-drill-planner

Turn an MEP IFC model into a list of ceiling anchor / drill points that a construction robot (or a human installer) can execute.

**Mission fit**
1. Pre-construction design automation: rule-check spacing, edge distances, and clashes before anyone drills.
2. Construction-site robotics: feed the same points into a ROS 2 simulation (later), then into robots such as Hilti Jaibot or fischer BauBot.

## Progress

| Step | Status | What's done |
|------|--------|-------------|
| **0. Scaffold** | Done | Repo layout, `requirements.txt` (ifcopenshell), venv, `.gitignore`, public GitHub at [HombreOso/mep-drill-planner](https://github.com/HombreOso/mep-drill-planner) |
| **1. Demo extractor** | Done | `--demo` writes 3 synthetic points to JSON (`id`, `x/y/z`, type, reason) |
| **2. IFC → points** | Done (v0.1) | `extract_anchor_points` loads IFC, skips entity types missing from the file's schema (IFC2X3-safe), takes top-of-bbox as hanger candidates from FlowSegment / FlowFitting / BuildingElementProxy (and IFC4 duct/pipe/cable types when present) |
| **3. Public sample IFCs** | Done | Three CC BY 4.0 models under `examples/` (Zenodo ventilation + piping, buildingSMART Duplex MEP); sources attributed below |
| **4. Sample runs** | Done | Ventilation **320** pts · Piping **439** pts · Duplex MEP **785** pts → `examples/out/*-points.json` (local only; gitignored) |
| **5. Rule checks** | Not started | Spacing, edge distance, structure clash |
| **6. HTML report** | Not started | Human-readable map / table of points + rule failures |
| **7. ROS 2 sim** | Not started | Mobile base + arm visits points (e.g. Gazebo / Jazzy) |
| **8. Perception** | Later | PyImageSearch / CV: verify as-built holes from site photos |

**Current focus:** tighten candidates (ceiling-level / hanger-like only), then rules + HTML report.

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

| Milestone | Status | What |
|-----------|--------|------|
| **v0.1** | Done | IFC → points JSON on public MEP samples (schema-safe extractor) |
| **v0.2** | Next | Ceiling/hanger filtering · spacing + edge-distance rules · HTML report |
| **v0.3** | Planned | ROS 2 Jazzy sim: mobile base + arm visits points |
| **later** | Planned | Perception / PyImageSearch: verify as-built holes from site photos |

## Sample IFC sources

Public MEP sample models used under `examples/` (CC BY 4.0):

- **Zenodo DuplexModel+MEP** (Teclaw, 2024), DOI [10.5281/zenodo.10610773](https://doi.org/10.5281/zenodo.10610773) — `zenodo-duplex-ventilation.ifc` (Ventilation.ifc) and `zenodo-duplex-piping.ifc` (Piping.ifc).
- **buildingSMART Duplex Apartment** `Duplex_MEP_20110907.ifc` — cite as BSI (2020) Duplex Apartment Test Files; saved as `buildingsmart-duplex-mep.ifc` (from [buildingsmart-community/Community-Sample-Test-Files](https://github.com/buildingsmart-community/Community-Sample-Test-Files)).

```bash
python -m src.extract_anchor_points examples/zenodo-duplex-ventilation.ifc --out examples/out/zenodo-duplex-ventilation-points.json
python -m src.extract_anchor_points examples/zenodo-duplex-piping.ifc --out examples/out/zenodo-duplex-piping-points.json
python -m src.extract_anchor_points examples/buildingsmart-duplex-mep.ifc --out examples/out/buildingsmart-duplex-mep-points.json
```

## Notes

- Never commit real project IFCs. Use anonymised / public sample models only.
- Built for Arthur Emig's portfolio path: computational MEP → BIM-to-robot.
