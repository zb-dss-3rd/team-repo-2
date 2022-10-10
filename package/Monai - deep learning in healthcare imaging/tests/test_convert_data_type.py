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
from typing import List, Tuple

import numpy as np
import torch
from parameterized import parameterized

from monai.utils.type_conversion import convert_data_type, convert_to_dst_type
from tests.utils import TEST_NDARRAYS

TESTS: List[Tuple] = []
for in_type in TEST_NDARRAYS + (int, float):
    for out_type in TEST_NDARRAYS:
        TESTS.append((in_type(np.array(1.0)), out_type(np.array(1.0))))  # type: ignore

TESTS_LIST: List[Tuple] = []
for in_type in TEST_NDARRAYS + (int, float):
    for out_type in TEST_NDARRAYS:
        TESTS_LIST.append(
            ([in_type(np.array(1.0)), in_type(np.array(1.0))], out_type(np.array([1.0, 1.0])), True)  # type: ignore
        )
        TESTS_LIST.append(
            (
                [in_type(np.array(1.0)), in_type(np.array(1.0))],  # type: ignore
                [out_type(np.array(1.0)), out_type(np.array(1.0))],
                False,
            )
        )


class TestTensor(torch.Tensor):
    pass


class TestConvertDataType(unittest.TestCase):
    @parameterized.expand(TESTS)
    def test_convert_data_type(self, in_image, im_out):
        converted_im, orig_type, orig_device = convert_data_type(in_image, type(im_out))
        # check input is unchanged
        self.assertEqual(type(in_image), orig_type)
        if isinstance(in_image, torch.Tensor):
            self.assertEqual(in_image.device, orig_device)
        # check output is desired type
        self.assertEqual(type(converted_im), type(im_out))
        # check dtype is unchanged
        if isinstance(in_type, (np.ndarray, torch.Tensor)):
            self.assertEqual(converted_im.dtype, im_out.dtype)

    def test_neg_stride(self):
        _ = convert_data_type(np.array((1, 2))[::-1], torch.Tensor)

    @parameterized.expand(TESTS_LIST)
    def test_convert_list(self, in_image, im_out, wrap):
        output_type = type(im_out) if wrap else type(im_out[0])
        converted_im, *_ = convert_data_type(in_image, output_type, wrap_sequence=wrap)
        # check output is desired type
        if not wrap:
            converted_im = converted_im[0]
            im_out = im_out[0]
        self.assertEqual(type(converted_im), type(im_out))
        # check dtype is unchanged
        if isinstance(in_type, (np.ndarray, torch.Tensor)):
            self.assertEqual(converted_im.dtype, im_out.dtype)


class TestConvertDataSame(unittest.TestCase):
    # add test for subclass of Tensor
    @parameterized.expand(TESTS + [(np.array(1.0), TestTensor(np.array(1.0)))])
    def test_convert_data_type(self, in_image, im_out):
        converted_im, orig_type, orig_device = convert_to_dst_type(in_image, im_out)
        # check input is unchanged
        self.assertEqual(type(in_image), orig_type)
        if isinstance(in_image, torch.Tensor):
            self.assertEqual(in_image.device, orig_device)
        # check output is desired type
        if isinstance(im_out, torch.Tensor):
            output_type = torch.Tensor
        else:
            output_type = np.ndarray
        self.assertEqual(type(converted_im), output_type)
        # check dtype is unchanged
        if isinstance(in_type, (np.ndarray, torch.Tensor)):
            self.assertEqual(converted_im.dtype, im_out.dtype)


if __name__ == "__main__":
    unittest.main()
