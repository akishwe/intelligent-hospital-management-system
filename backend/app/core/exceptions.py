
class PatientException(Exception):
    pass

class AuthException(Exception):
    pass

class UserAlreadyExists(AuthException):
    def __init__(self, message: str = "User already exists."):
        super().__init__(message)

class InvalidCredentials(AuthException):
    def __init__(self, message: str = "Invalid email or password."):
        super().__init__(message)

class InActiveUser(AuthException):
    def __init__(self, message: str = "User account is inactive."):
        super().__init__(message)

class InvalidPhoneNumber(PatientException):
    def __init__(self, message: str = "Invalid phone number format."):
        super().__init__(message)

class DuplicatePatient(PatientException):
    def __init__ (self, message: str = "Patient already exists."):
        super().__init__(message)

class PatientNotFound(PatientException):
    def __init__(self, message: str = "Patient not found."):
        super().__init__(message)
