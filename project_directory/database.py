import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Replace with your MySQL username
        password='mithraa@2325',  # Replace with your MySQL password
        database='restaurant_reviews'  # Replace with your database name
    )
