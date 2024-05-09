"""
This package provides convenient utilities and data to write a sphinx config file.
"""

from __future__ import annotations

from pathlib import Path
import json
from typing import Dict, Tuple, Set, Optional, cast

# I'm thinking of going YEAR.month.releasenumber

__version__ = "0.0.4"

registry_file = Path(__file__).parent / "registry.json"


def get_intersphinx_mapping(
    *, only: Optional[Set[str]]
) -> Dict[str, Tuple[str, Optional[str]]]:
    """
    Return values of intersphinx_mapping for sphinx configuration.

    For convenience, the returned dictionary is a copy so should be ok to
    mutate.

    Parameters
    ----------
    only: Set of Str or None
        Libraries to include.

        Sphinx will download and load all the `objects.inv` listed in
        intersphinx_mapping.  To get all known libraries explicitly pass
        `None`.

    """
    mapping = cast(
        Dict[str, Tuple[str, Optional[str]]],
        {k: tuple(v) for (k, v) in json.loads(registry_file.read_bytes()).items()},
    )
    if only is None:
        return mapping
    else:
        missing = set(only) - set(mapping)
        if missing:
            raise ValueError(f"Missing libraries in 'only': {repr(sorted(missing))}")
        return {k: v for k, v in mapping.items() if k in only}
