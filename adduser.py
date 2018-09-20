from app.models import cur, conn

cur.execute(
    "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
    ("Krafty Coder",
     "kraftycoder@gmail.com",
     "kraftycoder",
     "realestdeveloper"))

conn.commit()
