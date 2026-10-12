import os
import sys
from pathlib import Path

import pytest

BACKSIDE = Path(__file__).resolve().parents[1]
REPO = BACKSIDE.parent
# BACKSIDE holds scripts/, schemas/, stations/ ...; the repo root holds workflows/.
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(BACKSIDE))


@pytest.fixture(autouse=True)
def _run_from_backside():
    # Tests name sibling folders relative to the working directory (schemas/..., stations/...).
    old = os.getcwd()
    os.chdir(BACKSIDE)
    yield
    os.chdir(old)
