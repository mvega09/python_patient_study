from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

load_dotenv()

def process_and_combine_excel_files(excel_files):
    """Processes and combines patient and study information from the provided Excel files."""
    patient_df = pd.DataFrame()
    study_df = pd.DataFrame()

    for file in excel_files:
        try:
            df = pd.read_excel(file)
            if 'nombre_completo_paciente' in df.columns:
                df = df.rename(columns={
                    'nombre_completo_paciente': 'full_name',
                    'documento_paciente': 'document',
                    'tipo_documento': 'document_type',
                    'fecha_nacimiento_paciente': 'birthdate',
                    'sexo_paciente': 'patient_sex',
                    'celular_paciente': 'phone_number',
                    'email': 'email'
                })
                patient_df = pd.concat([patient_df, df[['full_name', 'document_type', 'document', 'birthdate', 'patient_sex', 'phone_number', 'email']]], ignore_index=True)

            elif 'modalidad' in df.columns:
                df = df.rename(columns={
                    'modalidad': 'modality',
                    'estudio': 'study',
                    'fecha_realizado': 'study_carried_out',
                    'valor': 'price',
                    'documento_paciente': 'document'
                })
                
                df['study_carried_out'] = pd.to_datetime(df['study_carried_out'], errors='coerce').dt.strftime('%Y-%m-%d')
                
                study_df = pd.concat([study_df, df[['modality', 'study', 'study_carried_out', 'price', 'document']]], ignore_index=True)

        except Exception as e:
            st.write(f"Error reading the Excel file {file.name}: {e}")
            continue

    # Verificar que los DataFrames tienen datos
    if patient_df.empty:
        st.error("Error: No se encontraron datos de pacientes. Por favor, sube el archivo correcto.")
    if study_df.empty:
        st.error("Error: No se encontraron datos de estudios. Por favor, sube el archivo correcto.")
    
    if patient_df.empty or study_df.empty:
        return None, patient_df, study_df  # Retornar None si falta algún DataFrame

    # Combinar ambos DataFrames basados en los campos 'document'
    combined_df = pd.merge(patient_df, study_df, on='document', how='inner')

    return combined_df, patient_df, study_df

def insert_data_to_db(table_name, dataframe, columns):
    """Inserts data into the specified table in the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        cursor = connection.cursor()

        # Preparar la consulta SQL
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        # Insertar los datos
        data_to_insert = dataframe[columns].to_records(index=False).tolist()
        cursor.executemany(insert_query, data_to_insert)

        connection.commit()

        st.success(f"{cursor.rowcount} rows inserted successfully into {table_name}.")

    except Error as e:
        st.error(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

st.title("Upload patient and study data")

uploaded_files = st.file_uploader("Select multiple Excel files", type=["xls", "xlsx"], accept_multiple_files=True)

if uploaded_files:

    combined_df, patient_df, study_df = process_and_combine_excel_files(uploaded_files)
    
    if patient_df is not None and study_df is not None:
        # Mostrar los DataFrames de pacientes y estudios por separado
        st.write("Datos de pacientes cargados:")
        st.dataframe(patient_df)
        if st.button('Guardar datos de pacientes en la base de datos'):
            insert_data_to_db('patients', patient_df, ['full_name', 'document_type', 'document', 'birthdate', 'patient_sex', 'phone_number', 'email'])
        
        st.write("Datos de estudios cargados:")
        st.dataframe(study_df)
        if st.button('Guardar datos de estudios en la base de datos'):
            insert_data_to_db('studies', study_df, ['modality', 'study', 'study_carried_out', 'price'])
        
        # Mostrar el DataFrame combinado si existe
        if combined_df is not None:
            st.write("Datos combinados de pacientes y estudios:")
            st.dataframe(combined_df)
            if st.button('Guardar datos combinados en la base de datos'):
                insert_data_to_db('patient_study_combined', combined_df)
        else:
            st.write("No se pudo combinar los datos debido a la falta de datos en uno de los archivos.")
