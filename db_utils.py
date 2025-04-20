# db_utils.py
import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="KUjMcLa9iTZrfjU.root",
        password="Fd8vm7Rtr3stcucS",
        database="Stock"
    )

def fetch_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
