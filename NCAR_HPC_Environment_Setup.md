# GeoAI Course - NCAR HPC Environment Setup Guide

This repository contains labs and assignments for the GeoAI course running on NCAR's Glade system.

## Table of Contents
- [Environment Information](#environment-information)
- [Quick Start](#quick-start)
- [Jupyter Notebook Setup](#jupyter-notebook-setup)
- [Understanding the Environment](#understanding-the-environment)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Environment Information

**Conda Environment Name:** `geolab`
**Location:** `/glade/work/wukoutian/conda-envs/geolab`

### Installed Packages
- **matplotlib:** 3.10.6 - Plotting and visualization
- **rasterio:** 1.4.3 - Geospatial raster I/O
- **numpy:** 2.2.6 - Numerical computing
- **geopandas:** Latest - Vector geospatial data handling
- **pyogrio:** Latest - Fast vector I/O
- **Additional packages:** shapely, pyproj, pandas, and more

## Quick Start

### For Command Line / Terminal Sessions

Run these commands before starting your Python session:

```bash
# Load NCAR environment modules
module load ncarenv/24.12
module load conda/latest

# Activate the geolab environment
conda activate geolab

# Verify installation
python -c "import matplotlib, rasterio, numpy; print('✓ Environment ready')"
```

### For Jupyter Notebooks

See the [Jupyter Notebook Setup](#jupyter-notebook-setup) section below for the 3-cell setup pattern.

## Jupyter Notebook Setup

**IMPORTANT:** All Jupyter notebooks (Lab 2, Lab 3, etc.) should start with these three setup cells to ensure a clean, isolated environment.

### Cell 1: Load NCAR Modules
```python
%%bash
module load ncarenv/24.12
module load conda/latest
echo "✓ Modules loaded successfully"
```

**What this does:** Loads the NCAR environment and conda module system.

---

### Cell 2: Activate Conda Environment
```python
%%bash
# Unset MPLBACKEND to avoid matplotlib backend conflicts
unset MPLBACKEND
export PYTHONNOUSERSITE=1
source /glade/u/apps/opt/conda/etc/profile.d/conda.sh
conda activate /glade/work/wukoutian/conda-envs/geolab
echo "✓ Conda environment 'geolab' activated"
echo "Python: $(which python)"
python -c "import sys; print('User site disabled:', not hasattr(sys, 'USER_SITE') or sys.flags.no_user_site)"
```

**What this does:**
- Unsets `MPLBACKEND` to prevent Jupyter's matplotlib backend from conflicting
- Sets `PYTHONNOUSERSITE=1` to ignore packages in `~/.local/lib/python3.10/site-packages/`
- Activates the geolab conda environment
- Verifies the correct Python interpreter is being used

---

### Cell 3: Configure Python Kernel
```python
# Set environment to ignore user site-packages and fix matplotlib backend
import os
import sys

# Unset MPLBACKEND and set PYTHONNOUSERSITE
if 'MPLBACKEND' in os.environ:
    del os.environ['MPLBACKEND']
os.environ['PYTHONNOUSERSITE'] = '1'

# Clear any previously imported modules to ensure clean imports
modules_to_clear = ['numpy', 'matplotlib', 'matplotlib.pyplot', 'rasterio', 'rasterio.plot']
for mod in modules_to_clear:
    if mod in sys.modules:
        del sys.modules[mod]

print("✓ Environment configured to use conda packages only")
print(f"Python executable: {sys.executable}")
print(f"PYTHONNOUSERSITE set: {os.environ.get('PYTHONNOUSERSITE', 'not set')}")
print(f"MPLBACKEND: {os.environ.get('MPLBACKEND', 'not set (good)')}")

# Now test imports
try:
    import matplotlib
    import matplotlib.pyplot as plt
    import rasterio
    import numpy as np
    print(f"\n✓ All packages imported successfully:")
    print(f"  - matplotlib: {matplotlib.__version__}")
    print(f"  - rasterio: {rasterio.__version__}")
    print(f"  - numpy: {np.__version__}")
except Exception as e:
    print(f"\n✗ Import error: {e}")
```

**What this does:**
- Configures the Python kernel to use only conda environment packages
- Clears any previously loaded module caches
- Tests all critical imports to verify the environment is working
- Provides diagnostic output to help debug issues

---

## Understanding the Environment

### Why Three Setup Cells?

The three-cell setup pattern addresses common issues on NCAR HPC systems:

1. **Cell 1 (Bash):** Loads system modules - this is standard NCAR HPC practice
2. **Cell 2 (Bash):** Activates conda and sets environment variables in the bash context
3. **Cell 3 (Python):** Configures the Python kernel itself to use the correct packages

### The Package Conflict Problem

On NCAR Glade, you may have packages installed in **two locations**:

1. **`~/.local/lib/python3.10/site-packages/`** - User-installed packages (via pip install --user)
2. **`/glade/work/wukoutian/conda-envs/geolab/`** - Conda environment packages

By default, Python searches `~/.local/` **first**, which can cause:
- Version conflicts (e.g., incompatible numpy versions)
- Corrupted packages (e.g., "file too short" errors)
- Backend conflicts (e.g., matplotlib_inline vs. conda matplotlib)

**Solution:** The `PYTHONNOUSERSITE=1` flag tells Python to skip `~/.local/` entirely and use only conda packages.

### Why Lab 2 Works Without This

Lab 2 (vector analysis with geopandas) happens to work because:
- Geopandas and its dependencies in `~/.local/` are compatible
- No matplotlib backend conflicts occur with vector plotting
- The packages were installed more recently and aren't corrupted

### Why Lab 3 Needs This

Lab 3 (raster analysis with rasterio) requires:
- Rasterio, which is only in the conda environment
- This triggers loading of numpy from `~/.local/`, which is corrupted
- Matplotlib backend conflicts appear when mixing conda and user packages

**Lesson:** Always use the three-cell setup for consistency, even if some labs seem to work without it.

## Course Structure

```
geoai-course/
├── Lab-1/                      # Lab 1 materials
├── Lab-2/                      # Lab 2: Vector Data Analysis (geopandas)
│   └── Lab2_Koutian_Wu.ipynb   # Works with or without strict isolation
├── Lab-3/                      # Lab 3: Raster Data Analysis (rasterio)
│   └── Lab3_Koutian_Wu.ipynb   # REQUIRES three-cell setup
└── NCAR_HPC_Environment_Setup.md  # This file
```

## Troubleshooting

### EnvironmentNotWritableError

**Error Message:**
```
EnvironmentNotWritableError: The current user does not have write permissions to the target environment.
  environment location: /glade/u/apps/opt/conda
```

**Cause:** You're trying to modify the system base conda environment (read-only).

**Solution:** Always activate your personal `geolab` environment first:

```bash
# Wrong - tries to modify base environment
conda install package_name

# Correct - modifies your geolab environment
conda activate geolab
conda install package_name

# Alternative - use -p flag with full path
conda install -y -c conda-forge package_name -p /glade/work/wukoutian/conda-envs/geolab
```

---

### ModuleNotFoundError

**Error Message:**
```
ModuleNotFoundError: No module named 'rasterio'
ModuleNotFoundError: No module named 'geopandas'
```

**Cause:** The conda environment isn't activated, or you're using the wrong Python interpreter.

**Solution:**
1. Make sure you've run all three setup cells in order
2. Check which Python is being used: `!which python` (should show `/glade/work/wukoutian/conda-envs/geolab/bin/python`)
3. If wrong, restart the kernel and re-run the setup cells

---

### ImportError: numpy file too short

**Error Message:**
```
ImportError: /glade/u/home/wukoutian/.local/lib/python3.10/site-packages/numpy/_core/_multiarray_umath.cpython-310-x86_64-linux-gnu.so: file too short
```

**Cause:** Corrupted numpy installation in your `~/.local/` directory.

**Solution:** Use `PYTHONNOUSERSITE=1` (already included in Cell 2 and Cell 3 above).

**Alternative (if issues persist):**
```bash
# Temporarily rename the local packages directory
mv ~/.local/lib/python3.10/site-packages ~/.local/lib/python3.10/site-packages.backup

# To restore later (after your lab is done):
mv ~/.local/lib/python3.10/site-packages.backup ~/.local/lib/python3.10/site-packages
```

---

### Matplotlib Backend Conflicts

**Error Message:**
```
ValueError: Key backend: 'module://matplotlib_inline.backend_inline' is not a valid value for backend
```

**Cause:** Jupyter Notebook sets `MPLBACKEND=module://matplotlib_inline.backend_inline`, which is incompatible with conda's matplotlib.

**Solution:** Use `unset MPLBACKEND` (already included in Cell 2 above).

**What's happening:**
- Jupyter/IPython uses matplotlib_inline backend for interactive plots
- Conda's matplotlib doesn't recognize this backend
- Unsetting the variable lets matplotlib choose the right backend automatically

---

### Kernel Dies or Crashes

**Symptoms:** Jupyter kernel crashes when importing packages.

**Possible Causes:**
1. Memory issues (unlikely on HPC)
2. Conflicting shared libraries
3. Multiple package sources mixing incompatible versions

**Solution:**
1. Restart the kernel: `Kernel → Restart Kernel`
2. Run all three setup cells in order
3. If still failing, check diagnostics in Cell 3 output
4. As a last resort, consider recreating the conda environment

---

## Best Practices

### DO ✓

1. **Always use the three-cell setup** at the start of every notebook
2. **Run cells in order** - don't skip the setup cells
3. **Restart kernel if you change environments**
4. **Use conda for package installation** in the geolab environment
5. **Check Cell 3 output** to verify all packages loaded correctly
6. **Use `conda list`** to see what's installed in your environment

### DON'T ✗

1. **Don't use `pip install` without activating the environment first**
2. **Don't install packages with `--user` flag** when using conda environments
3. **Don't skip the setup cells** even if previous labs worked without them
4. **Don't mix conda and pip** unless absolutely necessary
5. **Don't modify the system base conda environment**
6. **Don't delete Cell 1, 2, or 3** from lab notebooks

### Installing New Packages

If you need to add a package to your environment:

```bash
# From terminal
module load ncarenv/24.12
module load conda/latest
conda activate geolab
conda install -c conda-forge package_name

# Or use the -p flag
conda install -y -c conda-forge package_name -p /glade/work/wukoutian/conda-envs/geolab
```

**After installing, restart your Jupyter kernel and re-run the setup cells.**

### Verifying Your Environment

From command line:
```bash
module load ncarenv/24.12
module load conda/latest
conda activate geolab
conda list | grep -E "(matplotlib|rasterio|numpy|geopandas)"
```

Expected output:
```
geopandas                 1.1.1
matplotlib                3.10.6
matplotlib-base           3.10.6
numpy                     2.2.6
rasterio                  1.4.3
```

## Additional Resources

### NCAR Documentation
- **NCAR Conda Guide:** Check NCAR's official documentation for conda usage on Glade
- **Module System:** Use `module spider conda` to see available versions
- **Storage Info:** `gladequota` to check your disk usage on /glade/work

### Useful Commands

```bash
# List all conda environments
conda env list

# Show packages in current environment
conda list

# Search for a package
conda search package_name

# Get info about conda
conda info

# Check which Python you're using
which python

# Check Python version
python --version

# Test imports from command line
python -c "import matplotlib, rasterio, numpy; print('✓ All packages available')"
```

### Getting Help

If you encounter issues not covered here:
1. Check the error message carefully - it often tells you exactly what's wrong
2. Verify you ran all three setup cells in order
3. Check the Cell 3 output for diagnostic information
4. Try restarting the kernel and re-running setup cells
5. Check if your packages are corrupted: `conda list --show-channel-urls`
6. Consider reaching out to NCAR support or your course instructor

---

## Summary

**Key Takeaways:**

1. **Always use the three-cell setup pattern** in Jupyter notebooks
2. **`PYTHONNOUSERSITE=1`** prevents conflicts with `~/.local/` packages
3. **`unset MPLBACKEND`** fixes matplotlib backend conflicts
4. **Lab 2 works by luck, Lab 3 requires proper setup** - be consistent
5. **Never modify the base conda environment** - always use `geolab`
6. **When in doubt, restart kernel and re-run setup cells**

This setup ensures a **clean, reproducible, isolated environment** for all your GeoAI coursework on NCAR HPC systems.
