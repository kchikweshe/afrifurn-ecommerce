class CartNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        
class UpdateFailedException(Exception):
    def __init__(self, *kwargs: object) -> None:
        super().__init__(*kwargs)