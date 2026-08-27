from typing import Any


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, extra: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.extra = extra or {}

    def to_detail(self) -> dict[str, Any]:
        detail: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.extra:
            detail.update(self.extra)
        return detail


class NotFoundError(AppError):
    def __init__(self, code: str, message: str):
        super().__init__(code=code, message=message, status_code=404)


class ConflictError(AppError):
    def __init__(self, code: str, message: str):
        super().__init__(code=code, message=message, status_code=409)


class PayloadTooLargeError(AppError):
    def __init__(self, message: str = "File exceeds maximum allowed size."):
        super().__init__(code="PAYLOAD_TOO_LARGE", message=message, status_code=413)


class AgentError(AppError):
    def __init__(self, message: str, code: str = "AGENT_ERROR"):
        super().__init__(code=code, message=message, status_code=500)
