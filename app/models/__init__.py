
"""Models package

Ensure all model modules are imported so SQLAlchemy `Base.metadata` is populated
before migrations or table creation runs.
"""

from . import resource, user  # noqa: F401
