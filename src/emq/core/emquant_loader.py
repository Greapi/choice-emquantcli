from __future__ import annotations

import importlib.util
import platform
from pathlib import Path
from types import ModuleType
from typing import Any

from .config import EMQUANT_PY, LIBS_DIR
from .errors import EmqCliError

_EMQ_MODULE: ModuleType | None = None


def _platform_library_path() -> Path:
    system = platform.system().lower()
    machine = platform.machine().lower()
    is_64 = "64" in machine or machine in {"amd64", "x86_64", "arm64", "aarch64"}

    if "windows" in system:
        return LIBS_DIR / "windows" / ("EmQuantAPI_x64.dll" if is_64 else "EmQuantAPI.dll")
    if "linux" in system:
        return LIBS_DIR / "linux" / ("x64" if is_64 else "x86") / (
            "libEMQuantAPIx64.so" if is_64 else "libEMQuantAPI.so"
        )
    if "darwin" in system or "mac" in system:
        return LIBS_DIR / "mac" / "libEMQuantAPIx64.dylib"
    raise EmqCliError(f"Unsupported platform: {platform.system()}", code="UNSUPPORTED_PLATFORM")


def _load_module() -> ModuleType:
    if not EMQUANT_PY.exists():
        raise EmqCliError(
            f"EmQuantAPI vendor file not found: {EMQUANT_PY}",
            code="EMQUANT_VENDOR_MISSING",
        )

    spec = importlib.util.spec_from_file_location("emq_vendor_emquantapi", EMQUANT_PY)
    if spec is None or spec.loader is None:
        raise EmqCliError("Failed to create EmQuantAPI module spec", code="EMQUANT_IMPORT_ERROR")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    lib_path = _platform_library_path()
    if not lib_path.exists():
        raise EmqCliError(
            f"EmQuantAPI library not found for current platform: {lib_path}",
            code="EMQUANT_LIB_MISSING",
        )

    module.UtilAccess.GetLibraryPath = staticmethod(lambda: str(lib_path))
    return module


def get_emquant_module() -> ModuleType:
    global _EMQ_MODULE
    if _EMQ_MODULE is None:
        _EMQ_MODULE = _load_module()
    return _EMQ_MODULE


def get_emquant_client() -> Any:
    module = get_emquant_module()
    return module.c
