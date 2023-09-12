
class BaseCustomException(Exception):
    ERROR_MESSAGE = None
    ERROR_CODE = None

    def __init__(self):
        self.error_code = self.ERROR_CODE
        self.error_message = self.ERROR_MESSAGE
        super().__init__()
