import logging
import tarfile
from datetime import datetime, timezone
from pathlib import Path


logger: logging.Logger = logging.getLogger(__name__)


def create_gzip_file_with_path(
    source_path: Path, target_path: Path, file_prefix: str, file_suffix_timestamp_format: str
) -> Path:
    """Create a gzip file from the source path and save it to the target path.

    Args:
        target_path (Path): The directory where the gzip file will be saved.
        file_prefix (str): The prefix for the gzip file name.
        source_path (Path): The path of the directory to be archived.
        file_suffix_timestamp_format (str): The format for the timestamp suffix in the gzip file name.

    Returns:
        Path: The path of the created gzip file.
    """
    current_timestamp: str = datetime.now(timezone.utc).strftime(file_suffix_timestamp_format)
    gzip_filename: str = f"{file_prefix}_{current_timestamp}.tar.gz"
    gzip_filepath: Path = Path(f"{target_path}/{gzip_filename}")

    with tarfile.open(gzip_filepath, "w:gz") as tar:
        tar.add(source_path, arcname=Path(source_path).name)

    logger.info(f"created backup [{gzip_filepath}]")

    return gzip_filepath
