import psycopg2
from decimal import Decimal
import re

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
            return result
            print(result)

    def add_user(self, user_email: str, amount: Decimal) -> None:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, user_email):        
            raise ValueError(f"Invalid email address: {user_email}")
 
        with self.conn.cursor() as cursor:
            query = "INSERT INTO bank_app.bank_accounts (user_email, amount) VALUES (%s, %s)"
            cursor.execute(query, (user_email, amount))
            self.conn.commit()

    def delete_user(self, user_email: str) -> None : 
        with self.conn.cursor() as cursor:
            query = "DELETE FROM bank_app.bank_accounts WHERE user_email = %s"
            cursor.execute(query, (user_email,))
            self.conn.commit()

    def card_payment(self, user_email: str, amount: Decimal) -> bool:
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

                if current_balance < amount:
                    print(f"Insufficient funds for {user_email}")
                    return False
                
                new_balance = current_balance - amount
                update_query = "UPDATE bank_app.bank_accounts SET amount = %s WHERE user_email = %s"
                cursor.execute(update_query, (new_balance,user_email))
                self.conn.commit()
                print(f"Payment of {amount} processed for {user_email}. New balance: {new_balance}")
                return True
        
        except psycopg2.Error as e:
            print(f"Error processing payment: {e}")
            self.conn.rollback()
            raise
    
    def bank_transfer(self, from_email: str, to_email: str, amount: Decimal) -> bool:
        try:
            with self.conn.cursor() as cursor:
                check_balance_query = "SELECT amount FROM bank_app.bank_accounts WHERE user_email = %s"
                cursor.execute(check_balance_query, (from_email,))
                from_result= cursor.fetchone()

                if not from_result:
                    print(f"User with email {from_email} does not exist")
                    return False
        
                if from_result[0]<amount:
                    print(f"Insufficient funds for sender {from_email}")
                    return False
                
                cursor.execute(check_balance_query,(to_email,))
                to_result = cursor.fetchone()

                if not to_result:
                    print(f"User with email {to_email} does not exist")
                    return False
                
                new_from_balance = from_result[0] - amount
                new_to_balance = to_result[0] + amount

                update_from_query = "UPDATE bank_app.bank_accounts SET amount = %s WHERE user_email = %s"
                update_to_query = "UPDATE bank_app.bank_accounts SET amount = %s WHERE user_email = %s"

                cursor.execute(update_from_query, (new_from_balance, from_email))
                cursor.execute(update_to_query, (new_to_balance, to_email))

                self.conn.commit()
                print(f"Transfer of {amount} from {from_email} to {to_email} completed")
                return True
            
        except psycopg2.Error as e:
            print(f"Error processing transfer: {e}")
            self.conn.rollback()
            raise



                
        




# funckja płacenia kartą, podawanie kwoty do zapłaty i email. Sprawdzic czy sa wysttarczajace srodki, pobrac kwote i zaktualizowac
# wyslac zmiany na GIT i zrobić pull request

# dodac metodę robiącą przelew z jednego konta na drugie i update 
# testy jednostkowe, integracyjne i modeli sql (dbt test)

# bdb_handler=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
# bdb_handler2=BankDataBaseHandler(host="localhost", database="postgres", user="postgres", password="root")
# bdb_handler.add_user(user_email="hhhgmail.com", amount=1500)
# bdb_handler2.add_user(user_email="hhh@gmail.com", amount=890)
# bdb_handler.delete_user(user_email="bbb@gmail.com")
