from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from poetry.core.constraints.version import EmptyConstraint
from poetry.core.constraints.version import Version
from poetry.core.constraints.version import VersionRange
from poetry.core.constraints.version import VersionUnion


if TYPE_CHECKING:
    from poetry.core.constraints.version import VersionConstraint


@pytest.mark.parametrize(
    "constraint",
    [
        EmptyConstraint(),
        Version.parse("1"),
        VersionRange(Version.parse("1"), Version.parse("2")),
        VersionUnion(
            VersionRange(Version.parse("1"), Version.parse("2")),
            VersionRange(Version.parse("3"), Version.parse("4")),
        ),
    ],
)
def test_constraints_are_hashable(constraint: VersionConstraint) -> None:
    # We're just testing that constraints are hashable, there's nothing much to say
    # about the result.
    hash(constraint)


@pytest.mark.parametrize(
    ("constraint", "expected"),
    [
        (EmptyConstraint(), True),
        (Version.parse("1"), True),
        (VersionRange(), False),
        (VersionRange(Version.parse("1")), False),
        (VersionRange(max=Version.parse("2")), True),
        (VersionRange(Version.parse("1"), Version.parse("2")), True),
        (
            VersionUnion(
                VersionRange(Version.parse("1"), Version.parse("2")),
                VersionRange(Version.parse("3"), Version.parse("4")),
            ),
            True,
        ),
        (
            VersionUnion(
                VersionRange(Version.parse("1"), Version.parse("2")),
                VersionRange(Version.parse("3")),
            ),
            False,
        ),
    ],
)
def test_has_upper_bound(constraint: VersionConstraint, expected: bool) -> None:
    assert constraint.has_upper_bound() is expected
