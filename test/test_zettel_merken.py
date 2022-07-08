#
# USAGE: zettel-merken $ python -m pytest [ -q test/ ]
#
# https://docs.pytest.org/en/7.1.x/explanation/pythonpath.html#invoking-pytest-versus-python-m-pytest
#

import src.zettel_merken as zm


def test_some():
    assert zm.mainx() == 1
