# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2019 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

from __future__ import absolute_import, division, print_function

from hypothesis.internal.compat import hrange
from hypothesis.searchstrategy.featureflags import FeatureStrategy
from tests.common.debug import find_any, minimal

STRAT = FeatureStrategy()


def test_can_all_be_enabled():
    find_any(STRAT, lambda x: all(x.is_enabled(i) for i in hrange(100)))


def test_can_all_be_disabled():
    find_any(STRAT, lambda x: all(not x.is_enabled(i) for i in hrange(100)))


def test_minimizes_open():
    features = hrange(10)

    flags = minimal(STRAT, lambda x: [x.is_enabled(i) for i in features])

    assert all(flags.is_enabled(i) for i in features)


def test_minimizes_individual_features_to_open():
    features = hrange(10)

    flags = minimal(
        STRAT, lambda x: sum([x.is_enabled(i) for i in features]) < len(features)
    )

    assert all(flags.is_enabled(i) for i in features[:-1])
    assert not flags.is_enabled(features[-1])


def test_marks_unknown_features_as_enabled():
    x = find_any(STRAT, lambda v: True)

    assert x.is_enabled("fish")
