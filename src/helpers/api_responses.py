from fastapi import HTTPException, status

class APIResponses(Exception):
    switch: dict[int, str] = {
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
        404: "Not Found", 409: "Conflict", 422: "Unprocessable Entity",
        500: "Internal Server Error", 200: "OK", 201: "Created",
        202: "Accepted", 204: "No Content", 304: "Not Modified",
    }

    def __init__(self, status_code: int, message: str = None):
        self.status_code = status_code
        self.message = message or self.switch.get(status_code, "Unknown error")

    def raise_error(self):
        """Lanza una excepción HTTP de FastAPI."""
        raise HTTPException(status_code=self.status_code, detail=self.message)

    def __str__(self):
        return f"{self.status_code} {self.switch.get(self.status_code)}: {self.message}"


# Ejemplos de clases específicas
class DBError(APIResponses):
    def __init__(self, message: str = "Database error occurred"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message)

class ConflictError(APIResponses):
    def __init__(self, message: str = "Conflict occurred"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)

class NotFoundError(APIResponses):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)