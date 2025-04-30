import logging
import oci
from pathlib import Path

logger: logging.Logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, config, signer, bucket_name: str):
        """Initialize the Runner class with OCI configuration and signer.

        Args:
            config (Any): OCI configuration dictionary.
            signer (Any): OCI signer object for authentication.
            bucket_name (str): Name of the OCI Object Storage bucket.
        """
        self.object_storage = oci.object_storage.ObjectStorageClient(config=config, signer=signer)
        self.namespace = self.object_storage.get_namespace().data
        self.bucket_name: str = bucket_name

    def send_file_to_bucket(self, file_path: Path, bucket_prefix: str) -> None:
        """Upload a file to the OCI Object Storage bucket.

        Args:
            file_path (Path): Path to the file to be uploaded.
            bucket_prefix (str): Prefix for the object name in the bucket.
        """
        logger.info(f"sending {file_path} to {self.bucket_name}")
        with open(file_path, "rb") as file:
            put_object_response: oci.response.Response = self.object_storage.put_object(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                object_name=f"{bucket_prefix}/{file_path.name}",
                put_object_body=file,
            )
        extra = {
            "data": {
                "ETag": put_object_response.headers.get("etag"),
                "last modified": put_object_response.headers.get("last-modified"),
            }
        }
        logger.info("uploaded file to bucket", extra=extra)

    def rotate_file_in_bucket(self, bucket_prefix: str, retention_count: int) -> None:
        """Rotate files in the OCI Object Storage bucket by deleting older backups.

        Args:
            bucket_prefix (str): Prefix for the object names in the bucket.
            retention_count (int): Number of backups to retain.
        """
        objects: list = self.object_storage.list_objects(
            self.namespace, self.bucket_name, prefix=bucket_prefix
        ).data.objects
        backups = sorted([obj.name for obj in objects], reverse=True)
        for backup in backups[retention_count:]:
            logger.info(f"rotating bucket backup by deleting {backup} from bucket")
            self.object_storage.delete_object(self.namespace, self.bucket_name, backup)

    def rotate_file_in_local(self, target_path: Path, retention_count: int) -> None:
        """Rotate files in the local directory by deleting older backups.

        Args:
            target_path (Path): Path to the local directory.
            retention_count (int): Number of backups to retain.
        """
        files: list = list(target_path.glob("*"))
        files.sort(key=lambda x: x.name.split("_")[-1], reverse=True)
        for file in files[retention_count:]:
            logger.info(f"rotating local backup by deleting {file} from local")
            file.unlink()
