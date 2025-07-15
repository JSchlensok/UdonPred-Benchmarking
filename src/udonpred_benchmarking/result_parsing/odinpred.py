import re
from pathlib import Path

import polars as pl

def prepare_odinpred_files(
    path: Path
) -> None:
    for file in path.glob("DisorderPredictions*.txt"):
        content = file.open("r").read()
        content = re.sub(r"[ \t]+", "\t", content)
        file.open("w").write(content)
        file.rename(path / file.name.replace("DisorderPredictions", ""))


def read_odinpred_files(
    path: Path
) -> pl.DataFrame:
    return (
        pl.concat([
            pl.read_csv(file, separator="\t", schema_overrides={"No.": pl.Int16, "Zscore": pl.Float64, "Disorder-Probability": pl.Float64})
            .with_columns(pl.lit(file.stem).alias("protein"))
            .drop("No.")
            .with_row_index("No.", offset=1)
            for file in path.glob("*.txt")
        ])
        .with_columns(
            pl.col("Zscore").fill_null(0),
            pl.col("Disorder-Probability").fill_null(0),
            pl.when(pl.col("Zscore") <= 8).then(1).otherwise(0).alias("ODiNPred_binary")
        )
        .drop("Zscore")
        .rename({
            "Disorder-Probability": "ODiNPred_continuous",
            "No.": "position",
            "Residue": "residue"
        })
    )