---
name: gget
description: Use when doing quick bioinformatics lookups across genomic reference databases with the gget CLI or Python package — finding Ensembl IDs, gene metadata, sequences, BLAST/BLAT searches, enrichment, or protein-structure references. Covers the module set, CLI/Python call shapes, exact flags, and install workflow.
---

# gget

Use this skill when a task needs quick bioinformatics lookup across genomic reference databases with the `gget` CLI or Python package.

## When to Use

- Finding Ensembl IDs, gene metadata, transcript details, or sequences
- Running quick BLAST or BLAT lookups without building a full local pipeline
- Fetching reference genome links and annotations from Ensembl
- Querying protein structure, pathway, cancer, expression, or disease-association modules through a single interface

Use a dedicated workflow instead when the task requires regulated clinical interpretation, high-throughput production pipelines, or fine-grained control over database versions and local indexes.

## Installation

Use a clean Python environment. The upstream databases queried by `gget` change over time — upgrade and re-check module docs before relying on an older environment.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade gget
gget --help

# or with uv
uv venv && . .venv/bin/activate && uv pip install gget
```

## Basic Patterns

```bash
gget <module> [arguments] [options]
```

```python
import gget
result = gget.search(["BRCA1"], species="human")
```

## Common Modules

- `gget search`: find Ensembl IDs from search terms
- `gget info`: retrieve metadata for Ensembl, UniProt, or related IDs
- `gget seq`: fetch nucleotide or amino-acid sequences
- `gget ref`: retrieve reference genome download links
- `gget blast`: run a quick BLAST query
- `gget blat`: locate a sequence against supported genome assemblies
- `gget muscle`: run multiple sequence alignment
- `gget diamond`: run local sequence alignment against reference sequences
- `gget alphafold` and `gget pdb`: inspect protein-structure references
- `gget enrichr`, `gget opentargets`, `gget archs4`, `gget bgee`, `gget cbio`, `gget cosmic`: enrichment, target, expression, cancer, and disease-association data

Not every module supports every Python version or dependency set — some optional scientific dependencies have narrower version support than the core package. Install optional deps with `gget setup`.

## Quick Examples

```bash
# Find genes (-s species, -o output file)
gget search -s human brca1 dna repair -o brca1-search.json

# Fetch gene metadata
gget info ENSG00000012048 -o brca1-info.json

# Fetch a sequence
gget seq ENSG00000012048 -o brca1-seq.fa

# Small BLAST query (-l limit)
gget blast "MEEPQSDPSVEPPLSQETFSDLWKLLPEN" -l 10 -o blast-results.json
```

```python
import gget
genes = gget.search(["BRCA1", "DNA repair"], species="human")
info = gget.info(["ENSG00000012048"])
sequence = gget.seq("ENSG00000012048")
```

Preserve identifiers exactly, including Ensembl/UniProt prefixes. Output formats vary by module: JSON, CSV, FASTA, or a pandas DataFrame.

## References

- gget documentation: https://pachterlab.github.io/gget/
- gget GitHub: https://github.com/pachterlab/gget
- gget paper: https://doi.org/10.1093/bioinformatics/btac836
