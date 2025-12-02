from django.db import models

class Retiro(models.Model):
    producto = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    operario = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'retiros_pedidos'
    
    def __str__(self):
        return f"{self.producto} - {self.cantidad} - {self.operario}"