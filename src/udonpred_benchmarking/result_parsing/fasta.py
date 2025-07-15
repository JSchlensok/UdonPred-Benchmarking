from typing import Optional

from pathlib import Path

import polars as pl

def read_annotated_fasta_file(
    file: Path,
    contains_sequence: bool,
    method_name: str,
    contains_continuous_scores: bool=True,
    contains_binary_scores: bool=False,
    separator: Optional[str] = None,
    null_value: Optional[str] = "nan",
    binary_threshold: Optional[float] = None
) -> pl.DataFrame:
    lines = [line.strip() for line in file.open("r").readlines()]

    i = 0
    per_protein_dfs = []

    while i < len(lines):
        protein_id = lines[i].lstrip(">")
        i += 1
        if contains_sequence:
            i += 1
        
        if contains_continuous_scores:
            if separator:
                raw_values = lines[i].split(separator)
            else:
                raw_values = list(lines[i])

            continuous_preds = [float(x) if x != null_value else None for x in raw_values]
            i += 1

        if contains_binary_scores:
            if separator:
                raw_values = lines[i].split(separator)
            else:
                raw_values = list(lines[i])

            binary_preds = [int(x) if x != null_value else None for x in raw_values]
            i += 1

        if contains_continuous_scores and contains_binary_scores:
            records = [
                {"protein": protein_id, "position": i+1, f"{method_name}_continuous": pred[0], f"{method_name}_binary": pred[1]}
                for i, pred in enumerate(zip(continuous_preds, binary_preds))
            ]
        elif contains_continuous_scores:
            records = [
                {"protein": protein_id, "position": i+1, f"{method_name}_continuous": pred}
                for i, pred in enumerate(continuous_preds)
            ]
        elif contains_binary_scores:
            records = [
                {"protein": protein_id, "position": i+1, f"{method_name}_binary": pred}
                for i, pred in enumerate(binary_preds)
            ]
        else:
            raise ValueError("File needs to contain at least one type of scores")
        per_protein_dfs.append(pl.from_records(records, schema={"protein": str, "position": pl.Int16, f"{method_name}_binary": pl.Int8}))

    df = pl.concat(per_protein_dfs, how="vertical")
    if binary_threshold:
        df = df.with_columns(
            pl.when(pl.col(f"{method_name}_continuous") <= binary_threshold).then(1).otherwise(0).alias(f"{method_name}_binary")
        )
    return df