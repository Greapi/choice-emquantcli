from __future__ import annotations

import platform

from .errors import EmqCliError

_LINUX_X86_64 = {"x86_64", "amd64"}
_LINUX_X86_32 = {"x86", "i386", "i686"}
_LINUX_ARM64 = {"aarch64", "arm64"}
_WINDOWS_X86_64 = {"x86_64", "amd64"}
_WINDOWS_X86_32 = {"x86", "i386", "i686"}
_MAC_SUPPORTED = {"x86_64", "arm64"}


def _system_machine() -> tuple[str, str]:
    return platform.system().lower(), platform.machine().lower()


def ensure_sdk_runtime_supported() -> None:
    system, machine = _system_machine()

    if system == "linux":
        if machine in _LINUX_ARM64:
            raise EmqCliError(
                "Unsupported architecture: Linux arm64/aarch64. "
                "This package currently ships Linux SDK binaries for x86/x64 only.",
                code="EMQUANT_ARCH_UNSUPPORTED",
                exit_code=2,
            )
        if machine in _LINUX_X86_64 or machine in _LINUX_X86_32:
            return
        raise EmqCliError(
            f"Unsupported Linux architecture: {machine}. "
            "Supported Linux architectures: x86_64, amd64, x86, i386, i686.",
            code="EMQUANT_ARCH_UNSUPPORTED",
            exit_code=2,
        )

    if system == "windows":
        if machine in _WINDOWS_X86_64 or machine in _WINDOWS_X86_32:
            return
        raise EmqCliError(
            f"Unsupported Windows architecture: {machine}. "
            "Supported Windows architectures: x86_64, amd64, x86, i386, i686.",
            code="EMQUANT_ARCH_UNSUPPORTED",
            exit_code=2,
        )

    if system == "darwin":
        if machine in _MAC_SUPPORTED:
            return
        raise EmqCliError(
            f"Unsupported macOS architecture: {machine}. "
            "Supported macOS architectures: x86_64, arm64.",
            code="EMQUANT_ARCH_UNSUPPORTED",
            exit_code=2,
        )

    raise EmqCliError(
        f"Unsupported operating system: {platform.system()}",
        code="EMQUANT_ARCH_UNSUPPORTED",
        exit_code=2,
    )
