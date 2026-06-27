from fastapi import HTTPException, status

class ExceptionError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

class UnauthorizedError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

class NotFoundError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=msg)

class BadRequestError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)