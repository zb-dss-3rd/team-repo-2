# Copyright 2020 - 2021 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
from parameterized import parameterized

from monai.transforms import Flipd
from tests.utils import TEST_NDARRAYS, NumpyImageTestCase2D, assert_allclose

INVALID_CASES = [("wrong_axis", ["s", 1], TypeError), ("not_numbers", "s", TypeError)]

VALID_CASES = [("no_axis", None), ("one_axis", 1), ("many_axis", [0, 1])]


class TestFlipd(NumpyImageTestCase2D):
    @parameterized.expand(INVALID_CASES)
    def test_invalid_cases(self, _, spatial_axis, raises):
        with self.assertRaises(raises):
            flip = Flipd(keys="img", spatial_axis=spatial_axis)
            flip({"img": self.imt[0]})

    @parameterized.expand(VALID_CASES)
    def test_correct_results(self, _, spatial_axis):
        for p in TEST_NDARRAYS:
            flip = Flipd(keys="img", spatial_axis=spatial_axis)
            expected = [np.flip(channel, spatial_axis) for channel in self.imt[0]]
            expected = np.stack(expected)
            result = flip({"img": p(self.imt[0])})["img"]
            assert_allclose(result, p(expected))


if __name__ == "__main__":
    unittest.main()
