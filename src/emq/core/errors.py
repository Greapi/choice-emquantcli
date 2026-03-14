from __future__ import annotations


class EmqCliError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: int | str = "EMQ_CLI_ERROR",
        source: str = "cli",
        exit_code: int = 1,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.source = source
        self.exit_code = exit_code
