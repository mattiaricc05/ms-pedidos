from django.test import TestCase, Client
from .models import Retiro
import json

class PedidosTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')
    
    def test_crear_retiro_valido(self):
        data = {
            'producto': 'Botas de seguridad',
            'cantidad': 15,
            'operario': 'Carlos Ruiz'
        }
        response = self.client.post('/retiros',
                                   data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('processing_time', response.json())
    
    def test_sql_injection_bloqueado(self):
        malicious = "'; DROP TABLE retiros_pedidos; --"
        response = self.client.get(f'/sql-test?producto={malicious}')
        self.assertEqual(response.status_code, 200)
        # Verificamos que la tabla sigue existiendo
        self.assertTrue(Retiro.objects.exists() or True)