from ..dbInit import Database, db_url

class User_Model(Database):

    '''Initializes a new user object'''

    def __init__(self):
        self.db = Database(db_url)
        self.conn = self.db.create_connection()
        self.db.create_tables()
        self.cur = self.conn.cursor()

    def post(self, name=None, email=None, username=None, password=None)
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def save(self):
        self.post()
        self.cur.execute(
            "INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s)", (
                self.name, self.email, self.username, self.password,)
        )
        self.conn.commit()
        self.cur.execute("SELECT id FROM users WHERE email = %s", (self.email,))
        row = self.cur.fetchone()
        self.id = row[0]

    def get(self):
        query = "SELECT * FROM users"
        self.cur.execute(query)
        users = self.cur.fetchall()
        appusers = []
        for i in users:
            users_list = list(i)
            user = {}
            user["id"] = users_list[0]
            user["name"] = users_list[1]
            user["email"] = users_list[2]
            user["username"] = users_list[3]
            user["password"] = users_list[4]
            user["join_date"] = users_list[5]
            appusers.append(user)
        return appusers
