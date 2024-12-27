import psycopg2

class BankDataBaseHandler:

    def __init__(self, host, database, user, password, port=5432):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = self.connection()

    def connection(self):
        try:
            conn=psycopg2.connect(dbname=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def get_user(self,user_id):
        with self.conn.cursor() as cursor:
            query = "SELECT * FROM bank_app.bank_accounts WHERE user_id = %s"
            cursor.execute(query, (user_id,))            
            result=cursor.fetchall()
            print(result)

    def add_user(self, user_email, amount):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO bank_app.bank_accounts (user_email, amount) VALUES (%s, %s)"
            cursor.execute(query, (user_email, amount))
            self.conn.commit()

    def delete_user(self, user_email):
        with self.conn.cursor() as cursor:
            query = "DELETE FROM bank_app.bank_accounts WHERE user_email = %s"
            cursor.execute(query, (user_email,))
            self.conn.commit()

bdb_handler=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
bdb_handler2=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
# bdb_handler.add_user(user_email="ggg@gmail.com", amount=1500)
# bdb_handler2.add_user(user_email="hhh@gmail.com", amount=890)
bdb_handler.delete_user(user_email="bbb@gmail.com")