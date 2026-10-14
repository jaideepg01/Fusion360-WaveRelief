# Installation and first run

Install Autodesk Fusion with access to its scripting environment. The scripts use Fusion’s bundled `adsk` APIs and Python standard library; do not run the entry-point files with ordinary system Python. Both manifests declare Windows and macOS, but an exact tested Fusion build and cross-platform matrix have not been recorded.

1. Extract the repository or version ZIP to a permanent, writable folder. Keep each `.py` entry point beside its identically named `.manifest` and `shape.py`.
2. In Fusion open **Utilities → Scripts and Add-Ins**, or find the command through command search.
3. Select **Scripts**, choose **+**, and register `v1/WaveRelief_v103` or `v2/WaveRelief_v2`. Do not register the repository root. Version ZIPs have the script folder directly at their root.
4. Select the script and run it. Both versions can coexist. These are manually launched scripts; there is no persistent toolbar command or startup service.
5. Wait for the completion message. Save the new design as F3D and edit **Modify → Change Parameters**.

V1 always starts a new default design. V2 can rebuild from built-in parameters of an active V2 design into a new document; for a fresh default V2 run, start with a blank design. Keep `0 < CrestAllowance < CarveDepth < PanelThickness`, positive dimensions and oval scales, and `0 < CenterY < 1`. V2 RidgeSharpness should initially stay within 4–16.

## Update or remove

Extract updates into a separate folder, unlink the old script entry and register the new one. Keep saved F3D designs and any edited source separately. To remove, unlink the script in Scripts and Add-Ins, then remove its extracted folder when no longer needed. Saved designs are separate documents.

## Troubleshooting

- Wrong progress-window version: register the correct version folder and select its named entry.
- Slow generation: thousands of driving dimensions are created. Cancellation is checked between operations; an internal solver or loft call can pause the interface until it returns.
- Failure or cancellation: the new document may contain partial sketches. Inspect it before closing. Read `wave_relief_build.log` beside the script; this file is replaced on each run.
- Read-only folder: move the package to a writable location to enable logging.
- Large styling edits: rerun V2 with the edited V2 design active to refresh anchors. Custom-parameter expressions are not supported. V1 resolution changes require source configuration and regeneration.
- Immediate fixed geometry: open the supplied STEP. STL is the mesh alternative in millimetres; neither carries native parameter history.

Official reference: [Autodesk — Manage scripts and add-ins](https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/SLD-MANAGE-SCRIPTS-ADD-INS.htm).
