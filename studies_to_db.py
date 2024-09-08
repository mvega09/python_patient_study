import streamlit as st
import os
import mysql.connector
from mysql.connector import Error

def insert_studies_to_db(dataframe):
    """Inserts study data into the 'studies' table in the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO studies (modality, study, study_carried_out, price)
        VALUES (%s, %s, %s, %s)
        """
        
        data_to_insert = dataframe[['modality', 'study', 'study_carried_out', 'price']].to_records(index=False).tolist()
        cursor.executemany(insert_query, data_to_insert)
        
        connection.commit()
        st.success(f"{cursor.rowcount} rows inserted successfully into studies.")
    
    except Error as e:
        st.error(f"Error: {e}")
        if connection:
            connection.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()