from hatch.template import File
from hatch.utils.fs import Path

from ..new.default import get_files as get_template_files
from .utils import DEFAULT_METADATA_VERSION


def get_files(**kwargs):
    relative_root = kwargs.get('relative_root', '')

    files = [
        File(Path(relative_root, f.path), f.contents)
        for f in get_template_files(**kwargs)
    ]

    files.extend(
        (
            File(Path(relative_root, kwargs['package_name'], 'lib.so'), ''),
            File(
                Path(relative_root, '.gitignore'),
                """\
*.pyc
*.so
*.h
""",
            ),
            File(
                Path(relative_root, 'build.py'),
                """\
import pathlib

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        pathlib.Path('my_app', 'lib.so').touch()
        pathlib.Path('my_app', 'lib.h').touch()
""",
            ),
            File(
                Path(relative_root, 'PKG-INFO'),
                f"""\
Metadata-Version: {DEFAULT_METADATA_VERSION}
Name: {kwargs["project_name_normalized"]}
Version: 0.0.1
""",
            ),
        )
    )

    return files
