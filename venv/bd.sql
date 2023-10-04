CREATE DATABASE  IF NOT EXISTS `cloud` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cloud`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: cloud
-- ------------------------------------------------------
-- Server version	8.0.34-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `imagenes`
--

DROP TABLE IF EXISTS `imagenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagenes` (
  `idImagenes` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `VMs_idRecursos` int DEFAULT NULL,
  PRIMARY KEY (`idImagenes`),
  KEY `fk_Imagenes_VMs1_idx` (`VMs_idRecursos`),
  CONSTRAINT `fk_Imagenes_VMs1` FOREIGN KEY (`VMs_idRecursos`) REFERENCES `vms` (`idRecursos`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagenes`
--

LOCK TABLES `imagenes` WRITE;
/*!40000 ALTER TABLE `imagenes` DISABLE KEYS */;
INSERT INTO `imagenes` VALUES (1,'cirros-image.img',NULL),(2,'imagenPrueba.iso',NULL),(5,'proyecto.py',NULL),(6,'pyvenv.cfg',NULL);
/*!40000 ALTER TABLE `imagenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface`
--

DROP TABLE IF EXISTS `interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interface` (
  `idnombre` varchar(45) NOT NULL,
  `VMs_idRecursos` int NOT NULL,
  PRIMARY KEY (`idnombre`,`VMs_idRecursos`),
  KEY `fk_Interface_VMs1_idx` (`VMs_idRecursos`),
  CONSTRAINT `fk_Interface_VMs1` FOREIGN KEY (`VMs_idRecursos`) REFERENCES `vms` (`idRecursos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface`
--

LOCK TABLES `interface` WRITE;
/*!40000 ALTER TABLE `interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recursos`
--

DROP TABLE IF EXISTS `recursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recursos` (
  `idRecursos` int NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `memoriaAsignada` float DEFAULT NULL,
  `memoriaTotal` float DEFAULT NULL,
  `discoAsignado` float DEFAULT NULL,
  `discoTotal` float DEFAULT NULL,
  `Zonas_idZonas` int NOT NULL,
  PRIMARY KEY (`idRecursos`),
  KEY `fk_Recursos_Zonas1_idx` (`Zonas_idZonas`),
  CONSTRAINT `fk_Recursos_Zonas1` FOREIGN KEY (`Zonas_idZonas`) REFERENCES `zonas` (`idZonas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recursos`
--

LOCK TABLES `recursos` WRITE;
/*!40000 ALTER TABLE `recursos` DISABLE KEYS */;
/*!40000 ALTER TABLE `recursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `idRoles` int NOT NULL,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`idRoles`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Operador'),(2,'Usuario');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `slice`
--

DROP TABLE IF EXISTS `slice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `slice` (
  `idSlice` int NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `Tipo_idTipo` int NOT NULL,
  `Usuario_idUsuario` int NOT NULL,
  `Zonas_idZonas` int NOT NULL,
  PRIMARY KEY (`idSlice`),
  KEY `fk_Slice_Tipo_idx` (`Tipo_idTipo`),
  KEY `fk_Slice_Usuario1_idx` (`Usuario_idUsuario`),
  KEY `fk_Slice_Zonas1_idx` (`Zonas_idZonas`),
  CONSTRAINT `fk_Slice_Tipo` FOREIGN KEY (`Tipo_idTipo`) REFERENCES `tipo` (`idTipo`),
  CONSTRAINT `fk_Slice_Usuario1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `usuario` (`idUsuario`),
  CONSTRAINT `fk_Slice_Zonas1` FOREIGN KEY (`Zonas_idZonas`) REFERENCES `zonas` (`idZonas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `slice`
--

LOCK TABLES `slice` WRITE;
/*!40000 ALTER TABLE `slice` DISABLE KEYS */;
/*!40000 ALTER TABLE `slice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo`
--

DROP TABLE IF EXISTS `tipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo` (
  `idTipo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`idTipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo`
--

LOCK TABLES `tipo` WRITE;
/*!40000 ALTER TABLE `tipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `passwd` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `flagAZ` tinyint NOT NULL,
  `Roles_idRoles` int NOT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `fk_Usuario_Roles1_idx` (`Roles_idRoles`),
  CONSTRAINT `fk_Usuario_Roles1` FOREIGN KEY (`Roles_idRoles`) REFERENCES `roles` (`idRoles`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'angelo123','99ADC231B045331E514A516B4B7680F588E3823213ABE901738BC3AD67B2F6FCB3C64EFB93D18002588D3CCC1A49EFBAE1CE20CB43DF36B38651F11FA75678E8','a20192258@pucp.edu.pe',0,2),(2,'diego123','99ADC231B045331E514A516B4B7680F588E3823213ABE901738BC3AD67B2F6FCB3C64EFB93D18002588D3CCC1A49EFBAE1CE20CB43DF36B38651F11FA75678E8','a20190459@pucp.edu.pe',0,2),(3,'carlos123','99ADC231B045331E514A516B4B7680F588E3823213ABE901738BC3AD67B2F6FCB3C64EFB93D18002588D3CCC1A49EFBAE1CE20CB43DF36B38651F11FA75678E8','ayala.carlos@pucp.edu.pe',0,2),(4,'admin','c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec','az07.carlos@gmail.com',0,1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vms`
--

DROP TABLE IF EXISTS `vms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vms` (
  `idRecursos` int NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `memoria` float NOT NULL,
  `disco` float NOT NULL,
  `cores` int NOT NULL,
  `interfaces` int NOT NULL,
  `Slice_idSlice` int NOT NULL,
  PRIMARY KEY (`idRecursos`),
  KEY `fk_VMs_Slice1_idx` (`Slice_idSlice`),
  CONSTRAINT `fk_VMs_Slice1` FOREIGN KEY (`Slice_idSlice`) REFERENCES `slice` (`idSlice`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vms`
--

LOCK TABLES `vms` WRITE;
/*!40000 ALTER TABLE `vms` DISABLE KEYS */;
/*!40000 ALTER TABLE `vms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `zonas`
--

DROP TABLE IF EXISTS `zonas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `zonas` (
  `idZonas` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`idZonas`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `zonas`
--

LOCK TABLES `zonas` WRITE;
/*!40000 ALTER TABLE `zonas` DISABLE KEYS */;
/*!40000 ALTER TABLE `zonas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-04 11:22:59
