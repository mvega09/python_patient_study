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
    full_name VARCHAR(100) NOT NULL,
    document VARCHAR(50) NOT NULL UNIQUE,
    document_type VARCHAR(20) NOT NULL,
    birthdate DATE NOT NULL,
    patient_sex ENUM('M', 'F') NOT NULL,
    phone_number NUMBER(15),
    email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS patient_study_combined (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255),
    document_type VARCHAR(50),
    document VARCHAR(50),
    birthdate DATE,
    patient_sex VARCHAR(10),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    modality VARCHAR(50),
    study VARCHAR(100),
    study_carried_out DATE,
    price DECIMAL(10, 2)
);
