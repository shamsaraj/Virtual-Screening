# Example: running vs_vina_pipeline.py

A minimal, runnable example for the pipeline's local (non-HPC) mode, using
a small, well-known, public-domain structure rather than any of the
scripts' real project data. **This is for learning the folder layout and
workflow mechanics, not a real docking study** — the three ligands below
were picked for being simple and well-known, not because they're expected
to bind this target.

**Disclaimer:** this example folder structure and config have not been
run end-to-end here (this environment doesn't have Vina/OpenBabel/MGLTools
installed) — please verify it works before relying on it.

## What's here

- `receptor/1hsg_protein.pdb` — chains A and B (the HIV-1 protease dimer)
  from [PDB 1HSG](https://www.rcsb.org/structure/1HSG) (public domain),
  with the crystallographic ligand (MK1) and waters stripped out, leaving
  protein atoms only. 1HSG is the structure used in AutoDock Vina's own
  tutorial.
- `ligands_selected_3/ligands.csv` — three simple, well-known small
  molecules (aspirin, caffeine, ibuprofen) by SMILES, in the `mol_id,smiles`
  format `vs_vina_pipeline.py`'s CSV path expects.

## Prerequisites

Install separately (not bundled here — see the main README and the note
on MGLTools licensing): Python 2.7, OpenBabel, AutoDock Vina, and
MGLTools/AutoDockTools (`prepare_receptor4.py`, `prepare_ligand4.py`).

## Running it

`vs_vina_pipeline.py`'s config (path, receptor name, binding site) is
hardcoded at the top of the script rather than passed as arguments, so to
try this example you'll need to **temporarily edit those lines**, then
revert them before going back to your real project:

1. Set `path` to the absolute path of this `example/` folder (must end
   with `/`).
2. Set `recfile_name = "1hsg_protein.pdb"`.
3. Add a temporary entry to `BINDING_SITES` and point `binding_site_name`
   at it — the box below is centered on the native ligand's binding pocket
   (computed directly from its coordinates in the original 1HSG structure,
   with padding):

   ```python
   BINDING_SITES["example"] = {"size": (20, 20, 20), "center": (13, 22, 6)}
   ```
   ```python
   binding_site_name = "example"
   ```
4. Make sure `HPC = False`.
5. Run: `python vs_vina_pipeline.py`

This will prepare the receptor, convert the three SMILES to 3D ligands via
OpenBabel, prepare them for Vina, dock each against the example binding
site, and write results to `example/example_1hsg_protein/` (from
`out_path = path + binding_site_name + "_" + recfile_name[:-4] + "/"`),
including a `_results.csv` of docking energies.
