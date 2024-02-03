class CustomException(Exception):
    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

    def to_json(self):
        return self.message

# Excepciones específicas
class FirebaseStorageError(CustomException):
    pass

class UsuarioVerificationError(CustomException):
    pass

class FaltaDeDatos(CustomException):
    pass

class ErrorCrearPersonaje(CustomException):
    pass

class ErrorEliminarPersonaje(CustomException):
    pass

class ErrorDesconocido(CustomException):
    pass

# Excepciones comunes
class CommonException(CustomException):
    pass

class UserNotFound(CustomException):
    pass