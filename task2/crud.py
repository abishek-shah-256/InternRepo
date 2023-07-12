import config
import psycopg2
import traceback


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
            traceback.print_exc()
        finally:
            if connection is not None:
                connection.close()

    return wrapper


@handle_connection
def create(connection):
    cursor = connection.cursor()
    query = f'''
    create table person (
        id int primary key,
        first_name varchar(100),
        last_name varchar(100),
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
def insert(connection, data_tuple):
    cursor = connection.cursor()
    query = '''INSERT INTO person (id, first_name ,last_name, city) VALUES (%s, %s, %s, %s)'''
    record_to_insert = data_tuple

    try:
        cursor.execute(query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count,"Record inserted successfully into person table")

    except Exception as err:
        print(err)

    finally:
        if connection is not None:
            cursor.close()
            connection.close()
            print("Connection is closed")

@handle_connection
def read(connection):
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
def delete(connection, id):
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
def get_data(connection, id):
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
def update(connection, data):
    cursor = connection.cursor()
    query = '''update person set first_name= %s, last_name= %s , city= %s where id= %s'''

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

    # update('abishessask','sshah','pokh',3)
    while(True):
        print("What operation do you want to perform ? \n1. Create table\n2. Insert data\n3. Read data\n4. Delete data\n5. Update data")
        selection = int(input("Enter the number: "))

        if selection == 1:
            create()

        elif selection == 2:
            input_data = input("Enter the values id, first_name, second_name, city: ")
            values = input_data.split()
            data_tuple = tuple(values)
            insert(data_tuple)

        elif selection == 3:
            data = read()
            print(data)

        elif selection == 4:
            id = int(input("Enter the id to delete: "))
            delete(id)

        elif selection == 5:
            id = int(input("Enter the id to update: "))
            data_before_update = get_data(id)
            print("\ndata in the database: ",data_before_update)

            input_data = input("Enter the values first_name, second_name, city: ")
            values = input_data.split()
            data_tuple = tuple(values)

            final_data = data_tuple + (id,)
            update(final_data)


        else:
            print("Invalid option selected")
            break

        user_input = input("\nDo you want to perform more SQL operation ?(y/n)")
        if user_input.lower() != 'y':
            break

