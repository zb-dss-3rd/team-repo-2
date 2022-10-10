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

import os
import sys
import tempfile
import unittest

import numpy as np
import torch

from monai.data import DataLoader, Dataset, NumpyReader
from monai.transforms import LoadImaged


class TestNumpyReader(unittest.TestCase):
    def test_npy(self):
        test_data = np.random.randint(0, 256, size=[3, 4, 4])
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npy")
            np.save(filepath, test_data)

            reader = NumpyReader()
            result = reader.get_data(reader.read(filepath))
        np.testing.assert_allclose(result[1]["spatial_shape"], test_data.shape)
        np.testing.assert_allclose(result[0].shape, test_data.shape)
        np.testing.assert_allclose(result[0], test_data)

    def test_npz1(self):
        test_data1 = np.random.randint(0, 256, size=[3, 4, 4])
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npy")
            np.save(filepath, test_data1)

            reader = NumpyReader()
            result = reader.get_data(reader.read(filepath))
        np.testing.assert_allclose(result[1]["spatial_shape"], test_data1.shape)
        np.testing.assert_allclose(result[0].shape, test_data1.shape)
        np.testing.assert_allclose(result[0], test_data1)

    def test_npz2(self):
        test_data1 = np.random.randint(0, 256, size=[3, 4, 4])
        test_data2 = np.random.randint(0, 256, size=[3, 4, 4])
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npz")
            np.savez(filepath, test_data1, test_data2)

            reader = NumpyReader()
            result = reader.get_data(reader.read(filepath))
        np.testing.assert_allclose(result[1]["spatial_shape"], test_data1.shape)
        np.testing.assert_allclose(result[0].shape, (2, 3, 4, 4))
        np.testing.assert_allclose(result[0], np.stack([test_data1, test_data2]))

    def test_npz3(self):
        test_data1 = np.random.randint(0, 256, size=[3, 4, 4])
        test_data2 = np.random.randint(0, 256, size=[3, 4, 4])
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npz")
            np.savez(filepath, test1=test_data1, test2=test_data2)

            reader = NumpyReader(npz_keys=["test1", "test2"])
            result = reader.get_data(reader.read(filepath))
        np.testing.assert_allclose(result[1]["spatial_shape"], test_data1.shape)
        np.testing.assert_allclose(result[0].shape, (2, 3, 4, 4))
        np.testing.assert_allclose(result[0], np.stack([test_data1, test_data2]))

    def test_npy_pickle(self):
        test_data = {"test": np.random.randint(0, 256, size=[3, 4, 4])}
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npy")
            np.save(filepath, test_data, allow_pickle=True)

            reader = NumpyReader()
            result = reader.get_data(reader.read(filepath))[0].item()
        np.testing.assert_allclose(result["test"].shape, test_data["test"].shape)
        np.testing.assert_allclose(result["test"], test_data["test"])

    def test_kwargs(self):
        test_data = {"test": np.random.randint(0, 256, size=[3, 4, 4])}
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npy")
            np.save(filepath, test_data, allow_pickle=True)

            reader = NumpyReader(mmap_mode="r")
            result = reader.get_data(reader.read(filepath, mmap_mode=None))[0].item()
        np.testing.assert_allclose(result["test"].shape, test_data["test"].shape)

    def test_dataloader(self):
        test_data = np.random.randint(0, 256, size=[3, 4, 5])
        datalist = []
        with tempfile.TemporaryDirectory() as tempdir:
            for i in range(4):
                filepath = os.path.join(tempdir, f"test_data{i}.npz")
                np.savez(filepath, test_data)
                datalist.append({"image": filepath})

                num_workers = 2 if sys.platform == "linux" else 0
                loader = DataLoader(
                    Dataset(data=datalist, transform=LoadImaged(keys="image", reader=NumpyReader())),
                    batch_size=2,
                    num_workers=num_workers,
                )
                for d in loader:
                    for s in d["image_meta_dict"]["spatial_shape"]:
                        torch.testing.assert_allclose(s, torch.as_tensor([3, 4, 5]))
                    for c in d["image"]:
                        torch.testing.assert_allclose(c, test_data)

    def test_channel_dim(self):
        test_data = np.random.randint(0, 256, size=[3, 4, 5, 2])
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(tempdir, "test_data.npy")
            np.save(filepath, test_data)

            reader = NumpyReader(channel_dim=-1)
            result = reader.get_data(reader.read(filepath))
        np.testing.assert_allclose(result[1]["spatial_shape"], test_data.shape[:-1])
        self.assertEqual(result[1]["original_channel_dim"], -1)


if __name__ == "__main__":
    unittest.main()
