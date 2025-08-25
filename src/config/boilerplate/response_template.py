from collections import OrderedDict

from fastapi import status, Response
from fastapi.exceptions import FastAPIError

from boilerplate import logger


class Resp:
    error: str = None
    message: str = None
    data: dict | str | int | bool = None
    status_code: int = None

    def __init__(self, error: str = None, message: str = None, data: dict | str | int | bool | list = None, status_code: int = None) -> None:
        if error:
            self.error = error
        if message:
            self.message = message
        if data:
            self.data = data
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        if self.error:
            logger.warning(self.to_text())

        if (isinstance(self.data, dict) or isinstance(self.data, OrderedDict) ) and not self.error:
            return self.data

        else:
            return {
                "error": self.error,
                "message": self.to_text(),
                "data": self.data
            }

    def to_text(self):
        return f"{self.error.upper()+': ' if self.error else ''}{self.message}"

    def to_response(self):
        return Response(
            self.to_dict(),
            status=self.status_code if self.status_code else status.HTTP_200_OK
        )

    def to_exception(self):
        logger.exception(self.to_text())

        return FastAPIError(
            detail=self.to_text(),
            code=self.error
        )