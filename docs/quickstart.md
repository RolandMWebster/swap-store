# Quickstart

Guide for getting started with the ``swap-store`` package.

## Installation

The ``swap-store`` package can be installed from GitHub via pip:
```bash
pip install "swapstore[full] @ git+https://github.com/RolandMWebster/swap-store.git"
```

Note: The ``[full]`` option installs all dependencies for all supported cloud object
storage locations. Alternatively, you can install only the dependencies for your storage
location of choice, e.g.:
```bash
# install dependencies for Amazon S3 only
pip install "swapstore[s3] @ git+https://github.com/RolandMWebster/swap-store.git"
```

If you are only using the local storage functionality of ``swap-store``, then you can
ignore any cloud object storage dependencies:
```bash
pip install git+https://github.com/RolandMWebster/swap-store.git
```

## Basic Usage

The ``FileManager`` class is used to enable saving and loading files with a simple
``save()`` and ``load()`` interface. The location type is specified on instantiation of
the ``FileManager`` class and the file type is inferred from the file extension within
the ``save`` and ``load`` methods.

```python
from swapstore import FileManager

# some data to be saved and loaded as part of your project
data = {
    "name": "John Doe",
    "age": 30,
    "email": "johndoe@email.com",
}

# create a file manager instance to store files locally in the "data" directory
file_manager = FileManager(location_type="local", default_directory="data")

# use file manager to easily save and load files
file_manager.save(data, "data.json")  # file type inferred from the file extension
loaded_data = file_manager.load("data.json")
```

## Location-Specific Arguments

Most location types have handler specific arguments that can be passed in via the
`handler_kwargs` argument when instantiating the `FileManager`. For example, when using
S3 you'll need to specify the bucket name:

```python
s3_file_manager = FileManager(
    location_type="s3", handler_kwargs={"bucket_name": "my_bucket"}
)
# use the same interface to save and load files from S3 instead of local disk
s3_file_manager.save(data, "data.json")
loaded_data = s3_file_manager.load("data.json")
```

## Default Directory

When creating a ``FileManager`` instance, you can specify a default directory for storage. This directory will be used as the base path for all file operations. This avoids the need to specify the full path every time you save or load a file and can be useful if storing all your files in a flat storage structure. However, this parameter is
optional and users can instead opt to provide the full path via the ``directory`` parameter directly in the ``save()`` and ``load()`` methods. This approach allows for more flexibility in file organization, and may be more useful in cases where files are organized in subdirectories. The ``default_directory`` parameter can always be overridden on a per-operation basis via the ``directory`` parameter (Note the ``directory`` parameter will **override** the default directory, not append to it).

```python
# save to the default directory
file_manager.save(data, "data.json")  # saves to data/data.json

# save to a specific subdirectory
file_manager.save(data, "data.json", directory="data/subdir")  # saves to data/subdir/data.json
```

## Typical Workflow

The ``swapstore`` package implements a variety of shared storage location services,
but the typical workflow will only involve a single shared storage location (whichever
you or your team has chosen as part of your infrastructure) in conjunction with local storage. Files can be stored locally (or not at all) during development and testing, and then moved to shared storage for production use. See the section below on configuration driven usage for more details on what this looks like in practice.

## Configuration Driven Usage

One of the more powerful ways to make use of the ``swapstore`` package is to use
configuration driven file handling, which makes it easy to manage storage location
details for different environments (e.g. development, production) and to
switch between them with minimal effort. It might look something like the below, where we
start by defining a configuration file in YAML format:

```yaml
#! config.yaml
dev:
    location_type: "local" 
    file_type: "csv"  # for easy viewing in spreadsheet software or IDE
    handler_kwargs:
prod:
    location_type: "s3"  # shared storage accessible by multiple users
    file_type: "parquet"  # for optimized storage and performance
    handler_kwargs:
        bucket_name: "my_bucket"
        path_prefix: "my_project"
```

We opt for local ``.csv`` files in the development environment for ease of use, while in production we switch to using S3 with Parquet files for better performance. We can then
use an environment variable to determine which configuration to load.  Our python code to utilize this configuration might look something like this:

```python
import yaml
import os

# Load configuration from yaml file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Determine file handler configuration based on environment
env = os.getenv("PYTHON_PROJECT_ENV", "dev")  # should be set to "dev" or "prod"
location_type = config[env]["location_type"]
handler_config = config[env]["handler_kwargs"]

# Basic function intended to imitate a typical workflow
def main():
    file_manager = FileManager(
        default_directory="data",
        location_type=location_type,
        handler_kwargs=handler_config,
    )
    raw_data = file_manager.load("raw_data.csv")
    # do some processing here...
    file_manager.save("processed_data.csv", processed_data)
```

Importantly, the code for saving and loading data doesn't change between environments, allowing for a seamless transition from local development to production.


## Path Prefix for Shared Storage Locations

Location types intended for shared storage (Amazon S3, Google Cloud Services, or Azure
Blob Storage) all have a ``path_prefix`` parameter as part of their file
handler's instantiation method. This parameter is used to specify a common prefix for all
files stored in that location and is useful for maintaining consistency between local
storage and shared storage location types. For example, if you're working on a project
locally, called ``my_project`` let's say, then you will likely have a path for storing
your data that is relative to the root of the project called something like `data/`. This
path may also contain subdirectories, such as `data/raw_data/` or `data/outputs/` for
storing data that is specific to certain stages of the project's workflow. Importantly,
due to the self-contained nature of projects, this path is sufficient for storing data
locally without the need to prefix it with the project name (creating something like 
`my_project/data/`). However, when it comes to utilizing a shared storage location type
(e.g. Amazon S3), it's highly possible that all your storage paths are relative to some
root directory that is shared between multiple projects (a shared S3 bucket in Amazon
case). Because of this, we need a way to add an additional directory level to create a project specific path within the shared storage location. This can be done by using the 
``path_prefix`` parameter when instantiating the file handler.

```python
# create a local file manager instance (no path prefix needed)
local_file_manager = FileManager(location_type="local", default_directory="data")

# create an s3 file manager instance with a path prefix
s3_file_manager = FileManager(
    location_type="s3",
    handler_kwargs={
        "bucket_name": "my_bucket",
        "path_prefix": "my_project",
    },
)

# save data to local disk and s3
local_file_manager.save(data, "data.json")  # data is saved to data/data.json
s3_file_manager.save(data, "data.json")  # data is saved to s3://my_bucket/my_project/data/data.json
```
