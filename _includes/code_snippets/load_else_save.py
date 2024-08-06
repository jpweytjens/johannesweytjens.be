import functools
import hashlib
import inspect
import logging
import pathlib
import re
import textwrap

import black
import pandas as pd

logging.basicConfig(level="INFO")


def load_else_save(filename):
    """Decorator for slow functions that return a pandas DataFrame. When first
    running the function, the decorator will save the DataFrame to
    ``filename``. When rerunning the function the data is loaded from
    ``filename`` instead of rerunning the function. If the source code of the
    function changes, the function will be rerun and the new output will again
    be saved to ``filename``. Adding full line comments to the source code or
    changing the formatting of the source code of the function will not trigger
    running the function again. Any other change will.

    Does not support jupyterlab magic such as ``%%time``. The cell in which the
    decorated function is declared can not contain any jupyterlab magic functions.
    Calling the decorated function in another cell with jupyterlab magic works
    as expected.

    Examples
    --------

    >>> import pandas as pd
    >>> @load_else_save("data.parquet")
    >>> def slow_computation():
    >>>    # some long computation
    >>>    df = pd.DataFrame({"value": [1, 2]})
    >>>    return df
    >>>
    >>> # Running slow_computation and saving output to data.parquet
    >>> df = slow_computation()
    >>>
    >>> # Reading data.parquet
    >>> df = slow_computation()
    >>>
    >>> # Adding a full line comments
    >>> def slow_computation():
    >>>    # some long computation
    >>>    # very informative documentation
    >>>    df = pd.DataFrame({"value": [1, 2]})
    >>>    return df
    >>>
    >>> # Reading data.parquet
    >>> df = slow_computation()
    >>>
    >>> # Changing the source code
    >>> def slow_computation():
    >>>    # some long computation
    >>>    # very informative documentation
    >>>    df = pd.DataFrame({"value": [1, 100]})
    >>>    return df
    >>>
    >>> # Source code changed, rerunning slow_computation
    >>> df = slow_computation()

    Parameters
    ----------
    filename: str
        Full path of the filename to save the DataFrame in as a parquet file.

    Returns
    -------
    pandas DataFrame
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # pathlib is great
            data_file = pathlib.Path(filename)

            # get source code of decorated function
            source_code = inspect.getsource(func)

            # remove full line comments
            source_code = "\n".join(
                [
                    line
                    for line in source_code.splitlines()
                    if not re.match(r"^\s*#", line)
                ]
            )

            # remove excess indentation (tabs or spaces) if any
            source_code = textwrap.dedent(source_code)

            # normalize function formatting
            source_code = black.format_str(source_code, mode=black.Mode())

            # hashed source code
            hashed_code = hashlib.sha256(source_code.encode()).hexdigest()

            # save hash in a hidden folder
            hash_path = pathlib.Path(".decoration").resolve()
            if not hash_path.is_dir():
                hash_path.mkdir()

            # hashed source code filename
            hash_file = hash_path / f"{data_file.name.split('.')[0]}.hash"

            # output exists and hash is the same
            if (
                data_file.is_file()
                and hash_file.is_file()
                and (hashed_code == hash_file.read_text())
            ):
                logging.info(f"Reading {filename}")
                data = pd.read_parquet(data_file)

            else:
                # hash is not the same
                if hash_file.is_file() and (hashed_code != hash_file.read_text()):
                    logging.warning(f"Source code of {func.__name__} has changed.")
                logging.info(
                    f"Running {func.__name__} and saving output to {data_file.name}"
                )
                data = func(*args, **kwargs)
                data.to_parquet(data_file, compression="snappy")

            hash_file.write_text(hashed_code)

            return data

        return wrapper

    return decorator
