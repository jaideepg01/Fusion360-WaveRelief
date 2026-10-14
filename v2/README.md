> Release review, 14 October 2026: the original guide below predates the saved successful desktop run. See [verification](../docs/VERIFICATION.md) for the current evidence and limitations. Historical installation references refer to the original package; use [current installation instructions](../docs/INSTALLATION.md).

# Wave Relief V2 — concave channels and narrow crests

V2 changes the section geometry, rather than just increasing resolution. V1 used a cosine section with broad rounded peaks. V2 uses a rounded half-sine channel profile: steeper shoulders meet at a narrow rounded crest, while the trough remains smooth. The panel remains a closed solid with a flat back.

Default: **200 × 380 mm, 11 mm stock, 4 mm nominal carving depth**, designed within the user-specified 400 × 400 mm Snapmaker Artisan limit. Leave space for your actual clamps and tool/holder clearance. Default ridge sharpness is 12.

## Install and run

1. Extract the ZIP into its own permanent folder.
2. In Fusion **Scripts and Add-Ins → Scripts → +**, register the folder **WaveRelief_v2** containing `WaveRelief_v2.py` and its manifest.
3. Select **WaveRelief_v2** and run it. The progress window identifies **WaveRelief V2.0.0** and reports the current section and point.
4. After the solid finishes, save it as **F3D**.
5. Use **Modify → Change Parameters** for dimension and styling changes.

This is a NEW script entry. Your V1 installation and saved designs remain available.

## Parameters

| Parameter | Default | Effect |
|---|---:|---|
| PanelWidth | 200 mm | Panel X dimension |
| PanelHeight | 380 mm | Panel Y dimension |
| PanelThickness | 11 mm | Stock thickness |
| CarveDepth | 4 mm | Nominal deepest cut below stock top |
| CrestAllowance | 0.20 mm | Small stock skim at the crests to accommodate spline overshoot |
| RidgeSharpness | 12 | Larger values make narrower crests; start within 4–16 |
| WaveCount | 3 | Wave density; nominal cycles toward the top before bending |
| WaveBend | 0.65 | Upper flowing-wave deformation; zero gives concentric ovals |
| CenterX | 0.43 | Centre fraction of panel width |
| CenterY | 0.39 | Centre fraction of height, measured from the bottom |
| OvalRadiusX | 0.48 | Horizontal contour scale |
| OvalRadiusY | 0.21 | Vertical contour scale |
| WavePhase | 0 deg | Shifts ridges and valleys; 180 deg creates a central hollow |

`RidgeSharpness` is unitless. It controls a small rounded cap, not a guaranteed physical fillet radius. Its physical width also depends on wave spacing. V2 deliberately avoids a mathematical knife edge; it does not create hard seams between separate channel faces.

Try RidgeSharpness 6 for softer crests, 12 for the default narrow crest, and 16 for a sharper cap. These settings are exploratory; only the default exported solid is kernel-validated. Keep 0 < CrestAllowance < CarveDepth < PanelThickness. Keep CenterY between 0 and 1 and oval scales positive. The panel edges crop the contours, so WaveCount does not guarantee that many fully visible rings.

## Changing styles and rebuilding

All listed controls are native Fusion user parameters driving the spline fit points and section planes. Small changes update the existing model.

Each section includes extra samples at and beside the crests. These horizontal anchor locations are determined at creation. After large changes to centre position, phase, wave count, oval proportions or very high ridge sharpness, rerun **WaveRelief_v2 with your edited V2 design active**. It reads that design's built-in V2 parameters and creates a NEW document with refreshed crest anchors. Save the new design separately. This rebuild does not overwrite the existing design. Expressions referring to added custom user parameters are not supported by the rebuild.

61 uniformly spaced sections are used, with a base 41-point grid plus adaptive crest samples. Generation involves several thousand driving dimensions and can take time. Progress, cancellation between API operations, and a `wave_relief_build.log` beside the script are included. A single Fusion solver or loft call can pause the UI until that call returns.

## Files

- `WaveRelief_v2/`: native Fusion generator, parameter-driven geometry, manifest and profile helper.
- `WaveRelief_V2_200x380.step`: independently generated smooth B-rep solid for immediate import. No editable native parameter history.
- `WaveRelief_V2_200x380.stl`: mesh companion in millimetres.
- `WaveRelief_V2_preview.png`: section comparison and design preview.
- `validation.json`: actual exported solid bounds, top-height checks, approximation error and STL topology check. The default exported loft differs from the target analytic field by up to approximately 0.68 mm at checked surface samples, principally near the upper end. Inspect the actual STEP/native body before generating toolpaths.

The Fusion generator and portable exporter use the same analytic profile and adaptive anchors, but different spline/loft kernels. Small differences are possible. Sharp caps are approximated by fitted splines; sampling and loft interpolation can round them or overshoot between samples. The validation file records the default export's measured approximation error. This is a reference-inspired design, not an exact reconstruction of the photograph.

## CNC use

The default troughs leave approximately 7 mm of material beneath the front relief. The crests are nominally skimmed by 0.20 mm. Measure the actual MDF thickness and set the stock and Z reference accordingly.

Create and simulate toolpaths in Fusion Manufacture for your installed tool, actual fixtures and stock. This package contains no machine-specific feeds, toolpaths or G-code. Tool access to the narrow ridge shoulders must be checked in simulation; geometry changes alone do not guarantee the machined finish.

## Verification

The Python files compile. The default STEP is checked for validity, single-solid topology, dimensional bounds and sampled top heights. The STL is checked for closed edges. V2 has not been executed inside desktop Fusion here. It reuses the API calls that reached section creation in the user's V1 run, retaining the root-name and display-property fixes, while adding the new profile and adaptive samples.
