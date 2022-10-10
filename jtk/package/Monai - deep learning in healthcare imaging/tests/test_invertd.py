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

import sys
import unittest

import numpy as np
import torch

from monai.data import CacheDataset, DataLoader, create_test_image_3d, decollate_batch
from monai.transforms import (
    AddChanneld,
    CastToTyped,
    Compose,
    CopyItemsd,
    EnsureTyped,
    Invertd,
    LoadImaged,
    Orientationd,
    RandAffined,
    RandAxisFlipd,
    RandFlipd,
    RandRotate90d,
    RandRotated,
    RandZoomd,
    ResizeWithPadOrCropd,
    ScaleIntensityd,
    Spacingd,
    ToTensord,
)
from monai.utils import set_determinism
from tests.utils import make_nifti_image

KEYS = ["image", "label"]


class TestInvertd(unittest.TestCase):
    def test_invert(self):
        set_determinism(seed=0)
        im_fname, seg_fname = (make_nifti_image(i) for i in create_test_image_3d(101, 100, 107, noise_max=100))
        transform = Compose(
            [
                LoadImaged(KEYS),
                AddChanneld(KEYS),
                Orientationd(KEYS, "RPS"),
                Spacingd(KEYS, pixdim=(1.2, 1.01, 0.9), mode=["bilinear", "nearest"], dtype=np.float32),
                ScaleIntensityd("image", minv=1, maxv=10),
                RandFlipd(KEYS, prob=0.5, spatial_axis=[1, 2]),
                RandAxisFlipd(KEYS, prob=0.5),
                RandRotate90d(KEYS, spatial_axes=(1, 2)),
                RandZoomd(KEYS, prob=0.5, min_zoom=0.5, max_zoom=1.1, keep_size=True),
                RandRotated(KEYS, prob=0.5, range_x=np.pi, mode="bilinear", align_corners=True),
                RandAffined(KEYS, prob=0.5, rotate_range=np.pi, mode="nearest"),
                ResizeWithPadOrCropd(KEYS, 100),
                # test EnsureTensor for complicated dict data and invert it
                CopyItemsd("image_meta_dict", times=1, names="test_dict"),
                # test to support Tensor, Numpy array and dictionary when inverting
                EnsureTyped(keys=["image", "test_dict"]),
                ToTensord("image"),
                CastToTyped(KEYS, dtype=[torch.uint8, np.uint8]),
                CopyItemsd("label", times=2, names=["label_inverted", "label_inverted1"]),
                CopyItemsd("image", times=2, names=["image_inverted", "image_inverted1"]),
            ]
        )
        data = [{"image": im_fname, "label": seg_fname} for _ in range(12)]

        # num workers = 0 for mac or gpu transforms
        num_workers = 0 if sys.platform != "linux" or torch.cuda.is_available() else 2

        dataset = CacheDataset(data, transform=transform, progress=False)
        loader = DataLoader(dataset, num_workers=num_workers, batch_size=5)
        inverter = Invertd(
            # `image` was not copied, invert the original value directly
            keys=["image_inverted", "label_inverted", "test_dict"],
            transform=transform,
            orig_keys=["label", "label", "test_dict"],
            meta_keys=["image_inverted_meta_dict", "label_inverted_meta_dict", None],
            orig_meta_keys=["label_meta_dict", "label_meta_dict", None],
            nearest_interp=True,
            to_tensor=[True, False, False],
            device="cpu",
        )

        inverter_1 = Invertd(
            # `image` was not copied, invert the original value directly
            keys=["image_inverted1", "label_inverted1"],
            transform=transform,
            orig_keys=["image", "image"],
            meta_keys=["image_inverted1_meta_dict", "label_inverted1_meta_dict"],
            orig_meta_keys=["image_meta_dict", "image_meta_dict"],
            nearest_interp=[True, False],
            to_tensor=[True, True],
            device="cpu",
        )

        expected_keys = [
            "image",
            "image_inverted",
            "image_inverted1",
            "image_inverted1_meta_dict",
            "image_inverted_meta_dict",
            "image_meta_dict",
            "image_transforms",
            "label",
            "label_inverted",
            "label_inverted1",
            "label_inverted1_meta_dict",
            "label_inverted_meta_dict",
            "label_meta_dict",
            "label_transforms",
            "test_dict",
            "test_dict_transforms",
        ]
        # execute 1 epoch
        for d in loader:
            d = decollate_batch(d)
            for item in d:
                item = inverter(item)
                item = inverter_1(item)

                self.assertListEqual(sorted(item), expected_keys)
                self.assertTupleEqual(item["image"].shape[1:], (100, 100, 100))
                self.assertTupleEqual(item["label"].shape[1:], (100, 100, 100))
                # check the nearest interpolation mode
                i = item["image_inverted"]
                torch.testing.assert_allclose(i.to(torch.uint8).to(torch.float), i.to(torch.float))
                self.assertTupleEqual(i.shape[1:], (100, 101, 107))
                i = item["label_inverted"]
                torch.testing.assert_allclose(i.to(torch.uint8).to(torch.float), i.to(torch.float))
                self.assertTupleEqual(i.shape[1:], (100, 101, 107))
                # test inverted test_dict
                self.assertTrue(isinstance(item["test_dict"]["affine"], np.ndarray))
                self.assertTrue(isinstance(item["test_dict"]["filename_or_obj"], str))

                # check the case that different items use different interpolation mode to invert transforms
                d = item["image_inverted1"]
                # if the interpolation mode is nearest, accumulated diff should be smaller than 1
                self.assertLess(torch.sum(d.to(torch.float) - d.to(torch.uint8).to(torch.float)).item(), 1.0)
                self.assertTupleEqual(d.shape, (1, 100, 101, 107))

                d = item["label_inverted1"]
                # if the interpolation mode is not nearest, accumulated diff should be greater than 10000
                self.assertGreater(torch.sum(d.to(torch.float) - d.to(torch.uint8).to(torch.float)).item(), 10000.0)
                self.assertTupleEqual(d.shape, (1, 100, 101, 107))

        # check labels match
        reverted = item["label_inverted"].detach().cpu().numpy().astype(np.int32)
        original = LoadImaged(KEYS)(data[-1])["label"]
        n_good = np.sum(np.isclose(reverted, original, atol=1e-3))
        reverted_name = item["label_inverted_meta_dict"]["filename_or_obj"]
        original_name = data[-1]["label"]
        self.assertEqual(reverted_name, original_name)
        print("invert diff", reverted.size - n_good)
        # 25300: 2 workers (cpu, non-macos)
        # 1812: 0 workers (gpu or macos)
        # 1821: windows torch 1.10.0
        self.assertTrue((reverted.size - n_good) in (34007, 1812, 1821), f"diff.  {reverted.size - n_good}")

        set_determinism(seed=None)


if __name__ == "__main__":
    unittest.main()
