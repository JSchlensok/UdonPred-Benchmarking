import shutil
from pathlib import Path

from Bio import SeqIO

def prepare_af2_files(
    af_output_path: Path,
    target_directory: Path,
    sequence_file: Path
) -> None:
    """Copy AlphaFold2 PDB files to a target directory with renamed filenames.

    This function reads a FASTA file to map index numbers to sequence IDs,
    then copies AlphaFold2 `.pdb` files from the specified output path
    to a target directory, renaming each file using the corresponding
    sequence ID.

    Args:
        af_output_path: Path to the directory containing AlphaFold2 PDB output files.
        target_directory: Path to the directory where renamed PDB files will be copied.
        sequence_file: Path to file with protein sequences.

    Returns:
        None
    """
    target_directory.mkdir(exist_ok=True)

    ids = {i: rec.id for i, rec in enumerate(SeqIO.parse(sequence_file, "fasta"))}
    for pdb_file in list(af_output_path.glob("*rank_001*.pdb")):
        i = int(pdb_file.stem.split("_")[0])
        shutil.copy(str(pdb_file), str(target_directory / f"{ids[i]}.pdb"))


def prepare_af3_files(
    af_output_path: Path,
    target_directory: Path
) -> None:
    """Copy AlphaFold3 mmCIF files to a target directory with renamed filenames.

    This function searches for AlphaFold3 model `.cif` files in the specified output path
    and copies them to a target directory, renaming each file by removing the
    `_af3_model` suffix from its filename.

    Args:
        af_output_path: Path to the directory containing AlphaFold3 mmCIF output files.
        target_directory: Path to the directory where renamed mmCIF files will be copied.

    Returns:
        None
    """
    target_directory.mkdir(exist_ok=True)
    for mmcif_file in af_output_path.rglob("*af3_model.cif"):
        target_file = target_directory / mmcif_file.name.replace("_af3_model", "")
        shutil.copy(str(mmcif_file), str(target_file))