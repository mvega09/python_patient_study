import streamlit as st
import pandas as pd
from study_db_helper import get_all_the_courses
from patient_db_helper import insert_patienst_in_bulk

st.title("Upload patients")

def extract_patients_from_excel(excel_file, course_id):
    """Extracts patient information from the provided Excel file."""
    try:
        df = pd.read_excel(excel_file)
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []

    # Renombrar las columnas basadas en los ítems solicitados
    df = df.rename(columns={
        'tipo_documento': 'tipo_documento',
        'documento_paciente': 'documento',
        'nombre_completo_paciente': 'nombre_completo',
        'sexo_paciente': 'sexo',
        'fecha_nacimiento_paciente': 'fecha_nacimiento',
        'celular_paciente': 'celular',
        'email': 'email'
    })

    # Filtrar las columnas requeridas
    df = df[['tipo_documento', 'documento', 'nombre_completo', 'sexo', 'fecha_nacimiento', 'celular', 'email']]

    # Insertar los pacientes en la base de datos
    insert_patienst_in_bulk(df, course_id, table_name='patients')
    
    st.write(df)

# Obtener los cursos
courses = get_all_the_courses()

# Crear un diccionario para mapear IDs de cursos a sus nombres
course_dict = {course['id']: course['name'] for course in courses}
course_ids = list(course_dict.keys())

# Crear el dropdown con los IDs como valor de selección y los nombres como valor de visualización
selected_course_id = st.selectbox("Select a course", course_ids, format_func=lambda id: course_dict[id])

# Subir el archivo de Excel
uploaded_file = st.file_uploader("Upload patient data Excel file", type=["xls", "xlsx"])

# Botón para procesar la carga y mostrar los valores
if st.button("Save patients"):
    if uploaded_file is not None:
        extract_patients_from_excel(uploaded_file, selected_course_id)
        st.write("Patients have been uploaded successfully")
