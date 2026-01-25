
class PatientException(Exception):
    pass

class InvalidPhoneNumber(PatientException):
    def __init__(self, message: str = "Invalid phone number format."):
        super().__init__(message)

class DuplicatePatient(PatientException):
    def __init__ (self, message: str = "Patient already exists."):
        super().__init__(message)

class PatientNotFound(PatientException):
    def __init__(self, message: str = "Patient not found."):
        super().__init__(message)
