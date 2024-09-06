import os
import streamlit as st
import mysql.connector
from mysql.connector import Error


st.title("Crear Paciente")
full_name = st.text_input('Nombre paciente')
document_type = st.selectbox("Tipo de documento", ["CC", "CE", "TI", "PA", "RC"])
document = st.text_input(label="Documento")
birthdate = st.date_input(label="Fecha de nacimiento")
patient_sex = st.selectbox(label="Sexo", options=["Masculino", "Femenino", "Otro"])
phone_number = st.text_input(label="Numero de celular")
email = st.text_input("Correo electronico")
submit = st.button("Submit")

if submit:
    st.write(f"Nombre paciente es: {full_name}")
    st.write(f"database name: {os.getenv('DB_NAME')}")
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            query = """
            INSERT INTO patients (full_name, document_type, document, birthdate, patient_sex, phone_number, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                full_name,
                document_type,
                document,
                birthdate,
                patient_sex,
                phone_number,
                email
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()

            st.write("El paciente se ha creado con exito")

    except Error as e:
        st.error("Error connecting to database")
        connection = None
