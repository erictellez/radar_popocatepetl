# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 20:23:11 2022

@author: https://www.noahbrenowitz.com/post/loading_netcdfs/
"""

import numpy
import netCDF4 as nc
import xarray
import tensorflow_datasets as tfds
import tensorflow as tf
import os
import shutil
import glob
import plotly.express as px

print("Tensorflow:", tf.version.VERSION)
print("Xarray:", xarray.__version__)
print("netCDF4:", nc.__version__)


# initialize directory of files
dir_ = "ncfiles"
kb = 1_024
mb = kb * kb


def save_dirs(target_size: int, total_size: int, dir_: str):
    shutil.rmtree(dir_, ignore_errors=True)
    os.makedirs(dir_)
    nfiles = int(total_size / target_size)
    n = int(target_size / 8)
    ds = xarray.DataArray(numpy.random.uniform(size=(n // 64, 64))).to_dataset(name="a")
    os.makedirs(dir_, exist_ok=True)

    print("Data size (MB):", ds.nbytes/mb)

    for i in range(nfiles):
        path = os.path.join(dir_, "{:2d}.nc".format(i))
        ds.to_netcdf(path)
        
# from generator method
def load_nc_dir_with_generator(dir_):
    def gen():
        for file in glob.glob(os.path.join(dir_, "*.nc")):
            ds = xarray.open_dataset(file, engine='netcdf4')
            yield {key: tf.convert_to_tensor(val) for key, val in ds.items()}


    sample = next(iter(gen()))

    return tf.data.Dataset.from_generator(
        gen,
        output_signature={
            key: tf.TensorSpec(val.shape, dtype=val.dtype)
            for key, val in sample.items()
        }
    )


def load_nc_dir_with_map_and_xarray(dir_):
    def open_path(path_tensor: tf.Tensor):
        ds = xarray.open_dataset(path_tensor.numpy().decode())
        return tf.convert_to_tensor(ds["a"])
    return tf.data.Dataset.list_files(os.path.join(dir_, "*.nc")).map(
        lambda path: tf.py_function(open_path, [path], Tout=tf.float64),
        )

def load_nc_dir_cached_to_tfrecord(dir_):
    """Save data to tfRecord, open it, and deserialize
    
    Note that tfrecords are not that complicated! The simply store some
    bytes, and you can serialize data into those bytes however you find
    convenient. In this case, I serialie with `tf.io.serialize_tensor` and 
    deserialize with `tf.io.parse_tensor`. No need for `tf.train.Example` or any
    of the other complexities mentioned in the official tutorial.

    """
    generator_tfds = load_nc_dir_with_generator(dir_)
    writer = tf.data.experimental.TFRecordWriter("local.tfrecord")
    writer.write(generator_tfds.map(lambda x: tf.io.serialize_tensor(x["a"])))

    return tf.data.TFRecordDataset("local.tfrecord").map(
        lambda x: tf.io.parse_tensor(x, tf.float64))


def load_nc_dir_after_save(dir_):
    generator_tfds = load_nc_dir_with_generator(dir_)
    tf.data.experimental.save(generator_tfds, "local_ds")
    return tf.data.experimental.load("local_ds")

def load_nc_dir_cache_to_disk(dir_):
    generator_tfds = load_nc_dir_with_generator(dir_)
    cached = generator_tfds.cache(f"{dir_}/.cache")
    list(cached)
    return cached
    

def load_nc_dir_cache_to_mem(dir_):
    generator_tfds = load_nc_dir_with_generator(dir_)
    cached = generator_tfds.cache()
    list(cached)
    return cached

def load_nc_dir_to_bytes(dir_):
    return tf.data.Dataset.list_files(os.path.join(dir_, "*.nc")).map(tf.io.read_file)

def get_datasets(dir_):
    return dict(
        generator = load_nc_dir_with_generator(dir_),
        map = load_nc_dir_with_map_and_xarray(dir_),
        tfrecord = load_nc_dir_cached_to_tfrecord(dir_),
        tf_data_save = load_nc_dir_after_save(dir_),
        cache_disk = load_nc_dir_cache_to_disk(dir_),
        bytes_only = load_nc_dir_to_bytes(dir_),
        cache_mem = load_nc_dir_cache_to_mem(dir_),
    )

