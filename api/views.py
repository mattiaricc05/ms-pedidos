import logging
import time
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import Retiro
from .serializers import RetiroSerializer

logger = logging.getLogger(__name__)

@api_view(['GET'])
def health(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'service': 'ms-pedidos',
        'database': 'postgresql'
    })

@api_view(['POST'])
def crear_retiro(request):
    """
    Endpoint para registrar un retiro de inventario.
    ASR: Debe completar en menos de 5 segundos.
    """
    start_time = time.time()
    
    serializer = RetiroSerializer(data=request.data)
    
    if serializer.is_valid():
        retiro = serializer.save()
        elapsed = time.time() - start_time
        
        logger.info(f"Retiro creado en {elapsed:.3f}s - ID: {retiro.id}")
        
        return Response({
            'message': 'Retiro registrado exitosamente',
            'data': serializer.data,
            'processing_time': f"{elapsed:.3f}s"
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def sql_test(request):
    """
    Endpoint para demostrar resistencia a SQL injection.
    El ORM de Django previene inyecciones usando prepared statements.
    """
    malicious_input = request.GET.get('producto', '')
    
    try:
        # El ORM de Django previene SQL injection automáticamente
        # Incluso con inputs maliciosos, el ORM los escapa correctamente
        retiros = Retiro.objects.filter(producto__icontains=malicious_input)[:10]
        
        # Intento adicional: raw query parametrizada (forma segura)
        with connection.cursor() as cursor:
            # Consulta parametrizada - SEGURA
            cursor.execute(
                "SELECT COUNT(*) FROM retiros_pedidos WHERE producto LIKE %s",
                [f"%{malicious_input}%"]
            )
            count_raw = cursor.fetchone()[0]
        
        return Response({
            'message': 'Consulta segura ejecutada',
            'input_received': malicious_input,
            'results_count_orm': retiros.count(),
            'results_count_raw': count_raw,
            'protection': 'ORM Django usa prepared statements. Raw queries parametrizadas también son seguras.',
            'note': 'SQL injection bloqueado al 100% por el ORM y consultas parametrizadas'
        })
        
    except Exception as e:
        logger.error(f"Error en consulta: {str(e)}")
        return Response({
            'message': 'Error controlado',
            'error': str(e),
            'protection': 'Exception handling captura intentos maliciosos'
        }, status=status.HTTP_400_BAD_REQUEST)