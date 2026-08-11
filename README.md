# Virtual-Screening

Python 2 scripts for AutoDock Vina (and, separately, AutoDock4) virtual
screening: receptor/ligand preparation, docking, and result extraction.
Each script has a hardcoded config block at the top that needs editing
for your project before running.

## Main pipeline: `vs_vina_pipeline.py`

The primary, actively-used Vina pipeline. For a project working directory
(`path` in the script) containing `receptor/` and either a ligands folder
or a `(mol_id, SMILES)` CSV, it:

1. Prepares the receptor (`prepare_receptor4.py`, pdb → pdbqt)
2. Prepares ligands — from a CSV it also generates 3D mol2 files from
   SMILES at one or more pH values (`obabel --gen3D`), otherwise from an
   existing folder of `.mol2`/`.pdb` files (`prepare_ligand4.py`)
3. Writes a Vina `conf.txt` for the configured binding site (see
   `BINDING_SITES` in the script)
4. Runs Vina per ligand
5. Converts docked poses to SDF and extracts the first (best) pose per
   ligand
6. Extracts docking energies into a results CSV (`utilities/vina_results.py`)

### Local vs. HPC mode

Set `HPC = True`/`False` near the top of the script.

- **Local** (`HPC = False`): run directly, no arguments. Set
  `checkpoint_start` to resume from a specific ligand index if a previous
  run was interrupted; it processes through to the end of the list.
- **HPC** (`HPC = True`): intended for an SGE array job. Takes two
  positional CLI arguments, `start` and `end` (`python vs_vina_pipeline.py
  start end`), and processes only ligands with index in `[start, end)` —
  each array task handles one slice, writing its own
  `<end>_results.csv` so concurrent tasks don't collide. See
  `submit_vina_sge_array.sh` for an example array-job submission script
  (adjust `BATCH_SIZE` and the `qsub -t` range to match your ligand count).

### Configuration

Edit near the top of the script: `path` (project directory), `recfile_name`,
`binding_site_name` (must be a key in `BINDING_SITES`, or add a new one),
`script_path`/`vina_path`/`python_path` for your environment.

## Other scripts

- **`parallel_autodock_vs.py`** — a separate pipeline using **AutoDock4**
  (grid/GA-based, via `prepare_gpf4.py`/`prepare_dpf42.py`/`Autogrid4`/
  `Autodock4`), parallelized locally with `multiprocessing.Pool`. Not
  related to the Vina pipeline above — different docking engine entirely.
- **`parallel_vina_vs.py`** — Vina docking parallelized locally across
  cores with `multiprocessing.Pool`, for machines without cluster access
  (as opposed to `vs_vina_pipeline.py`'s HPC array-job mode).
- **`submit_vina_sge_array.sh`** — SGE array-job submission script for
  `vs_vina_pipeline.py`'s HPC mode.

## `utilities/`

- **`vina_results.py`** — shared `extraction()`/`is_number()`/`makefile()`
  helpers used by `vs_vina_pipeline.py` (parses Vina `.pdbqt` output into
  a results CSV, writes Vina config files).
- **`select_top_compounds.py`** — copies ligand files whose ID appears in
  a `results.csv` into a `Top-Selection` folder (post-hoc shortlisting).
- **`set_mol2_titles_from_filename.py`** — sets each mol2 file's title to its
  filename via `babel`.
- **`zinc15script.py`** — bulk-extracts and converts a downloaded ZINC15
  tranche (`.gz` → `.pdbqt`), organizing outputs by ZINC ID.
- **`set_vina_priority_high.bat`** / **`set_vina_priority_low.bat`** —
  Windows only: set the running `vina.exe` process to high or idle CPU
  priority (via `wmic ... setpriority`), to speed up docking or let it run
  in the background without slowing down other programs.

## Requirements

Python 2.7, OpenBabel (`babel`/`obabel` on PATH), AutoDock Vina
(`vina`/`vina.exe`), and MGLTools/AutoDockTools (`prepare_receptor4.py`,
`prepare_ligand4.py`).
