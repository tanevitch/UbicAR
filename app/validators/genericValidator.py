import re
from typing import List

from app.models.role import Role
def check_email(email):
    if (not re.search('^(?=^.{1,100}$)^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$', email)):
        return 'El mail no tiene un formato válido'

def check_empty_fields(args: List[str]):
    if "" in args or None in args:
        return "Todos los campos son requeridos"

def check_only_letters(word): 
    if (not re.search("^[a-zA-ZÀ-ÿ\s]{1,100}$", word)):
        return 'El campo debe contener solamente letras, entre 1 y 100 caracteres'

def check_limit_100_chars(word): #porque en la BD se definió 100 para todo
    if (not re.search("^(.{1,100})$", word)):
        return 'El campo debe tener entre 1 y 100 caracteres'

def check_limit_500_chars(word): #porque en la BD se definió 100 para todo
    if (not re.search("^(.{1,500})$", word)):
        return 'El campo no puede superar los 500 caracteres'

def check_phone(phone):
    if (not re.search('^(?:(?:00)?549?)?0?(?:11|[2368]\d)(?:(?=\d{0,2}15)\d{2})??\d{8,10}$', phone)):
        return "El teléfono debe ser ingresado solo de manera numérica"

    
def check_coords(coords):
    if (not re.search('^[[][-]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)[\]]$', coords)):
        return "Coordenadas inválidas"
        
def check_polycoords(coords):
    
    if (not re.search('^([[][-]?([1-8]?\d(.\d+)?|90(.0+)?),\s*[-]?(180(.0+)?|((1[0-7]\d)|([1-9]?\d))(.\d+)?)[]],)+[[][-]?([1-8]?\d(.\d+)?|90(.0+)?),\s*[-]?(180(.0+)?|((1[0-7]\d)|([1-9]?\d))(.\d+)?)[]]$',coords)):
        return "Coordenadas inválidas"
    #if (not re.search('^([[][-]?([1-8]?\d(.\d+)?|90(.0+)?),\s*[-+]?(180(.0+)?|((1[0-7]\d)|([1-9]?\d))(.\d+)?)[]](?:,|$))+(?<!,)$',coords)):

def check_alphanumeric(text):
    if not re.search('^[\w\-\s]+$', text):
        return "El campo solo puede contener letras, numeros y los simbolos '-' y '_'"

def check_hex_color(color):
    if not re.search('^#[0-9A-Fa-f]{6}$',color):
        return "El campo color tiene un hexadecimal inválido"


def check_role(role):
    rol = Role.find_by_name(role)
    if not rol:
        return False
    return rol