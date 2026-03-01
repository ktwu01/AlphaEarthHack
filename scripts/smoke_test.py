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
        )
    except ImportError as e:
        errors.append(f"Cannot import src.config: {e}")
        return errors

    if not ALPHAEARTH_COLLECTION:
        errors.append("ALPHAEARTH_COLLECTION is empty")

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

    if not errors:
        print(f"  OK  AlphaEarth collection: {ALPHAEARTH_COLLECTION}")
        print(f"  OK  Thresholds: AE={AE_MAG_THRESHOLD}, LT={LT_MAG_THRESHOLD}")

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

    print("\n3. GEE authentication instructions...")
    check_gee_auth_instructions()

    print()
    if failed_imports or config_errors:
        print("RESULT: FAILED")
        if failed_imports:
            print(f"  Missing packages: {failed_imports}")
            print("  Run:  conda env create -f environment.yml && conda activate alphaearth")
        if config_errors:
            for e in config_errors:
                print(f"  Config error: {e}")
        return 1

    print("RESULT: PASSED — environment and config look good.")
    print("        Next step: authenticate GEE, then run notebooks in order.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
