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
- `ligands/ligands.csv` — three simple, well-known small
  molecules (aspirin, caffeine, ibuprofen) by SMILES, in the `mol_id,smiles`
  format `vs_vina_pipeline.py`'s CSV path expects.

## Prerequisites

Python 2.7, OpenBabel, AutoDock Vina, and MGLTools/AutoDockTools — none
bundled here. See "Installing prerequisites" in the main README for
where to get each one and exactly what to set `script_path`/`vina_path`/
`python_path` to.

## Running it

`vs_vina_pipeline.py` now ships with this example as its default config
(`path = "example/"`, `recfile_name = "1hsg_protein.pdb"`,
`binding_site_name = "example"`), so after installing the prerequisites
above and setting `script_path`/`vina_path`/`python_path` for your
environment, just run it from the repo root:

```
python vs_vina_pipeline.py
```

This prepares the receptor, converts the three SMILES to 3D ligands via
OpenBabel, prepares them for Vina, docks each against the example binding
site, and writes results to `example/example_1hsg_protein/` (from
`out_path = path + binding_site_name + "_" + recfile_name[:-4] + "/"`),
including a `_results.csv` of docking energies.

When you're ready to point it at your own project, edit `path`,
`recfile_name`, and add your own entry to `BINDING_SITES`. To get a
`center` for a new binding site: open the receptor in Pymol, select or
zoom to the pocket, then run `print cmd.get_position()` to read off
coordinates. The `example` entry above was instead computed directly from
the bound ligand's atom coordinates in the original 1HSG structure — the
geometric center and extent of the `HETATM`/`MK1` records, with padding
added to the extent for the box `size`.
