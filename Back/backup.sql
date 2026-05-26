-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: cv_generator
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `certificacion`
--

DROP TABLE IF EXISTS `certificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificacion` (
  `id_certificacion` int unsigned NOT NULL AUTO_INCREMENT,
  `id_cv` int unsigned NOT NULL,
  `certificacion` varchar(255) NOT NULL,
  `expedicion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_certificacion`),
  KEY `fk_cert_cv` (`id_cv`),
  CONSTRAINT `fk_cert_cv` FOREIGN KEY (`id_cv`) REFERENCES `curriculum` (`id_cv`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificacion`
--

LOCK TABLES `certificacion` WRITE;
/*!40000 ALTER TABLE `certificacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `certificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curriculum`
--

DROP TABLE IF EXISTS `curriculum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curriculum` (
  `id_cv` int unsigned NOT NULL AUTO_INCREMENT,
  `id_usuario` int unsigned NOT NULL,
  `id_oferta` int unsigned DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `hash_control` varchar(64) DEFAULT NULL,
  `tiene_foto` tinyint(1) NOT NULL DEFAULT '0',
  `plantilla` varchar(100) NOT NULL,
  PRIMARY KEY (`id_cv`),
  KEY `fk_cv_usuario` (`id_usuario`),
  KEY `fk_cv_oferta` (`id_oferta`),
  CONSTRAINT `fk_cv_oferta` FOREIGN KEY (`id_oferta`) REFERENCES `oferta_empleo` (`id_oferta`) ON DELETE SET NULL,
  CONSTRAINT `fk_cv_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curriculum`
--

LOCK TABLES `curriculum` WRITE;
/*!40000 ALTER TABLE `curriculum` DISABLE KEYS */;
/*!40000 ALTER TABLE `curriculum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cv_habilidad`
--

DROP TABLE IF EXISTS `cv_habilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cv_habilidad` (
  `id_cv` int unsigned NOT NULL,
  `id_habilidad` int unsigned NOT NULL,
  PRIMARY KEY (`id_cv`,`id_habilidad`),
  KEY `fk_cvh_habilidad` (`id_habilidad`),
  CONSTRAINT `fk_cvh_cv` FOREIGN KEY (`id_cv`) REFERENCES `curriculum` (`id_cv`) ON DELETE CASCADE,
  CONSTRAINT `fk_cvh_habilidad` FOREIGN KEY (`id_habilidad`) REFERENCES `habilidad` (`id_habilidad`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cv_habilidad`
--

LOCK TABLES `cv_habilidad` WRITE;
/*!40000 ALTER TABLE `cv_habilidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `cv_habilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_personales`
--

DROP TABLE IF EXISTS `datos_personales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_personales` (
  `id_datos` int unsigned NOT NULL AUTO_INCREMENT,
  `id_cv` int unsigned NOT NULL,
  `nombre` varchar(20) DEFAULT NULL,
  `Apellido` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `localidad` varchar(100) DEFAULT NULL,
  `permiso_conducir` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_datos`),
  UNIQUE KEY `id_cv` (`id_cv`),
  CONSTRAINT `fk_datos_cv` FOREIGN KEY (`id_cv`) REFERENCES `curriculum` (`id_cv`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_personales`
--

LOCK TABLES `datos_personales` WRITE;
/*!40000 ALTER TABLE `datos_personales` DISABLE KEYS */;
/*!40000 ALTER TABLE `datos_personales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `educacion`
--

DROP TABLE IF EXISTS `educacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `educacion` (
  `id_educacion` int unsigned NOT NULL AUTO_INCREMENT,
  `id_cv` int unsigned NOT NULL,
  `institucion` varchar(255) DEFAULT NULL,
  `titulo` varchar(255) DEFAULT NULL,
  `anioInicio` varchar(50) DEFAULT NULL,
  `anioFin` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_educacion`),
  KEY `fk_edu_cv` (`id_cv`),
  CONSTRAINT `fk_edu_cv` FOREIGN KEY (`id_cv`) REFERENCES `curriculum` (`id_cv`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `educacion`
--

LOCK TABLES `educacion` WRITE;
/*!40000 ALTER TABLE `educacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `educacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiencia_laboral`
--

DROP TABLE IF EXISTS `experiencia_laboral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencia_laboral` (
  `id_experiencia` int unsigned NOT NULL AUTO_INCREMENT,
  `id_cv` int unsigned NOT NULL,
  `empresa` varchar(255) NOT NULL,
  `puesto` varchar(255) DEFAULT NULL,
  `fecha_inicio` varchar(50) DEFAULT NULL,
  `fecha_fin` varchar(50) DEFAULT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_experiencia`),
  KEY `fk_exp_cv` (`id_cv`),
  CONSTRAINT `fk_exp_cv` FOREIGN KEY (`id_cv`) REFERENCES `curriculum` (`id_cv`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiencia_laboral`
--

LOCK TABLES `experiencia_laboral` WRITE;
/*!40000 ALTER TABLE `experiencia_laboral` DISABLE KEYS */;
/*!40000 ALTER TABLE `experiencia_laboral` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `habilidad`
--

DROP TABLE IF EXISTS `habilidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `habilidad` (
  `id_habilidad` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  PRIMARY KEY (`id_habilidad`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habilidad`
--

LOCK TABLES `habilidad` WRITE;
/*!40000 ALTER TABLE `habilidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `habilidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idioma`
--

DROP TABLE IF EXISTS `idioma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `idioma` (
  `id_idioma` int unsigned NOT NULL AUTO_INCREMENT,
  `id_cv` int unsigned NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `nivel` enum('BÃ¡sico','Intermedio','Avanzado','Nativo') NOT NULL DEFAULT 'BÃ¡sico',
  PRIMARY KEY (`id_idioma`),
  KEY `fk_idioma_cv` (`id_cv`),
  CONSTRAINT `fk_idioma_cv` FOREIGN KEY (`id_cv`) REFERENCES `curriculum` (`id_cv`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idioma`
--

LOCK TABLES `idioma` WRITE;
/*!40000 ALTER TABLE `idioma` DISABLE KEYS */;
/*!40000 ALTER TABLE `idioma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oferta_empleo`
--

DROP TABLE IF EXISTS `oferta_empleo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oferta_empleo` (
  `id_oferta` int unsigned NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `empresa` varchar(255) NOT NULL,
  `descripcion` text,
  `requisitos` text,
  PRIMARY KEY (`id_oferta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oferta_empleo`
--

LOCK TABLES `oferta_empleo` WRITE;
/*!40000 ALTER TABLE `oferta_empleo` DISABLE KEYS */;
/*!40000 ALTER TABLE `oferta_empleo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(150) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'juan','fernandez','juan1@test.com','$5$rounds=535000$KYNbybHJRPNC0o5X$V62e64BhSQML2ST5T/0e5EOwM9q.eyOdAWgfxPohBD3','2026-05-26 12:22:04');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-26 12:43:35
