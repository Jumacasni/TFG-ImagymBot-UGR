-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: castinievas.mysql.eu.pythonanywhere-services.com    Database: castinievas$Imagym
-- ------------------------------------------------------
-- Server version	5.7.28-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Actividad_cardio`
--

DROP TABLE IF EXISTS `Actividad_cardio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Actividad_cardio` (
  `id_actividad_cardio` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_actividad_cardio`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Actividad_cardio`
--

LOCK TABLES `Actividad_cardio` WRITE;
/*!40000 ALTER TABLE `Actividad_cardio` DISABLE KEYS */;
INSERT INTO `Actividad_cardio` VALUES (1,'Cinta de correr'),(2,'Elíptica'),(3,'Máquinas escaladoras'),(4,'Bicicleta estática');
/*!40000 ALTER TABLE `Actividad_cardio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Calendario`
--

DROP TABLE IF EXISTS `Calendario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Calendario` (
  `id_calendario` int(11) NOT NULL AUTO_INCREMENT,
  `id_reto` int(11) NOT NULL,
  `dia` int(11) NOT NULL,
  `repeticiones` int(11) NOT NULL,
  PRIMARY KEY (`id_calendario`),
  KEY `id_reto_fk` (`id_reto`),
  CONSTRAINT `id_reto_fk` FOREIGN KEY (`id_reto`) REFERENCES `Retos` (`id_reto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Calendario`
--

LOCK TABLES `Calendario` WRITE;
/*!40000 ALTER TABLE `Calendario` DISABLE KEYS */;
/*!40000 ALTER TABLE `Calendario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cardio_en_gimnasio`
--

DROP TABLE IF EXISTS `Cardio_en_gimnasio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cardio_en_gimnasio` (
  `id_gym` int(11) NOT NULL,
  `id_actividad_cardio` int(11) NOT NULL,
  PRIMARY KEY (`id_gym`,`id_actividad_cardio`),
  KEY `id_actividad_cardio` (`id_actividad_cardio`),
  CONSTRAINT `Cardio_en_gimnasio_ibfk_1` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  CONSTRAINT `Cardio_en_gimnasio_ibfk_2` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cardio_en_gimnasio`
--

LOCK TABLES `Cardio_en_gimnasio` WRITE;
/*!40000 ALTER TABLE `Cardio_en_gimnasio` DISABLE KEYS */;
INSERT INTO `Cardio_en_gimnasio` VALUES (1,1),(1,2),(1,4);
/*!40000 ALTER TABLE `Cardio_en_gimnasio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ejercicio_del_mes`
--

DROP TABLE IF EXISTS `Ejercicio_del_mes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ejercicio_del_mes` (
  `id_objetivo_mensual` int(11) NOT NULL AUTO_INCREMENT,
  `objetivo` varchar(50) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `date_add` date NOT NULL,
  `id_trainer` int(11) NOT NULL,
  `id_actividad_cardio` int(11) NOT NULL,
  PRIMARY KEY (`id_objetivo_mensual`),
  KEY `id_trainer_fk` (`id_trainer`),
  KEY `id_actividad_cardio_fk` (`id_actividad_cardio`),
  CONSTRAINT `id_actividad_cardio_fk` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  CONSTRAINT `id_trainer_fk` FOREIGN KEY (`id_trainer`) REFERENCES `Trainers` (`id_trainer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ejercicio_del_mes`
--

LOCK TABLES `Ejercicio_del_mes` WRITE;
/*!40000 ALTER TABLE `Ejercicio_del_mes` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ejercicio_del_mes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ejercicios`
--

DROP TABLE IF EXISTS `Ejercicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ejercicios` (
  `id_ejercicio` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  PRIMARY KEY (`id_ejercicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ejercicios`
--

LOCK TABLES `Ejercicios` WRITE;
/*!40000 ALTER TABLE `Ejercicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ejercicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ejercita`
--

DROP TABLE IF EXISTS `Ejercita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ejercita` (
  `id_ejercicio` int(11) NOT NULL,
  `id_musculo` int(11) NOT NULL,
  PRIMARY KEY (`id_ejercicio`,`id_musculo`),
  KEY `id_musculo_fk` (`id_musculo`),
  CONSTRAINT `id_ejercicio_fk` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`),
  CONSTRAINT `id_musculo_fk` FOREIGN KEY (`id_musculo`) REFERENCES `Musculos` (`id_musculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ejercita`
--

LOCK TABLES `Ejercita` WRITE;
/*!40000 ALTER TABLE `Ejercita` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ejercita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Gimnasios`
--

DROP TABLE IF EXISTS `Gimnasios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Gimnasios` (
  `id_gym` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `cif` varchar(9) DEFAULT NULL,
  `telefono` int(11) DEFAULT NULL,
  `clave_admin` varchar(20) NOT NULL,
  `clave_clientes` varchar(20) NOT NULL,
  `caducidad_clave_clientes` date NOT NULL,
  PRIMARY KEY (`id_gym`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Gimnasios`
--

LOCK TABLES `Gimnasios` WRITE;
/*!40000 ALTER TABLE `Gimnasios` DISABLE KEYS */;
INSERT INTO `Gimnasios` VALUES (1,'Gimnasio Kronos',NULL,NULL,'admin','clientes','2021-03-04');
/*!40000 ALTER TABLE `Gimnasios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Hace_rutina`
--

DROP TABLE IF EXISTS `Hace_rutina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Hace_rutina` (
  `id_usuario` varchar(20) NOT NULL,
  `id_rutina` int(11) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`id_usuario`,`id_rutina`,`fecha`),
  KEY `id_rutina` (`id_rutina`),
  CONSTRAINT `Hace_rutina_ibfk_1` FOREIGN KEY (`id_rutina`) REFERENCES `Rutinas` (`id_rutina`),
  CONSTRAINT `Hace_rutina_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Hace_rutina`
--

LOCK TABLES `Hace_rutina` WRITE;
/*!40000 ALTER TABLE `Hace_rutina` DISABLE KEYS */;
/*!40000 ALTER TABLE `Hace_rutina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Musculos`
--

DROP TABLE IF EXISTS `Musculos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Musculos` (
  `id_musculo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id_musculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Musculos`
--

LOCK TABLES `Musculos` WRITE;
/*!40000 ALTER TABLE `Musculos` DISABLE KEYS */;
/*!40000 ALTER TABLE `Musculos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Objetivo_personal_cardio`
--

DROP TABLE IF EXISTS `Objetivo_personal_cardio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Objetivo_personal_cardio` (
  `id_objetivo_personal` int(11) NOT NULL AUTO_INCREMENT,
  `objetivo` varchar(50) DEFAULT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` varchar(1) NOT NULL,
  `date_add` date NOT NULL,
  `id_usuario` varchar(20) NOT NULL,
  `id_actividad_cardio` int(11) NOT NULL,
  PRIMARY KEY (`id_objetivo_personal`),
  KEY `id_actividad_cardio` (`id_actividad_cardio`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `Objetivo_personal_cardio_ibfk_1` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  CONSTRAINT `Objetivo_personal_cardio_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Objetivo_personal_cardio`
--

LOCK TABLES `Objetivo_personal_cardio` WRITE;
/*!40000 ALTER TABLE `Objetivo_personal_cardio` DISABLE KEYS */;
INSERT INTO `Objetivo_personal_cardio` VALUES (7,'20.0 distancia','2020-06-09','2020-07-09','C','2020-06-09','Eybra',2);
/*!40000 ALTER TABLE `Objetivo_personal_cardio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Objetivo_peso`
--

DROP TABLE IF EXISTS `Objetivo_peso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Objetivo_peso` (
  `id_objetivo_peso` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` varchar(7) NOT NULL,
  `objetivo` decimal(10,3) NOT NULL,
  `diferencia` decimal(10,3) DEFAULT NULL,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `date_add` date NOT NULL,
  `id_usuario` varchar(20) NOT NULL,
  PRIMARY KEY (`id_objetivo_peso`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `Objetivo_peso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Objetivo_peso`
--

LOCK TABLES `Objetivo_peso` WRITE;
/*!40000 ALTER TABLE `Objetivo_peso` DISABLE KEYS */;
INSERT INTO `Objetivo_peso` VALUES (17,'peso',67.000,-6.000,'2020-06-06','2020-09-06','2020-06-06','lulivi'),(18,'peso',60.000,-1.000,'2020-06-06','2020-07-06','2020-06-06','PugnaireB'),(19,'peso',74.000,-9.000,'2020-06-07','2020-09-07','2020-06-07','Eybra'),(20,'peso',65.000,-25.000,'2020-06-07','2020-12-07','2020-06-07','Noa250'),(22,'peso',49.000,-1.000,'2020-06-07','2020-08-07','2020-06-07','Monetillo'),(23,'peso',55.000,-9.000,'2020-06-09','2020-09-09','2020-06-09','Crisoc'),(24,'peso',56.000,-2.000,'2020-06-10','2020-07-10','2020-06-10','rosanamontes');
/*!40000 ALTER TABLE `Objetivo_peso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Peso`
--

DROP TABLE IF EXISTS `Peso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Peso` (
  `id_peso` int(11) NOT NULL AUTO_INCREMENT,
  `peso` decimal(10,3) DEFAULT NULL,
  `grasa` decimal(10,3) DEFAULT NULL,
  `musculo` decimal(10,3) DEFAULT NULL,
  `IMC` decimal(10,3) DEFAULT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `id_usuario` varchar(20) NOT NULL,
  PRIMARY KEY (`id_peso`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `Peso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Peso`
--

LOCK TABLES `Peso` WRITE;
/*!40000 ALTER TABLE `Peso` DISABLE KEYS */;
INSERT INTO `Peso` VALUES (6,93.400,NULL,20.000,26.040,'2020-06-04','10:32:45','Jumacasni'),(7,94.000,NULL,NULL,26.040,'2020-06-05','10:32:45','Jumacasni'),(8,88.000,16.600,NULL,24.120,'2020-06-06','12:06:34','Jumacasni'),(9,73.000,NULL,NULL,25.260,'2020-06-06','18:19:09','lulivi'),(10,61.000,NULL,NULL,20.620,'2020-06-06','21:31:56','PugnaireB'),(11,83.000,NULL,NULL,26.790,'2020-06-07','08:24:45','Eybra'),(12,89.600,14.500,NULL,24.560,'2020-06-07','10:37:15','Jumacasni'),(13,102.000,NULL,NULL,31.480,'2020-06-07','10:44:54','Danielbroxlr'),(14,90.000,NULL,NULL,NULL,'2020-06-07','11:21:49','Noa250'),(15,94.000,NULL,NULL,25.500,'2020-06-07','15:20:05','Fran_Gr92'),(16,50.000,NULL,NULL,20.280,'2020-06-07','16:55:29','Monetillo'),(17,64.000,NULL,NULL,23.510,'2020-06-07','23:30:39','Crisoc'),(18,58.000,33.000,29.000,NULL,'2020-06-10','08:55:46','rosanamontes');
/*!40000 ALTER TABLE `Peso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Realiza_reto`
--

DROP TABLE IF EXISTS `Realiza_reto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Realiza_reto` (
  `id_usuario` varchar(20) NOT NULL,
  `id_calendario` int(11) NOT NULL,
  `repeticiones` int(11) NOT NULL,
  PRIMARY KEY (`id_usuario`,`id_calendario`),
  KEY `id_calendario` (`id_calendario`),
  CONSTRAINT `Realiza_reto_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`),
  CONSTRAINT `Realiza_reto_ibfk_2` FOREIGN KEY (`id_calendario`) REFERENCES `Calendario` (`id_calendario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Realiza_reto`
--

LOCK TABLES `Realiza_reto` WRITE;
/*!40000 ALTER TABLE `Realiza_reto` DISABLE KEYS */;
/*!40000 ALTER TABLE `Realiza_reto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Registra_cardio`
--

DROP TABLE IF EXISTS `Registra_cardio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Registra_cardio` (
  `id_actividad_cardio` int(11) NOT NULL,
  `id_usuario` varchar(20) NOT NULL,
  `fecha` datetime NOT NULL,
  `tiempo` int(11) DEFAULT NULL,
  `distancia` decimal(10,3) DEFAULT NULL,
  `nivel` int(11) DEFAULT NULL,
  `calorias` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_actividad_cardio`,`id_usuario`,`fecha`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `Registra_cardio_ibfk_1` FOREIGN KEY (`id_actividad_cardio`) REFERENCES `Actividad_cardio` (`id_actividad_cardio`),
  CONSTRAINT `Registra_cardio_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Registra_cardio`
--

LOCK TABLES `Registra_cardio` WRITE;
/*!40000 ALTER TABLE `Registra_cardio` DISABLE KEYS */;
INSERT INTO `Registra_cardio` VALUES (2,'Eybra','2020-06-09 13:05:33',NULL,10.000,NULL,NULL),(2,'Eybra','2020-06-09 13:08:28',NULL,10.000,NULL,NULL);
/*!40000 ALTER TABLE `Registra_cardio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Retos`
--

DROP TABLE IF EXISTS `Retos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Retos` (
  `id_reto` int(11) NOT NULL AUTO_INCREMENT,
  `nivel` int(11) NOT NULL,
  `date_add` date NOT NULL,
  `id_trainer` int(11) NOT NULL,
  `id_ejercicio` int(11) NOT NULL,
  PRIMARY KEY (`id_reto`),
  KEY `id_ejercicio` (`id_ejercicio`),
  KEY `id_trainer` (`id_trainer`),
  CONSTRAINT `Retos_ibfk_1` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`),
  CONSTRAINT `Retos_ibfk_2` FOREIGN KEY (`id_trainer`) REFERENCES `Trainers` (`id_trainer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Retos`
--

LOCK TABLES `Retos` WRITE;
/*!40000 ALTER TABLE `Retos` DISABLE KEYS */;
/*!40000 ALTER TABLE `Retos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rutinas`
--

DROP TABLE IF EXISTS `Rutinas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Rutinas` (
  `id_rutina` int(11) NOT NULL AUTO_INCREMENT,
  `date_add` date NOT NULL,
  `id_trainer` int(11) NOT NULL,
  PRIMARY KEY (`id_rutina`),
  KEY `id_trainer` (`id_trainer`),
  CONSTRAINT `Rutinas_ibfk_1` FOREIGN KEY (`id_trainer`) REFERENCES `Trainers` (`id_trainer`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rutinas`
--

LOCK TABLES `Rutinas` WRITE;
/*!40000 ALTER TABLE `Rutinas` DISABLE KEYS */;
/*!40000 ALTER TABLE `Rutinas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rutinas_ejercicios`
--

DROP TABLE IF EXISTS `Rutinas_ejercicios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Rutinas_ejercicios` (
  `id_rutina` int(11) NOT NULL,
  `id_ejercicio` int(11) NOT NULL,
  PRIMARY KEY (`id_rutina`,`id_ejercicio`),
  KEY `id_ejercicio` (`id_ejercicio`),
  CONSTRAINT `Rutinas_ejercicios_ibfk_1` FOREIGN KEY (`id_ejercicio`) REFERENCES `Ejercicios` (`id_ejercicio`),
  CONSTRAINT `Rutinas_ejercicios_ibfk_2` FOREIGN KEY (`id_rutina`) REFERENCES `Rutinas` (`id_rutina`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rutinas_ejercicios`
--

LOCK TABLES `Rutinas_ejercicios` WRITE;
/*!40000 ALTER TABLE `Rutinas_ejercicios` DISABLE KEYS */;
/*!40000 ALTER TABLE `Rutinas_ejercicios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Se_apunta`
--

DROP TABLE IF EXISTS `Se_apunta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Se_apunta` (
  `id_usuario` varchar(20) NOT NULL,
  `id_objetivo_mensual` int(11) NOT NULL,
  PRIMARY KEY (`id_usuario`,`id_objetivo_mensual`),
  UNIQUE KEY `id_usuario` (`id_usuario`,`id_objetivo_mensual`),
  KEY `id_objetivo_mensual` (`id_objetivo_mensual`),
  CONSTRAINT `Se_apunta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuarios` (`id_usuario`),
  CONSTRAINT `Se_apunta_ibfk_2` FOREIGN KEY (`id_objetivo_mensual`) REFERENCES `Ejercicio_del_mes` (`id_objetivo_mensual`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Se_apunta`
--

LOCK TABLES `Se_apunta` WRITE;
/*!40000 ALTER TABLE `Se_apunta` DISABLE KEYS */;
/*!40000 ALTER TABLE `Se_apunta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Trainers`
--

DROP TABLE IF EXISTS `Trainers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Trainers` (
  `id_trainer` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(50) NOT NULL,
  `DNI` varchar(9) NOT NULL,
  `id_gym` int(11) NOT NULL,
  PRIMARY KEY (`id_trainer`),
  KEY `id_gym` (`id_gym`),
  CONSTRAINT `Trainers_ibfk_1` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Trainers`
--

LOCK TABLES `Trainers` WRITE;
/*!40000 ALTER TABLE `Trainers` DISABLE KEYS */;
/*!40000 ALTER TABLE `Trainers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ubicaciones`
--

DROP TABLE IF EXISTS `Ubicaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ubicaciones` (
  `id_ubicacion` int(50) NOT NULL AUTO_INCREMENT,
  `direccion` varchar(50) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `provincia` varchar(50) NOT NULL,
  `codigo_postal` int(11) NOT NULL,
  `id_gym` int(11) NOT NULL,
  PRIMARY KEY (`id_ubicacion`),
  KEY `id_gym` (`id_gym`),
  CONSTRAINT `Ubicaciones_ibfk_1` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ubicaciones`
--

LOCK TABLES `Ubicaciones` WRITE;
/*!40000 ALTER TABLE `Ubicaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `Ubicaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuarios`
--

DROP TABLE IF EXISTS `Usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuarios` (
  `id_usuario` varchar(20) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `chat_id` varchar(50) NOT NULL,
  `clave_web` varchar(20) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `altura` int(11) DEFAULT NULL,
  `genero` varchar(1) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `date_add` date NOT NULL,
  `id_gym` int(11) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  KEY `id_gym` (`id_gym`),
  CONSTRAINT `Usuarios_ibfk_1` FOREIGN KEY (`id_gym`) REFERENCES `Gimnasios` (`id_gym`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuarios`
--

LOCK TABLES `Usuarios` WRITE;
/*!40000 ALTER TABLE `Usuarios` DISABLE KEYS */;
INSERT INTO `Usuarios` VALUES ('angelrh7','Angel',NULL,'511461469','ZVg4YdKqDR',NULL,NULL,'v',NULL,'2020-06-06',1),('Crisma_17','Cristina','Serrano','831341852','xTzgLDTJSf',NULL,NULL,NULL,NULL,'2020-06-10',1),('Crisoc','Cris',NULL,'29198455','6L1bqOgUmq',NULL,165,NULL,NULL,'2020-06-07',1),('Danielbroxlr','Daniel','Muñoz Sánchez','181392871','h8B31qwWZw',NULL,180,NULL,NULL,'2020-06-07',1),('Eybra','Abraham',NULL,'7993299','ceVE74dm71','1994-04-02',176,'v','Prueba@prueba.com','2020-06-07',1),('Fran_Gr92','Fran',NULL,'799216442','ZIIChtNjw7',NULL,192,NULL,NULL,'2020-06-07',1),('Jumacasni','Juan Manuel',NULL,'192276362','T7ooNKcque',NULL,191,'v',NULL,'2020-06-04',1),('lulivi','Luvo',NULL,'7719679','DZ2gZDQNdP',NULL,170,NULL,NULL,'2020-06-06',1),('Monetillo','Nazaret :)',NULL,'214197744','iEWbnJt7W0','1997-12-19',157,'m',NULL,'2020-06-06',1),('Noa250','Noa',NULL,'973643877','6hA3qpTgNr','1993-11-23',163,'m','Noeliamolinareina@gmail.com','2020-06-06',1),('PugnaireB','Belén',NULL,'517712138','AN5NJOD8UD',NULL,172,NULL,NULL,'2020-06-06',1),('rosanamontes','Rosana','Montes','367839674','J2m7qyeDiA','1975-04-10',163,'m','rosana@ugr.es','2020-06-10',1);
/*!40000 ALTER TABLE `Usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-11  7:25:43
