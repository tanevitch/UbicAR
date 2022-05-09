from app.validators.genericValidator import check_empty_fields, check_coords
class FZValidator():

    @classmethod
    def check_lenght(cls,colCoords):
        if (len(colCoords)>=3):
            return True
        else:
            return False
    
            
    @classmethod
    def check_coordsList(cls, list):
        '''
        Si alguna esta mal, devuelve msj error. Si todas están bien devuelve none, no hubo error
        
        '''
        for par in list:
            error_c= check_coords(str(par))
            if(error_c):
                return error_c
