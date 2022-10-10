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
import skimage.transform
from parameterized import parameterized

from monai.transforms import Resize
from tests.utils import TEST_NDARRAYS, NumpyImageTestCase2D, assert_allclose

TEST_CASE_0 = [{"spatial_size": 15}, (6, 10, 15)]

TEST_CASE_1 = [{"spatial_size": 15, "mode": "area"}, (6, 10, 15)]

TEST_CASE_2 = [{"spatial_size": 6, "mode": "trilinear", "align_corners": True}, (2, 4, 6)]


class TestResize(NumpyImageTestCase2D):
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            resize = Resize(spatial_size=(128, 128, 3), mode="order")
            resize(self.imt[0])

        with self.assertRaises(ValueError):
            resize = Resize(spatial_size=(128,), mode="order")
            resize(self.imt[0])

    @parameterized.expand(
        [((32, -1), "area"), ((32, 32), "area"), ((32, 32, 32), "trilinear"), ((256, 256), "bilinear")]
    )
    def test_correct_results(self, spatial_size, mode):
        resize = Resize(spatial_size, mode=mode)
        _order = 0
        if mode.endswith("linear"):
            _order = 1
        if spatial_size == (32, -1):
            spatial_size = (32, 64)
        expected = [
            skimage.transform.resize(
                channel, spatial_size, order=_order, clip=False, preserve_range=False, anti_aliasing=False
            )
            for channel in self.imt[0]
        ]

        expected = np.stack(expected).astype(np.float32)
        for p in TEST_NDARRAYS:
            out = resize(p(self.imt[0]))
            assert_allclose(out, expected, type_test=False, atol=0.9)

    @parameterized.expand([TEST_CASE_0, TEST_CASE_1, TEST_CASE_2])
    def test_longest_shape(self, input_param, expected_shape):
        input_data = np.random.randint(0, 2, size=[3, 4, 7, 10])
        input_param["size_mode"] = "longest"
        result = Resize(**input_param)(input_data)
        np.testing.assert_allclose(result.shape[1:], expected_shape)

    def test_longest_infinite_decimals(self):
        resize = Resize(spatial_size=1008, size_mode="longest", mode="bilinear", align_corners=False)
        ret = resize(np.random.randint(0, 2, size=[1, 2544, 3032]))
        self.assertTupleEqual(ret.shape, (1, 846, 1008))


if __name__ == "__main__":
    unittest.main()
