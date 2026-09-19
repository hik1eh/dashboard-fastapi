from fastapi import HTTPException, status

class PlanerError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code,
            detail=detail
        )
        
class ItemNotFound(PlanerError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Выбранная запись не найдена'
        )

class UnknowItemKind(PlanerError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='Неизвестная запись'
        )

class InvalidGoalProgress(PlanerError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=''
        )