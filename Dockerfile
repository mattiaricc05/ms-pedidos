FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:8003 --workers 2 --timeout 60 pedidos.wsgi:application"]
```

**requirements.txt**
```
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-decouple==3.8
```

**.env.example**
```
DEBUG=True
SECRET_KEY=your-secret-key-pedidos
DATABASE_URL=postgresql://provesi:provesi123@postgres:5432/db_productos