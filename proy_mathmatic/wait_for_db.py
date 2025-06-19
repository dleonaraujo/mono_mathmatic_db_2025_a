import time
import psycopg2
import os

host = os.getenv('DB_HOST', 'db')
port = os.getenv('DB_PORT', '5432')
dbname = os.getenv('DB_NAME', 'mathmatic_db')
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'postgres')

for i in range(30):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("✅ Base de datos disponible")
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"⏳ Esperando la base de datos... ({i+1}/30)")
        time.sleep(2)
else:
    print("❌ Tiempo de espera agotado.")
    exit(1)
