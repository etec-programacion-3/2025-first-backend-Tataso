from tortoise.models import Model
from tortoise import fields

class Libro(Model):
    id = fields.IntField(pk=True)
    titulo = fields.CharField(max_length=255)
    autor = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=13, unique=True) #el dni del librito
    categoria = fields.CharField(max_length=100)
    estado = fields.CharField(max_length=50, default="disponible")
    fecha_creacion = fields.DatetimeField(auto_now_add=True)