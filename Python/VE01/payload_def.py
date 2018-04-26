'''
payload_def.py
Defines basic enums and details required for payloads
'''
import enum

class ParamLocation(enum.Enum):
    '''
    Class DOCSTRING: Enum for parameter inclusion
    '''
    Param_Nowhere = 0
    Param_Body_Json = 1
    Param_Body_Xml = 2
    Param_Body_Form = 4
    Param_Url_Form = 8