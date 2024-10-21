# Swap Store

*A unified Python interface for saving and loading files across various storage types.*

## Overview

In modern applications, the need to read from and write to different storage
locations—such as local disk, cloud storage (e.g., AWS S3), or even mock locations for
testing—can quickly become complex and error-prone. Each storage type often comes with
its own APIs, libraries, and specific configurations, making it challenging to manage and
switch between them seamlessly. This package addresses these challenges by providing a
unified ``save()`` and ``load()`` interface that abstracts away the complexities of
interacting with different storage types. By simplifying this process, it allows
developers to easily swap storage backends without modifying their codebase, making it
ideal for projects that require flexible storage management.

## Caution

While this package provides convenience in some use cases, it does come with some
trade-offs and limitations that should be considered before adopting it:

- **Limited Access to Specific Features:** By abstracting the underlying storage APIs,
the package may not expose all the specialized features or fine-tuned controls available
in specific storage types. If your application requires advanced, storage-specific
functionalities, this package might not meet those needs without additional customization.

- **Potential Performance Overhead:** The abstraction layer introduces a small
performance overhead due to the generalized handling of different storage types. For
applications with high-performance requirements or large-scale data operations, this
might become a consideration.

- **Reduced Flexibility:** While the package aims to simplify storage interactions, it
also reduces flexibility by imposing a standardized interface. This can limit the ability
to fully exploit the unique capabilities of each storage type or to handle edge cases
specific to certain storage solutions.

- **Increased Complexity for Simple Use Cases:** For applications that only require
interaction with a single storage type (e.g., local filesystem only), using this package
might introduce unnecessary complexity. In such cases, directly using the relevant
storage API could be simpler and more straightforward.

With that being said...

<p align="center">
<img src="https://github.com/user-attachments/assets/aef4ae48-877b-4799-a7cf-8896af9ae8cd" width="500">
</p>

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

## Example Usage

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

For more detailed usage, refer to the [quickstart guide](docs/quickstart.md).

## Supported Input/Output Types and Storage Locations

The table below summarizes the supported input/output types and storage locations:

| Object Type | File Type(s) | Location Type(s) |
|-------------|--------------|------------------|
| ``pandas.DataFrame`` | ``.csv``, ``.parquet`` | ``Local``, ``Azure``, ``S3``, ``Google``, ``None`` |
| ``dict`` | ``.json`` | ``Local``, ``Azure``, ``S3``, ``Google``, ``None`` |
| ``Any`` | ``.pkl`` | ``Local``, ``Azure``, ``S3``, ``Google``, ``None`` |
