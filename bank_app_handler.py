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

    def card_payment(self, user_email, amount):
        try:
            with self.conn.cursor() as cursor:
                query = "SELECT amount FROM bank_app.bank_accounts WHERE user_email = %s"
                cursor.execute(query, (user_email))
                result= cursor.fetchone()

                if not result:
                    print(f"User with email {user_email} does not exist")
                    return False
                
                current_balance=result[0]
                print(f"Current balance for {user_email}: {current_balance}")

                if current_balance<amount:
                    print(f"Insufficient funds for {user_email}")
                    return False
                
                new_balance = current_balance - amount
                update_query = "UPDATE bank_app.bank.accounts SET amount = %s WHERE user_email = %s"
                cursor.execute(update_query, (new_balance,user_email))
                self.conn.commit()
                print(f"Payment of {amount} processed for {user_email}. New balance: {new_balance}")
                return True
        
        except psycopg2.Error as e:
            print(f"Error processing payment: {e}")
            self.conn.rollback()
            raise

# funckja płacenia kartą, podawanie kwoty do zapłaty i email. Sprawdzic czy sa wysttarczajace srodki, pobrac kwote i zaktualizowac
# wyslac zmiany na GIT i zrobić pull request

bdb_handler=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
bdb_handler2=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
# bdb_handler.add_user(user_email="ggg@gmail.com", amount=1500)
# bdb_handler2.add_user(user_email="hhh@gmail.com", amount=890)
bdb_handler.delete_user(user_email="bbb@gmail.com")