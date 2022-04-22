"""
Helpers file to just tidy up main app.py file
"""

def access_db():
    """
    Function to open db
    """
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="postgres",
                                    password="Otelfingen",
                                    host="localhost",
                                    port="5432",
                                    database="test")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        connection.commit()


    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
