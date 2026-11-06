"""Static file storage that degrades instead of failing."""

from whitenoise.storage import CompressedManifestStaticFilesStorage


class ForgivingManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Serve a hashed URL when the manifest has one, the plain name otherwise.

    The strict default raises as soon as a template references a file that is
    not in the manifest, which turns one missing asset — or a forgotten
    `collectstatic` — into a 500 on every page. For a public site that trade
    is wrong: an unstyled page is recoverable, a dead site is not.
    """

    manifest_strict = False
