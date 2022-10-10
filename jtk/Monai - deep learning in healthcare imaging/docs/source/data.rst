:github_url: https://github.com/Project-MONAI/MONAI

.. _data:

Data
====

Generic Interfaces
------------------
.. currentmodule:: monai.data

`Dataset`
~~~~~~~~~
.. autoclass:: Dataset
  :members:
  :special-members: __getitem__

`IterableDataset`
~~~~~~~~~~~~~~~~~
.. autoclass:: IterableDataset
  :members:
  :special-members: __next__

`DatasetFunc`
~~~~~~~~~~~~~
.. autoclass:: DatasetFunc
  :members:
  :special-members: __next__

`ShuffleBuffer`
~~~~~~~~~~~~~~~
.. autoclass:: ShuffleBuffer
  :members:
  :special-members: __next__

`CSVIterableDataset`
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: CSVIterableDataset
  :members:
  :special-members: __next__

`PersistentDataset`
~~~~~~~~~~~~~~~~~~~
.. autoclass:: PersistentDataset
  :members:
  :special-members: __getitem__

`CacheNTransDataset`
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: CacheNTransDataset
  :members:
  :special-members: __getitem__

`LMDBDataset`
~~~~~~~~~~~~~
.. autoclass:: LMDBDataset
  :members:
  :special-members: __getitem__

`CacheDataset`
~~~~~~~~~~~~~~
.. autoclass:: CacheDataset
  :members:
  :special-members: __getitem__

`SmartCacheDataset`
~~~~~~~~~~~~~~~~~~~
.. autoclass:: SmartCacheDataset
  :members:
  :special-members: __getitem__

`ZipDataset`
~~~~~~~~~~~~
.. autoclass:: ZipDataset
  :members:
  :special-members: __getitem__

`ArrayDataset`
~~~~~~~~~~~~~~
.. autoclass:: ArrayDataset
  :members:
  :special-members: __getitem__

`ImageDataset`
~~~~~~~~~~~~~~
.. autoclass:: ImageDataset
  :members:
  :special-members: __getitem__

`NPZDictItemDataset`
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: NPZDictItemDataset
  :members:
  :special-members: __getitem__

`CSVDataset`
~~~~~~~~~~~~
.. autoclass:: CSVDataset
  :members:
  :special-members: __getitem__

Patch-based dataset
-------------------

`GridPatchDataset`
~~~~~~~~~~~~~~~~~~
.. autoclass:: GridPatchDataset
  :members:

`PatchIter`
~~~~~~~~~~~
.. autoclass:: PatchIter
  :members:

`PatchDataset`
~~~~~~~~~~~~~~
.. autoclass:: PatchDataset
  :members:

Image reader
------------

ImageReader
~~~~~~~~~~~
.. autoclass:: ImageReader
  :members:

ITKReader
~~~~~~~~~
.. autoclass:: ITKReader
  :members:

NibabelReader
~~~~~~~~~~~~~
.. autoclass:: NibabelReader
  :members:

NumpyReader
~~~~~~~~~~~
.. autoclass:: NumpyReader
  :members:

PILReader
~~~~~~~~~
.. autoclass:: PILReader
  :members:

WSIReader
~~~~~~~~~
.. autoclass:: WSIReader
  :members:

Nifti format handling
---------------------

Writing Nifti
~~~~~~~~~~~~~
.. autoclass:: monai.data.NiftiSaver
  :members:

.. autofunction:: monai.data.write_nifti


PNG format handling
-------------------

Writing PNG
~~~~~~~~~~~
.. autoclass:: monai.data.PNGSaver
  :members:

.. autofunction:: monai.data.write_png


Synthetic
---------
.. automodule:: monai.data.synthetic
  :members:


Utilities
---------
.. automodule:: monai.data.utils
  :members:

Partition Dataset
~~~~~~~~~~~~~~~~~
.. autofunction:: monai.data.partition_dataset

Partition Dataset based on classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autofunction:: monai.data.partition_dataset_classes

DistributedSampler
~~~~~~~~~~~~~~~~~~
.. autoclass:: monai.data.DistributedSampler

DistributedWeightedRandomSampler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: monai.data.DistributedWeightedRandomSampler

DatasetSummary
~~~~~~~~~~~~~~
.. autoclass:: monai.data.DatasetSummary

Decathlon Datalist
~~~~~~~~~~~~~~~~~~
.. autofunction:: monai.data.load_decathlon_datalist
.. autofunction:: monai.data.load_decathlon_properties
.. autofunction:: monai.data.check_missing_files
.. autofunction:: monai.data.create_cross_validation_datalist


DataLoader
~~~~~~~~~~
.. autoclass:: monai.data.DataLoader


ThreadBuffer
~~~~~~~~~~~~
.. autoclass:: monai.data.ThreadBuffer

ThreadDataLoader
~~~~~~~~~~~~~~~~
.. autoclass:: monai.data.ThreadDataLoader

TestTimeAugmentation
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: monai.data.TestTimeAugmentation
