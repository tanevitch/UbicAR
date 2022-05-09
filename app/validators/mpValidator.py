import re
from app.models.meeting_point import Meeting_point
from app.validators.genericValidator import check_coords, check_email, check_empty_fields, check_limit_100_chars, check_only_letters, check_phone
class MPValidator():
    
    @classmethod 
    def emptyFields(cls, mp: Meeting_point):
        return check_empty_fields([mp.name, mp.address, mp.mail, mp.coords, mp.phone, mp.visible])

    @classmethod
    def invalidType(cls, mp: Meeting_point):        
        return (
            check_only_letters(mp.name)
            or check_limit_100_chars(mp.address) 
            or check_email(mp.mail)
            or check_phone(mp.phone)
            or check_coords(mp.coords)
        )
