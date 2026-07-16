"""
Smoke test — run without GEE auth to verify environment and config are sane.

    python -m scripts.smoke_test
"""

import importlib
import sys

REQUIRED_PACKAGES = [
    "ee",
    "geemap",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "scipy",
    "ipyleaflet",
    "ipywidgets",
    "nbformat",
]


def check_imports() -> list[str]:
    failed = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
            print(f"  OK  {pkg}")
        except ImportError as e:
            print(f"  FAIL {pkg}: {e}")
            failed.append(pkg)
    return failed


def check_config() -> list[str]:
    errors = []
    try:
        from src.config import (
            ALPHAEARTH_COLLECTION,
            LANDTRENDR_ASSETS,
            AE_MAG_THRESHOLD,
            LT_MAG_THRESHOLD,
            AE_YEAR_START,
            AE_YEAR_END,
            GEE_PROJECT,
        )
    except ImportError as e:
        errors.append(f"Cannot import src.config: {e}")
        return errors

    if not ALPHAEARTH_COLLECTION:
        errors.append("ALPHAEARTH_COLLECTION is empty")

    if not GEE_PROJECT:
        errors.append("GEE_PROJECT is empty")

    expected_sites = 15
    if len(LANDTRENDR_ASSETS) != expected_sites:
        errors.append(
            f"Expected {expected_sites} LandTrendr assets, "
            f"got {len(LANDTRENDR_ASSETS)}"
        )
    else:
        print(f"  OK  {len(LANDTRENDR_ASSETS)} LandTrendr asset paths defined")

    for name, asset_id in LANDTRENDR_ASSETS.items():
        if not asset_id.startswith("users/") and not asset_id.startswith("projects/"):
            errors.append(f"Asset '{name}' has unexpected path: {asset_id}")

    if AE_MAG_THRESHOLD <= 0:
        errors.append(f"AE_MAG_THRESHOLD must be > 0, got {AE_MAG_THRESHOLD}")
    if LT_MAG_THRESHOLD <= 0:
        errors.append(f"LT_MAG_THRESHOLD must be > 0, got {LT_MAG_THRESHOLD}")
    if not (2017 <= AE_YEAR_START <= AE_YEAR_END <= 2024):
        errors.append(
            f"Year range [{AE_YEAR_START}, {AE_YEAR_END}] is outside 2017–2024"
        )

    if not errors:
        print(f"  OK  GEE project: {GEE_PROJECT}")
        print(f"  OK  AlphaEarth collection: {ALPHAEARTH_COLLECTION}")
        print(f"  OK  Thresholds: AE={AE_MAG_THRESHOLD}, LT={LT_MAG_THRESHOLD}")
        print(f"  OK  Year range: {AE_YEAR_START}–{AE_YEAR_END}")

    return errors


def check_change_detection() -> list[str]:
    errors = []
    try:
        from src.change_detection import (
            normalize_image,
            compute_alpha_layers,
            smooth_and_mask_alpha,
            find_lt_band,
        )
        print("  OK  src.change_detection importable")
        print(f"  OK  Functions: {normalize_image.__name__}, {compute_alpha_layers.__name__}, "
              f"{smooth_and_mask_alpha.__name__}, {find_lt_band.__name__}")
    except ImportError as e:
        errors.append(f"Cannot import src.change_detection: {e}")
    return errors


def check_visualization() -> list[str]:
    errors = []
    try:
        from src.visualization import VIS_YOD, VIS_MAG_AE, VIS_MAG_LT, VIS_DUR
        for name, obj in [("VIS_YOD", VIS_YOD), ("VIS_MAG_AE", VIS_MAG_AE),
                          ("VIS_MAG_LT", VIS_MAG_LT), ("VIS_DUR", VIS_DUR)]:
            if not isinstance(obj, dict) or "palette" not in obj:
                errors.append(f"{name} is not a valid vis-param dict")
        if not errors:
            print("  OK  src.visualization importable (VIS_YOD, VIS_MAG_AE, VIS_MAG_LT, VIS_DUR)")
    except ImportError as e:
        errors.append(f"Cannot import src.visualization: {e}")
    return errors


def check_gee_auth_instructions() -> None:
    """Remind the user how to authenticate; does NOT attempt ee.Initialize()."""
    try:
        import ee  # noqa: F401
        print("  OK  earthengine-api importable")
        print("      To authenticate, run:")
        print("        earthengine authenticate")
        print("      or in Python:")
        print("        import ee; ee.Authenticate(); ee.Initialize()")
    except ImportError:
        print("  FAIL earthengine-api not installed")


def main() -> int:
    print("\n=== Smoke Test: AlphaEarth Change Detection ===\n")

    print("1. Checking required packages...")
    failed_imports = check_imports()

    print("\n2. Checking src/config.py...")
    config_errors = check_config()

    print("\n3. Checking src/change_detection.py...")
    cd_errors = check_change_detection()

    print("\n4. Checking src/visualization.py...")
    vis_errors = check_visualization()

    print("\n5. GEE authentication instructions...")
    check_gee_auth_instructions()

    all_errors = failed_imports + config_errors + cd_errors + vis_errors

    print()
    if all_errors:
        print("RESULT: FAILED")
        if failed_imports:
            print(f"  Missing packages: {failed_imports}")
            print("  Run:  conda env create -f environment.yml && conda activate alphaearth")
        for e in config_errors + cd_errors + vis_errors:
            print(f"  Error: {e}")
        return 1

    print("RESULT: PASSED — environment and config look good.")
    print("        Next step: authenticate GEE, then run notebooks in order.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
