from pathlib import Path

import polars as pl

def read_fldpnn_file(
    file: Path
) -> pl.DataFrame:
    per_protein_dfs = []
    lines = file.open("r").readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith(">"):
            protein_id = line[1:].replace("[WARNING]", "")
            header = lines[i+1].strip().split(",")
            entries = []
            i += 2

            while i < len(lines) and not lines[i].startswith(">"):
                entries.append(lines[i].split(","))
                i += 1

            per_protein_dfs.append(pl.DataFrame(entries, schema=header, orient="row").with_columns(pl.lit(protein_id).alias("protein_id")))

    return (
        pl.concat(per_protein_dfs)
        .select(["protein_id", "Residue Number", "Residue Type", "Predicted Score for Disorder", "Binary Prediction for Disorder"])
        .rename({
            "Predicted Score for Disorder": "flDPnn_continuous",
            "Binary Prediction for Disorder": "flDPnn_binary",
            "protein_id": "protein",
            "Residue Number": "position",
            "Residue Type": "residue"
        })
        .with_columns(
            pl.col("position").cast(pl.Int16),
            pl.col("flDPnn_continuous").cast(pl.Float64),
            pl.col("flDPnn_binary").cast(pl.Int8)
        )
    )