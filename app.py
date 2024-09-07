from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

load_dotenv()

def process_and_combine_excel_files(excel_files):
    """Processes and combines patient information from the provided Excel files."""
    combined_df = pd.DataFrame()

    for file in excel_files:
        try:
            df = pd.read_excel(file)
        except Exception as e:
            st.write(f"Error reading the Excel file {file.name}: {e}")
            continue

        # Renombrar las columnas basadas en los ítems solicitados
        df = df.rename(columns={
            'nombre_completo_paciente': 'full_name',
            'documento_paciente': 'document',
            'tipo_documento': 'document_type',
            'fecha_nacimiento_paciente': 'birthdate',
            'sexo_paciente': 'patient_sex',
            'celular_paciente': 'phone_number',
            'email': 'email'
        })

        # Filtrar las columnas requeridas
        df = df[['full_name', 'document_type', 'document', 'birthdate', 'patient_sex', 'phone_number', 'email']]
        
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df

def insert_patients_to_db(dataframe):
    """Inserts patient information from the dataframe into the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='patient_db',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        # Preparar la consulta SQL
        insert_query = """
            INSERT INTO patients (full_name, document_type, document, birthdate, patient_sex, phone_number, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Insertar los datos en la base de datos
        for index, row in dataframe.iterrows():
            cursor.execute(insert_query, tuple(row))
        
        # Confirmar la transacción
        connection.commit()
        st.write("Datos insertados correctamente.")

    except Error as e:
        st.write(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

st.title("Upload patients")

uploaded_files = st.file_uploader("Select multiple Excel files", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    # Procesar y combinar los archivos Excel
    combined_df = process_and_combine_excel_files(uploaded_files)
    
    # Mostrar el DataFrame combinado
    st.write("Datos cargados:")
    st.dataframe(combined_df)

    # Botón para insertar datos en la base de datos
    if st.button('Guardar datos en la base de datos'):
        insert_patients_to_db(combined_df)
