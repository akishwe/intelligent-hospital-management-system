
class PatientException(Exception):
    pass

class InvalidPhoneNumberException(PatientException):
    def __init__(self, message: str = "Invalid phone number format."):
        super().__init__(message)

class DuplicatePatient(PatientException):
    def __init__ (self, message: str = "Patient already exists."):
        super().__init__(message)
