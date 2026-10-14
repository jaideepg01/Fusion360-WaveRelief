> Release review, 14 October 2026: the original guide below predates the saved successful desktop run. See [verification](../docs/VERIFICATION.md) for the current evidence and limitations. Historical installation references refer to the original package; use [current installation instructions](../docs/INSTALLATION.md).

# Wave Relief — Fusion parametric CNC panel

Reference-inspired approximation of the carved wooden panel supplied by JD. Not an exact reconstruction or scan. The current shape uses a smooth elliptical wave field that bends toward the top of the panel. Flat rear surface; no intended undercuts.

## Files

- `WaveRelief_v103/` — Fusion script, manifest and shared profile definition. This creates the editable native parametric design.
- `WaveRelief_200x380.step` — ready-to-import solid, with fixed geometry and no native parameter history.
- `WaveRelief_200x380.stl` — millimetre mesh companion; not the preferred file for editing.
- `WaveRelief_preview.png` — mathematical profile preview, not a Fusion screenshot.
- `validation.json` — exported solid validation results.

## Create the editable model in Fusion

1. Extract this ZIP to a permanent folder on your desktop computer.
2. In Fusion open **Utilities > Scripts and Add-Ins** (or find **Scripts and Add-Ins** through command search).
3. On the Scripts tab use **Add / +** and select the extracted `WaveRelief_v103` folder containing `WaveRelief_v103.py` and its manifest.
4. Select **WaveRelief_v103** and run it. It creates a new document; building the many constrained sections can take several minutes.
5. Save the new document as an F3D design.
6. Open **Modify > Change Parameters**. Filter to User Parameters, then edit the controls below. Dimensions and styling update through the native sketch/loft timeline.

## Controls

| Parameter | Default | What changes |
|---|---:|---|
| PanelWidth | 200 mm | Overall X size |
| PanelHeight | 380 mm | Overall Y size |
| PanelThickness | 11 mm | Stock thickness above the flat back |
| CarveDepth | 4 mm | Nominal crest-to-valley relief depth |
| CrestAllowance | 0.15 mm | Small skim allowance at the crests to keep default spline interpolation within stock |
| WaveCount | 3 | Density; nominal number of radial cycles from centre to top before wave bending |
| WaveBend | 0.65 | Upper wave curvature; 0 produces concentric oval contours |
| CenterX | 0.43 | Centre location as a fraction of width; 0.5 is centred |
| CenterY | 0.39 | Centre location as a fraction of height measured from the bottom |
| OvalRadiusX | 0.48 | Horizontal contour scale relative to width |
| OvalRadiusY | 0.21 | Vertical contour scale relative to height |
| WavePhase | 0 deg | Shifts ridges/valleys; 0 gives a central crest, 180 deg a central depression |

Fractional settings are unitless. The centre element is part of the continuous wave field; its apparent size changes with oval scale, wave count and phase. It is not an independently bounded medallion. Panel edges crop the contours, so WaveCount does not guarantee exactly that many complete visible rings.

Suggested starting bounds: WaveCount 1.5–4; WaveBend 0–1; CenterX 0.15–0.85; CenterY 0.15–0.80; positive oval radii. Keep 0 < CrestAllowance < CarveDepth < PanelThickness, with enough remaining wood for your chosen stock and mounting. Do not set CenterY to 1: the normalization divides by 1-CenterY.

## Quick styles to try

| Style | WaveCount | WaveBend | CenterX | CenterY | OvalRadiusX | OvalRadiusY | Phase |
|---|---:|---:|---:|---:|---:|---:|---:|
| Flowing reference direction | 3 | 0.65 | 0.43 | 0.39 | 0.48 | 0.21 | 0 deg |
| Calm concentric ovals | 2 | 0 | 0.5 | 0.5 | 0.48 | 0.21 | 0 deg |
| Offset flowing waves | 3.5 | 0.85 | 0.30 | 0.32 | 0.55 | 0.20 | 0 deg |
| Central hollow | 2.5 | 0.35 | 0.5 | 0.42 | 0.48 | 0.21 | 180 deg |

These are exploratory settings, not separately kernel-validated exports.

## Geometry and practical limits

49 cross sections, each with 41 spline fit points, approximate the continuous field. Every fit point is positioned through live parameter expressions; planes are driven by PanelHeight. A 0.15 mm crest allowance keeps the default sampled surface inside the nominal stock top. The exported panel is therefore slightly thinner at its highest point than PanelThickness, which describes the stock. Width and height are the specified panel dimensions. The stored STEP is independently generated with the same sampled field using a different CAD kernel; small surface differences from Fusion are possible.

Large styling changes or high wave counts can exceed this sampling resolution and cause ripples or failed lofts. For denser patterns, edit SECTIONS and POINTS in `WaveRelief_v103/shape.py` before running the script again; this creates a new design. These two resolution controls require regeneration, unlike the native styling parameters.

## Snapmaker Artisan / 11 mm MDF

Default panel: **200 × 380 mm**, designed within the user-specified 400 × 400 mm working limit. At this placement the bed has 200 mm total spare width and 20 mm total spare length; confirm the actual clamp and cutter/holder clearance in the setup. Parameter edits must retain room for your chosen fixtures: the full 400 × 400 mm area is not automatically available when clamps occupy it.

The stock is 11 mm MDF. CarveDepth defaults to 4 mm, leaving nominally 7 mm beneath the valleys. Crests are skimmed by 0.15 mm. No rear machining is included. Measure the actual board thickness before setting PanelThickness and Z. Feed rates, stepdowns and cutter choice are not set because the installed cutter and MDF specifications are unknown.

## CNC preparation

Import STEP for immediate solid geometry, or use the saved native design for parametric editing. In Manufacture, create a setup with the panel flat, Z pointing up and the stock top as the machining reference. Use an appropriate roughing operation followed by a ball-nose finishing strategy suitable for the relief. Set tools, feeds, stepdowns, stepover and workholding for your specific machine, wood and cutter; this package does not include toolpaths or machine-specific G-code.

Simulate the actual tool and holder against the stock and fixtures after changing the shape. Narrower/deeper waves may need a smaller ball-nose tool or reduced depth. The default panel leaves approximately 7 mm of material under the nominal deepest trough, before any additional rear operations. Verify the final model and setup, since fitted splines can deviate slightly between samples.

## Validation status

The STEP solid was generated and checked for CAD-kernel validity, single-solid topology, envelope dimensions and tessellated top-surface heights. The Python files compile successfully. The native Fusion script was checked against Autodesk API documentation but has not been executed inside Fusion in this environment. The first desktop run is therefore required to verify sketch solving and loft behavior.

Authoring basis: Autodesk Fusion API documentation for SketchFittedSplines.add, SketchDimensions.addDistanceDimension, LoftFeature and Parameter.expression; Autodesk Parameters reference for sqrt, sin and cos expressions.

## Version 1.0.1 — Fusion startup fix

Removed the root-component name assignment, which Fusion rejects. The carved body is still named CNC Wave Panel. To update an existing installation, replace WaveRelief.py in the registered WaveRelief folder with the file in this package, then run it again. The startup fix is syntax-checked; full native Fusion execution remains to be verified on desktop.

## Version 1.0.2 — visibility fix

Replaced assignments to sketch/plane isVisible with the documented writable isLightBulbOn property. In particular, ConstructionPlane.isVisible is read-only. The user desktop run reached the end of the first closed section before encountering this display error; complete loft execution remains to be verified.

## Version 1.0.3 — visible progress and diagnostics

Register the NEW `WaveRelief_v103` folder rather than selecting an older WaveRelief entry. The progress window should say **WaveRelief v1.0.3** immediately when run. It reports section creation, point constraints, sketch solving and loft creation. Cancellation is checked between these operations; Fusion's internal solver/loft operation cannot be interrupted by this script while an API call is running.

A `wave_relief_build.log` file is written beside the script if that folder is writable. It records the actual loaded script path, current stage, completed sections, cancellation and failures. If the progress bar stops, the last log entries identify the operation. No log is bundled; it is created on your computer.

The geometric sampling stays at 49 sections × 41 points. There are approximately 3,969 spline point dimensions, so generation can be slow. Version 1.0.3 adds feedback without reducing surface sampling. The shared shape definition is loaded from the script's own folder to avoid picking up a cached module from an older installation.

The Python file compiles and the progress API follows Autodesk's Progress Dialog sample. Full desktop execution remains unverified in this environment. The STEP/STL companions remain the previously validated fixed geometry.
