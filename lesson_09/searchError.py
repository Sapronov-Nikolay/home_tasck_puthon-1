from sqlalchemy import create_engine, text

db_string = "postgresql://myuser:mypassword@localhost:5432/mydatabase"

# Проверка соединения
try:
    engine = create_engine(db_string)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connect good")
except Exception as e:
    print("Error:", e)