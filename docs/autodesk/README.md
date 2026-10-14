# Autodesk App Store submission pack

**Prepared listing copy and review plan; not submitted or Autodesk-approved.**

## Listing copy

**Product name:** Wave Relief for Autodesk Fusion  
**Publisher / author:** Gerald Jaideep  
**Distribution:** Free, MIT licensed  
**Source repository:** https://github.com/jaideepg01/Fusion360-WaveRelief  
**Product versions:** V1.0.3 and V2.0.0

**Short description:** Create parametric wave-relief panels with rounded waves or concave channels in Autodesk Fusion.

**Full description:** Wave Relief creates a new Fusion design with an editable relief surface and flat back. Choose V1 for broad rounded waves or V2 for concave channels with adjustable narrow crests. Change panel dimensions, nominal carving depth, wave density, bend, centre position, oval proportions and phase through native user parameters. V2 adds RidgeSharpness and a rebuild workflow that refreshes adaptive crest samples after major styling changes. Both scripts display progress and write a local diagnostic log. Fixed-geometry STEP and STL examples accompany the scripts. Default examples use a 200 × 380 mm panel based on 11 mm stock and 4 mm nominal depth. Manufacturing toolpaths and G-code are not included.

**Getting started / help:** Use [installation and troubleshooting](../INSTALLATION.md), plus the version-specific parameter guides. Launch through Scripts and Add-Ins → Scripts. There is no persistent toolbar command.

**Support:** Repository Issues. Publisher must supply and verify the support email in the Autodesk submission portal.

**Privacy statement:** The recovered Python source has no network calls, telemetry, account system or licensing service. It writes a diagnostic log beside the script, including the local script path. Users choose whether to share logs for support. Fusion’s own services are outside this script’s control.

**Media captions:** V1 — original mathematical preview of a rounded-wave panel. V2 — original mathematical preview with profile comparison. These are not application screenshots or manufactured results.

## Submission readiness

- [x] Original V1/V2 source, MIT license and author credit assembled.
- [x] Listing copy, help, version history, genuine preview assets and source provenance prepared.
- [x] Saved logs show a completed one-solid build for each version.
- [ ] Record the current Fusion build and test Windows/macOS separately before claiming support for both.
- [ ] Test first run, parameter edits, V2 rebuild, cancel/failure handling and uninstall on each claimed platform.
- [ ] Capture genuine Fusion screenshots showing the finished body, parameters and command entry; no source screenshots were found in the recovered packages.
- [ ] Supply a publisher-approved product icon and verified support email.
- [ ] Confirm with Autodesk how these manually launched Python scripts should be packaged. Build and test the required installer/bundle for the accepted submission format; do not submit the repository ZIP as a certified installer.
- [ ] Complete publisher registration, review the Publisher Agreement, and submit through the publisher portal.

Autodesk’s current guidance requires compatibility with the latest Fusion and describes installer and `.bundle` packaging. These source scripts are not yet a tested App Store bundle. The final agreement and portal requirements control the submission.

Reference checked 14 October 2026: [Autodesk Fusion publishing guidelines](https://aps.autodesk.com/marketplace/publisher-center/fusion-publisher-guidelines).

## Reviewer test plan

For each claimed OS, record Fusion build and hardware. Register each script in a clean installation, run default generation, save and reopen F3D, and confirm a solid body with a flat rear surface. Record dimensions and inspect for surface defects. Change panel size and one styling parameter; confirm timeline recompute. In V2 change phase/centre, rebuild, and verify a new document retains built-in values while refreshing anchors. Test cancellation and inspect partial-document behavior. Confirm log location and successful unlink/removal. Compare native geometry to the supplied STEP while allowing for different spline kernels. Record results rather than inferring pass status from source review.
