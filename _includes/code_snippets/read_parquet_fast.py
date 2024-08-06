from functools import partial

import pandas as pd
import pyarrow as pa
from tqdm.contrib.concurrent import process_map


def _read_parquet(filename, columns=None):
    """Wrapper to pass to a ProcessPoolExecutor to read parquet files as fast
    as possible. The PyArrow engine (v4.0.0) is faster than the fastparquet
    engine (v0.7.0) as it can read columns in parallel. Explicitly enable
    multithreaded column reading with `use_threads == true`.

    Parameters
    ----------
    filename : str
        Path of the parquet file to read.
    columns : list, default=None
        List of columns to read from the parquet file. If None, reads all columns.

    Returns
    -------
    pandas Dataframe
    """

    return pd.read_parquet(
        filename, columns=columns, engine="pyarrow", use_threads=True
    )


def read_parquet(
    files,
    columns=None,
    n_concurrent_files=8,
    n_concurrent_columns=4,
    show_progress=True,
    ignore_index=True,
    chunksize=None,
):
    """Read a single parquet file or a list of parquet files and return a pandas DataFrame. If `parallel==True`, it's on average 50% faster than `pd.read_parquet(..., engine="fastparquet")`. Limited benchmarks indicate that the default values for `n_concurrent_files` and `n_concurrent_columns` are the fastest combination on a 32 core CPU. `n_concurrent_files` * `n_concurrent_columns` <= the number of available cores.

    Parameters
    ----------
    files : list or str
        String with path or list of strings with paths of the parqiaet file(s) to be read.
    columns : list, default=None
        List of columns to read from the parquet file(s). If None, reads all columns.
    parallel : bool, default=True
        If True, reads both files and columns in parallel. If False, read the files serially while still reading the columns in parallel.
    n_concurrent_files : int, default=8
        Number of files to read in parallel.
    n_concurrent_columns : int, default=4
        Number of columns to read in parallel.
    show_progress : bool, default=True
        If True, shows a tqdm progress bar with the number of files that have already been read.
    ignore_index : bool, default=True
        If True, do not use the index values along the concatenation axis. The resulting axis will be labeled 0, ..., n-1. This is useful if you are concatenating objects where the concatention axis does not have meaningful indexing information.

    Returns
    ------
    pandas DataFrame
    """

    # ensure files is a list when reading a single file
    if isinstance(files, str):
        files = [files]

    # no need for more cpu's then files
    if len(files) < n_concurrent_files:
        n_concurrent_files = len(files)

    # no need for more workers than columns
    if columns:
        if len(columns) < n_concurrent_columns:
            n_concurrent_columns = len(columns)

    # set number of threads used for reading the columns of each parquet files
    pa.set_cpu_count(n_concurrent_columns)

    # read files
    _read_parquet_map = partial(_read_parquet, columns=columns)

    # don't construct a process pool for a single file
    if len(files) == 1:
        df = _read_parquet(files)
    else:
        dfs = process_map(
            _read_parquet_map,
            files,
            max_workers=n_concurrent_files,
            chunksize=chunksize,
            disabled=not show_progress,
        )

        # reduce the list of dataframes to a single dataframe
        df = pd.concat(dfs, ignore_index=ignore_index)

    return df
