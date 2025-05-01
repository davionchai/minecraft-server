import logging
from pathlib import Path
from models.arguments import Arguments
from utils.logger import log_setup
from utils.packer import create_gzip_file_with_path
from utils.runner import Runner
from utils.scheduler import run_cron_job


def main(arguments: Arguments) -> None:
    logger.info("starting backup process")

    if arguments.environment == "staging":
        target_path: Path = Path(f"{main_path}/target")
        target_path.mkdir(parents=True, exist_ok=True)
        source_path: Path = Path(f"{main_path}/tests")
    elif arguments.environment == "production":
        target_path: Path = arguments.target_path
        source_path: Path = arguments.source_path

    gzip_filepath: Path = create_gzip_file_with_path(
        target_path=target_path,
        file_prefix=arguments.file_prefix,
        source_path=source_path,
        file_suffix_timestamp_format=arguments.file_suffix_timestamp_format,
    )

    runner = Runner(config=arguments.config, signer=arguments.signer, bucket_name=arguments.bucket_name)
    runner.send_file_to_bucket(
        file_path=gzip_filepath,
        bucket_prefix=arguments.bucket_prefix,
    )
    runner.rotate_file_in_bucket(
        bucket_prefix=arguments.bucket_prefix,
        retention_count=arguments.retention_count,
    )
    runner.rotate_file_in_local(
        target_path=target_path,
        retention_count=arguments.retention_count,
    )

    logger.info("finished backup process")


if __name__ == "__main__":
    main_path: Path = Path(__file__).resolve().parent
    arguments: Arguments = Arguments()
    logger: logging.Logger = log_setup(
        main_path=main_path,
        log_filename=main_path.name,
        logger_level=arguments.sys_log_level,
        rotation_when="midnight",
        rotation_interval=1,
        rotation_backupCount=15,
        provider="discord" if arguments.enable_discord_logging else None,
        provider_level=arguments.discord_log_level,
        webhook=arguments.webhook_url,
    )
    try:
        run_cron_job(
            cron_expr=arguments.cron_schedule,
            task=main,
            arguments=arguments,
        )
        # main(arguments=arguments)
    except Exception as e:
        logger.error(f"error detected: [{e}]", exc_info=True)
        raise
