import importlib
import os

# Import the stdlib `logging` module via importlib to avoid
# static-analysis confusion with this module's filename.
_stdlib_logging = importlib.import_module("logging")


def setup_logging():
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    _stdlib_logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Example: integrate Sentry if DSN provided (import sentry_sdk in production)
    sentry_dsn = os.environ.get("SENTRY_DSN")
    if sentry_dsn:
        try:
            sentry_sdk = importlib.import_module("sentry_sdk")
        except Exception:
            _stdlib_logging.getLogger(__name__).warning("sentry_sdk not installed; skipping Sentry init")
        else:
            try:
                sentry_sdk.init(dsn=sentry_dsn)
                _stdlib_logging.getLogger(__name__).info("Sentry initialized")
            except Exception:
                _stdlib_logging.getLogger(__name__).exception("Failed to init Sentry")

    # Return root logger for convenience
    return _stdlib_logging.getLogger()
