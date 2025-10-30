from kedro.framework.hooks import hook_impl
from kedro.io import MemoryDataset
from typing import Dict, Any
from kedro.io import DataCatalog

import contextvars

# Thread-safe context variable to hold runtime datasets
RUNTIME_DATASETS_CTX: contextvars.ContextVar[Dict[str, Any]] = contextvars.ContextVar(
    "runtime_datasets", default={}
)


class RuntimeDatasetHook:
    """Inject in-memory datasets into the catalog after it's created."""

    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog):
        runtime_datasets = RUNTIME_DATASETS_CTX.get()
        if runtime_datasets:
            for name, data in runtime_datasets.items():
                catalog[name] = MemoryDataset(data)
        return catalog
