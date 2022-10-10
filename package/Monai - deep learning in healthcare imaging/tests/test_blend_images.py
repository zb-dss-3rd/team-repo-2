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
from unittest.case import skipUnless

import torch
from parameterized import parameterized

from monai.data.synthetic import create_test_image_2d, create_test_image_3d
from monai.transforms.utils_pytorch_numpy_unification import moveaxis
from monai.utils.module import optional_import
from monai.visualize.utils import blend_images
from tests.utils import TEST_NDARRAYS

plt, has_matplotlib = optional_import("matplotlib.pyplot")

TESTS = []
for p in TEST_NDARRAYS:
    image, label = create_test_image_2d(100, 101)
    TESTS.append((p(image), p(label)))

    image, label = create_test_image_3d(100, 101, 102)
    TESTS.append((p(image), p(label)))


@skipUnless(has_matplotlib, "Matplotlib required")
class TestBlendImages(unittest.TestCase):
    @parameterized.expand(TESTS)
    def test_blend(self, image, label):
        blended = blend_images(image[None], label[None])
        self.assertEqual(type(image), type(blended))
        if isinstance(blended, torch.Tensor):
            self.assertEqual(blended.device, image.device)
            blended = blended.cpu().numpy()
        self.assertEqual((3,) + image.shape, blended.shape)

        blended = moveaxis(blended, 0, -1)  # move RGB component to end
        if blended.ndim > 3:
            blended = blended[blended.shape[0] // 2]
        plt.imshow(blended)


if __name__ == "__main__":
    unittest.main()
