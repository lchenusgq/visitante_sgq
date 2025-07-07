import psycopg2

# Configura los datos reales de conexión a tu base de datos
conn = psycopg2.connect(
    dbname='personasDB',
    user='postgres',
    password='postgres',
    host='localhost',  # o IP del servidor
    port='5433'         # usualmente 5432
)



try:
    with conn.cursor() as cursor:
        cedula = '838370'  # Usa una cédula real que sabes que existe
        cursor.execute("""
            SELECT nombres::bytea, apellidos::bytea
            FROM ciudadano
            WHERE cedula = %s
        """, [cedula])

        resultado = cursor.fetchone()
        print("✅ Resultado crudo desde la DB:", resultado)

        if resultado:
            nombres = resultado[0].tobytes().decode('latin1')
            apellidos = resultado[1].tobytes().decode('latin1')
            print("🟢 Nombres decodificados:", nombres)
            print("🟢 Apellidos decodificados:", apellidos)
        else:
            print("⚠️ Cédula no encontrada")

except Exception as e:
    print("❌ Error:", e)

finally:
    conn.close()
