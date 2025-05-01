import base64
import json
import os
import oci
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Arguments:
    """Arguments class to handle configuration and environment variables for the backup agent.

    Attributes:
        sys_log_level (str): The logging level for the system.
        enable_discord_logging (bool): Flag to enable Discord logging.
        secret_id (str): The OCID of the secret in OCI Vault.
        discord_log_level (str): The logging level for Discord.
        environment (str): The environment in which the application is running (staging/production).
        file_prefix (str): The prefix for the backup file name.
        file_suffix_timestamp_format (str): The format for the timestamp suffix in the backup file name.
        target_path (Path): The path where the backup file will be stored.
        source_path (str): The path of the source directory to be backed up.
        bucket_name (str): The name of the OCI Object Storage bucket.
        bucket_prefix (str): The prefix for the backup file in the bucket.
        retention_count (int): The number of backup files to retain.
        config (Any): The OCI configuration object.
        signer (Any): The OCI signer object for authentication.
        webhook_url (str): The Discord webhook URL for logging.
    """

    # system level
    cron_schedule: str = field(default_factory=lambda: os.getenv("CRON_SCHEDULE", "0 2 * * *"))
    sys_log_level: str = field(default_factory=lambda: os.getenv("SYS_LOG_LEVEL", "INFO").upper())
    enable_discord_logging: bool = field(
        default_factory=lambda: os.getenv("ENABLE_DISCORD_LOGGING", "False").lower() == "true"
    )
    secret_id: str = field(default_factory=lambda: os.getenv("SECRET_ID"))
    discord_log_level: str = field(default_factory=lambda: os.getenv("DISCORD_LOG_LEVEL", "INFO").upper())
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "staging"))
    # app level
    file_prefix: str = field(default_factory=lambda: os.getenv("FILE_PREFIX", "backup"))
    file_suffix_timestamp_format: str = field(
        default_factory=lambda: os.getenv("FILE_SUFFIX_TIMESTAMP_FORMAT", "%Y%m%dT%H%M%S")
    )
    target_path: Path = field(default_factory=lambda: Path(os.getenv("TARGET_PATH", "")))
    source_path: str = field(default_factory=lambda: os.getenv("SOURCE_PATH"))
    bucket_name: str = field(default_factory=lambda: os.getenv("BUCKET_NAME"))
    bucket_prefix: str = field(default_factory=lambda: os.getenv("BUCKET_PREFIX", "backup"))
    retention_count: str = field(default_factory=lambda: int(os.getenv("RETENTION_COUNT", "10")))
    # internal level
    config: Any = None
    signer: Any = None
    webhook_url: str = None

    def __post_init__(self) -> None:
        self.config, self.signer = self.__sign_in_oci()
        if self.enable_discord_logging and self.secret_id:
            secret_data = self.__get_secret(self.secret_id)
            self.webhook_url = secret_data.get("discord_webhook_url")

    def __sign_in_oci(self) -> Any:
        """Signs in to Oracle Cloud Infrastructure (OCI) using Instance Principal authentication.

        Returns:
            Any: A tuple containing the OCI configuration and signer object.
        """
        if self.environment == "staging":
            config = oci.config.from_file(file_location="~/.oci/config", profile_name="DEFAULT")
            token_file = config["security_token_file"]
            token = None
            with open(token_file) as f:
                token = f.read()
            private_key = oci.signer.load_private_key_from_file(config["key_file"])
            signer = oci.auth.signers.SecurityTokenSigner(token, private_key)
        elif self.environment == "production":
            config = {}
            signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        return config, signer

    def __get_secret(self, secret_id):
        """Retrieves and decodes a base64-encoded JSON secret from OCI Vault.

        Args:
            secret_id (str): The OCID of the secret.

        Returns:
            dict: A dictionary containing the secret data (e.g., {'username': '...', 'password': '...'}).
        """
        secrets_client = oci.secrets.SecretsClient(config=self.config, signer=self.signer)
        response: oci.response.Response = secrets_client.get_secret_bundle(secret_id=secret_id)
        base64_content: str = response.data.secret_bundle_content.content
        decoded_secret: dict = json.loads(base64.b64decode(base64_content).decode("utf-8"))
        return decoded_secret
