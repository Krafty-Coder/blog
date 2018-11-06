from ..dbInit import Database, db_url

class ArticleModel():
    def __init__(self):
        self.db = Database(db_url)
        self.conn = self.db.create_connection()
        self.db.create_tables()
        self.cur = self.conn.cursor()

    def post(self, title, author, body):
        self.title = title
        self.author = author
        self.body = body

    def save(self):
        self.post()
        self.cur.execute(
                "INSERT INTO articles(title, author, body) VALUES(%s, %s, %s);",
                (title,
                 session['username'],
                 body,))
        self.conn.commit()

    def get(self):
        query = "SELECT * FROM articles"
        self.cur.execute(query)
        articles = self.cur.fetchall()
        available_articles = []
        for i in articles:
            articles_list = list(i)
            article = {}
            article["id"] = articles_list[0]
            article["title"] = articles_list[1]
            article["author"] = articles_list[2]
            article["body"] = articles_list[3]
            article["create_date"] = articles_list[4]
            available_articles.append(article)
        return available_articles

    def get_one(self):
        pass

