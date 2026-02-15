import logging
import os

def setup_logging():
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Example: integrate Sentry if DSN provided (import sentry_sdk in production)
    sentry_dsn = os.environ.get("SENTRY_DSN")
    if sentry_dsn:
        try:
            import sentry_sdk
            sentry_sdk.init(dsn=sentry_dsn)
            logging.getLogger(__name__).info("Sentry initialized")
        except Exception:
            logging.getLogger(__name__).exception("Failed to init Sentry")

    # Return root logger for convenience
    return logging.getLogger()
