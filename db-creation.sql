-- Script para crear la base de datos y las tablas necesarias

CREATE DATABASE IF NOT EXISTS patient_db;

USE patient_db;

-- Tabla para almacenar la información del curso
CREATE TABLE IF NOT EXISTS studies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modality VARCHAR(10) NOT NULL,
    study VARCHAR(100) NOT NULL,
    study_carried_out DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);


-- Tabla para almacenar la lista de estudiantes
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    docuemnt_type VARCHAR(20) NOT NULL,
    document VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    patient_sex ENUM('M', 'F') NOT NULL,
    birthday DATE NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(100) NOT NULL
);