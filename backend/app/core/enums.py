from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"
    LAB_TECHNICIAN = "lab_technician"
    PHARMACIST = "pharmacist"
    ACCOUNTANT = "accountant"
    BILLING_OFFICER = "billing_officer"
    RADIOLOGIST = "radiologist"
    SURGEON = "surgeon"
    PHYSIOTHERAPIST = "physiotherapist"
    PATIENT = "patient"

class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"
    UNKNOWN = "Unknown"

class MaritalStatus(str, Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"
    OTHER = "Other"

class PersonType(str, Enum):
    USER = "User"
    PATIENT = "Patient"

class ContactType(str, Enum):
    EMERGENCY = "Emergency"
    GUARDIAN = "Guardian"
    OTHER = "Other"

class AdmissionStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISCHARGED = "DISCHARGED"
    CANCELLED = "CANCELLED"