from fastapi import HTTPException, status

class ExceptionError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=msg)

class UnAuthorizesError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=msg)

class NotFoundError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=msg)