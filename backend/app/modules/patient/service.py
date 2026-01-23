from typing import Dict
from app.modules.patient.schemas import PatientCreate

class PatientService:

    @staticmethod
    def create_patient(patient_data: PatientCreate) -> Dict:

        phone = patient_data.phone_number
        if not phone.isdigit() and len(phone) in (10,12):
            raise ValueError("Invalid phone number format.")
        
        return {
            "id" : 1,
            "first_name": patient_data.first_name,
            "last_name": patient_data.last_name,
            "gender": patient_data.gender,
            "date_of_birth": patient_data.date_of_birth,
            "phone_number": patient_data.phone_number,
            "email": patient_data.email,
            "address": patient_data.address
        }

    