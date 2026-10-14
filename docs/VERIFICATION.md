# Verification and provenance

Prepared 14 October 2026 from existing local packages `WaveRelief_Fusion_v1_0_3` and `WaveRelief_Fusion_V2`. No replacement generator code was invented. All four Python source files match their originals byte for byte. Manifest authors were changed to Gerald Jaideep as requested. Source hashes appear in [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json).

## Checks performed for this packaging

- All four Python files parse and compile successfully without executing Fusion entry points.
- Both analytic profile helpers were sampled at 10,201 default grid points each: finite normalized depths within [0, 1].
- V2 adaptive anchors were checked across all 61 sections for ordering, uniqueness and endpoints.
- Manifest JSON parsed; author metadata normalized; Python source fidelity checked byte for byte.
- Original previews inspected visually and labelled accurately.

## Recovered desktop evidence

The [V1 log](evidence/v1-build.txt) records all 49 closed sections and `COMPLETE: one solid created` at 19:05:55. The [V2 log](evidence/v2-build.txt) records all 61 closed sections and the same completion status at 21:20:23. Local installation paths were removed from the copies. These are pre-existing logs, not fresh runs performed for this release. They do not identify the exact Fusion build or prove every parameter combination or operating system works.

The original guides and validation JSON predate this evidence and describe native execution as unverified. They are retained with an explanatory notice; this document supersedes that historical status. A new native execution, full compatibility matrix and machining validation have not been performed.

Original export validation JSON reports valid single-solid STEP geometry and closed STL edges. Those CAD-kernel checks were not rerun during packaging. V2 records maximum sampled analytic-field error 0.6780967441981431 mm. Exported models use a different spline/loft kernel from native Fusion and may differ.

The original portable exporter source and genuine Fusion screenshots were not present in the recovered packages. The supplied images are mathematical previews.
