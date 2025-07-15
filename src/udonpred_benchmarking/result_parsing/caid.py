from typing import IO, Optional

import warnings
from pathlib import Path
from io import StringIO

import polars as pl


def read_caid_file(
    file: IO[str],
    protein_name: str,
    method_name: str,
    has_binary_scores: bool = True,
    binary_threshold: Optional[float] = None
) -> pl.DataFrame:
    """Parse a single CAID file (or file-like object) into a DataFrame.

    If the file does not contain a binary score column, one is computed using
    `binary_threshold`.

    Args:
        file: An open file-like object containing CAID data.
        protein_name: Name of the protein (used as an identifier).
        method_name: Name of the prediction method (used to name columns).
        has_binary_scores: Whether a binary score column is expected or should be computed.
        binary_threshold: Threshold to convert continuous scores to binary scores if needed.

    Returns:
        A Polars DataFrame with columns:
        ["protein", "position", "residue", "<method>_continuous", "<method>_binary"].
    """
    column_names = ["position", "residue", f"{method_name}_continuous"]
    if has_binary_scores:
        column_names.append(f"{method_name}_binary")

    df = (
        pl.read_csv(
            file,
            separator="\t",
            skip_lines=1,
            has_header=False,
            new_columns=column_names
        )
        .with_columns(pl.lit(protein_name).alias("protein"))
    )

    if binary_threshold:
        if has_binary_scores:
            warnings.warn("Overriding binary scores from file since binarization threshold was provided")
        df = df.with_columns(
            pl.when(pl.col(f"{method_name}_continuous") <= binary_threshold)
            .then(0)
            .otherwise(1)
            .alias(f"{method_name}_binary")
        )

    return df.select(
        ["protein", "position", "residue", f"{method_name}_continuous", f"{method_name}_binary"]
    )


def read_caid_files(
    directory: Path,
    method_name: str,
    has_binary_scores: bool = True,
    binary_threshold: Optional[float] = None
) -> pl.DataFrame:
    """Read and concatenate multiple single-protein CAID files from a directory.

    Args:
        parent_directory: Path to the directory containing `.caid` files.
        method_name: Name of the prediction method (used to name columns).
        has_binary_scores: Whether files contain a column with binarized scores.
        binary_threshold: Threshold to convert continuous scores to binary scores.

    Returns:
        A concatenated Polars DataFrame with CAID data for all proteins.
    """
    dfs = []
    for path in directory.glob("*.caid"):
        with open(path, "r") as f:
            dfs.append(
                read_caid_file(
                    f,
                    path.stem,
                    method_name,
                    has_binary_scores=has_binary_scores,
                    binary_threshold=binary_threshold
                )
            )

    return pl.concat(dfs)


def read_multi_caid_file(
    file: Path,
    method_name: str,
    separator: str = "\t",
    has_binary_scores: bool = True,
    binary_threshold: Optional[float] = None
) -> pl.DataFrame:
    """Read a multi-protein CAID file, split it in memory, and parse each protein.

    The input file should contain multiple protein sections starting with a '>' line.

    Args:
        file: Path to the multi-protein CAID file.
        method_name: Name of the prediction method (used to name columns).
        separator: Separator used in the data lines.
        has_binary_scores: Whether file contains a column with binarized scores.
        binary_threshold: Threshold to convert continuous scores to binary scores.

    Returns:
        A concatenated Polars DataFrame with CAID data for all proteins.
    """
    lines = file.read_text().splitlines()
    dfs: list[pl.DataFrame] = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith(">"):
            protein_id = line[1:]
            entries = ["position\tresidue\tdisorder"]
            i += 1
            while i < len(lines) and not lines[i].startswith(">"):
                entries.append(lines[i].strip())
                i += 1

            file_like = StringIO("\n".join(entries))
            df = read_caid_file(
                file_like,
                protein_id,
                method_name,
                has_binary_scores=has_binary_scores,
                binary_threshold=binary_threshold
            )
            dfs.append(df)

    return pl.concat(dfs)

