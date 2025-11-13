from src.post import POSTGRES_HOST

pg_db = POSTGRES_HOST()
pg_db.init_db()
pg_db.insert_document("hello")
pg_db.insert_document("world")
result = pg_db.get_documents()
print("Documents in DB:", result)
pg_db.delete_documents()
