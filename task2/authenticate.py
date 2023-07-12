import jwt
import config
import psycopg2
from datetime import datetime, timedelta
import pytz


def generate_token(payload):
    key = "nepal"
    encoded = jwt.encode(payload, key, algorithm="HS256")
    return encoded

def verify_token(token):
    try:
        secret_key = "nepal"
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def handle_connection(func):
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = psycopg2.connect(
                user=config.user,
                password=config.password,
                host=config.host,
                port=config.port
            )
            result = func(connection, *args, **kwargs)
            return result
        except Exception as err:
            print("Error occurred in making connection...")
        finally:
            if connection is not None:
                connection.close()

    return wrapper

@handle_connection
def authenticate(connection):
    first_name = input("Enter the username: ")
    last_name = input("Enter the password: ")

    cursor = connection.cursor()
    query = '''SELECT * from person'''
    try:
        cursor.execute(query)
        records = cursor.fetchall()

        user_exist = [r for r in records if r[1] == str(first_name) and r[2] == str(last_name)]

        user_list = [item for sublist in user_exist for item in sublist]

        if user_exist:

            dt = datetime.now(pytz.utc) + timedelta(seconds=10)
            payload = {'id': user_list[0], 'first_name': user_list[1], 'exp': dt}

            tok = generate_token(payload)

            print("Authentication successful!")
            print("Token:", tok)
            return tok
        else:
            print("firstname or lastname is invalid")


    except Exception as err:
        print(err)

    finally:
        if connection is not None:
            cursor.close()
            connection.close()

# @handle_connection
# def create(connection):
#     cursor = connection.cursor()
#     query = f'''
#     create table person (
#         id int primary key,
#         username varchar(100),
#         password varchar(100),
#         city varchar(100)
#     );
#     '''
#     try:
#         cursor.execute(query)
#         connection.commit()
#         print("table created successfully!")
#
#     except Exception as err:
#         print(err)
#
#     finally:
#         if connection is not None:
#             cursor.close()
#             connection.close()
#
# @handle_connection
# def insert(connection, data_tuple):
#     cursor = connection.cursor()
#     query = '''INSERT INTO person (id, username ,password, city) VALUES (%s, %s, %s, %s)'''
#     record_to_insert = data_tuple
#
#     try:
#         cursor.execute(query, record_to_insert)
#         connection.commit()
#         count = cursor.rowcount
#         print(count,"Record inserted successfully into person table")
#
#     except Exception as err:
#         print(err)
#
#     finally:
#         if connection is not None:
#             cursor.close()
#             connection.close()
#             print("Connection is closed")

@handle_connection
def create(connection, token):

    payload = verify_token(token)
    if not payload:
        print("Token is expired or invalid")
        return

    else:
        print(payload)
        cursor = connection.cursor()
        query = f'''
            create table person (
                id int primary key,
                username varchar(100),
                password varchar(100),
                city varchar(100)
            );
            '''
        try:
            cursor.execute(query)
            connection.commit()
            print("table created successfully!")

        except Exception as err:
            print(err)

        finally:
            if connection is not None:
                cursor.close()
                connection.close()

@handle_connection
def insert(connection, token, data_tuple):
    payload = verify_token(token)
    if not payload:
        print("Token is expired or invalid")
        return

    else:
        cursor = connection.cursor()
        query = '''INSERT INTO person (id, username ,password, city) VALUES (%s, %s, %s, %s)'''
        record_to_insert = data_tuple

        try:
            cursor.execute(query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into person table")

        except Exception as err:
            print(err)

        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                print("Connection is closed")

@handle_connection
def read(connection, token):
    payload = verify_token(token)
    if not payload:
        print("Token is expired or invalid")
        return

    else:
        cursor = connection.cursor()
        query = '''SELECT * from person'''

        try:
            cursor.execute(query)
            records = cursor.fetchall()

            # print(records)
            count = cursor.rowcount
            print(count, "Record read successfully from the person table")
            return records


        except Exception as err:
            print(err)

        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                print("Connection is closed")

@handle_connection
def delete(connection, token, id):
    payload = verify_token(token)
    if not payload:
        print("Token is expired or invalid")
        return

    else:
        cursor = connection.cursor()
        query = '''DELETE from person where id = %s'''

        try:
            cursor.execute(query, (id,))
            connection.commit()

            count = cursor.rowcount
            print(count, "Record deleted successfully from the person table")

        except Exception as err:
            print(err)

        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                print("Connection is closed")

@handle_connection
def get_data(connection, token, id):
    payload = verify_token(token)
    if not payload:
        print("Token is expired or invalid")
        return

    else:
        cursor = connection.cursor()
        query = f'''SELECT * from person where id= {id}'''

        try:
            cursor.execute(query)
            record = cursor.fetchone()

            # print(records)
            count = cursor.rowcount
            print(count, "Record read successfully from the person table")
            return record


        except Exception as err:
            print(err)

        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                print("Connection is closed")

@handle_connection
def update(connection, token, data):
    payload = verify_token(token)
    if not payload:
        print("Token is expired or invalid")
        return

    else:
        cursor = connection.cursor()
        query = '''update person set username= %s, password= %s , city= %s where id= %s'''

        try:
            cursor.execute(query, data)
            connection.commit()

            count = cursor.rowcount
            print(count, "Record updated successfully into the person table")

        except Exception as err:
            print(err)

        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                print("Connection is closed")


if __name__ == '__main__':

    token = authenticate()

    # create()
    # input_data = input("Enter the values: (id, username, password, city): ")
    # values = input_data.split()
    # data_tuple = tuple(values)
    # insert(data_tuple)

    if not token:
        print("Authentication required")

    else:
        while (True):
            print("What operation do you want to perform ? \n1. Create table\n2. Insert data\n3. Read data\n4. Delete data\n5. Update data")
            selection = int(input("Enter the number: "))

            if selection == 1:
                create(token)

            elif selection == 2:
                input_data = input("Enter the values id, username, password, city: ")
                values = input_data.split()
                data_tuple = tuple(values)
                insert(token, data_tuple)

            elif selection == 3:
                data = read(token)
                print(data)

            elif selection == 4:
                id = int(input("Enter the id to delete: "))
                delete(token, id)

            elif selection == 5:
                id = int(input("Enter the id to update: "))
                data_before_update = get_data(token, id)
                print("\ndata in the database: ", data_before_update)

                input_data = input("Enter the values username, password, city: ")
                values = input_data.split()
                data_tuple = tuple(values)

                final_data = data_tuple + (id,)
                update(token, final_data)


            else:
                print("Invalid option selected")
                break

            user_input = input("\nDo you want to perform more SQL operation ?(y/n)")
            if user_input.lower() != 'y':
                break
