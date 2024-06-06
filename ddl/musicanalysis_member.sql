-- MySQL dump 10.13  Distrib 8.0.36, for macos14 (arm64)
--
-- Host: localhost    Database: musicanalysis
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `authority` varchar(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `preference_genre` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'ROLE_USER','bb@naver.com','tim','$2a$10$TlLzeFHE3D0M0mC5gfVD/OKvLl0VNzPA/Bx8Z5rv7LWLLD2m64k9S','[Taylor Swift, The Weeknd, Drake, Eminem, Rihanna]'),(2,'ROLE_USER','boun00@naver.com','test','$2a$10$QMyrouX8OVq0lGdaYrq9luY1VmYyT2kt2ftiHjfxzhyN9nxYzQjGO',NULL),(3,'ROLE_USER','qwe@naver.com','qqq','$2a$10$CGAkUuKnw8eY5i7oOT1eEOON4uXzqhlZKW/2aayjysa/bgs278pVG','[Taylor Swift, The Weeknd, Drake, Lana Del Rey, Ed Sheeran]'),(4,'ROLE_USER','yyy@naver.com','yyy','$2a$10$Xfd6xLeeh64JpsOTM/TK0uvyw/v75FkzAIBnfy/jDla7yq0TVWEUm','[Taylor Swift, The Weeknd, Drake, Lana Del Rey, Ed Sheeran]'),(5,'ROLE_USER','test@gmail.com','test','$2a$10$VYSWKwNfJOxNzmQBQ3KnHuNkGOqbrVq4769/3J6bLiddkD2asuf6i','[Taylor Swift, Eminem, Kanye West, Future, Drake, The Weeknd]'),(6,'ROLE_USER','ftest@naver.com','ftest','$2a$10$if8mRH.y1nQtlFx5zDRzV.bti5m3.FZxRA2hu0HG/sl0UAvfax2kS',NULL),(7,'ROLE_USER','cap@naver.com','caps','$2a$10$wGxJ6iVD4P39kXDb58EiO.WCh2PMFSziS2L2pNdVTuGjAeiI97UKq','[The Weeknd, Drake, Kanye West, Ed Sheeran, Rihanna, Future]'),(8,'ROLE_USER','capd@naver.com','be','$2a$10$s8sJLlXD5VT0RoTtlTfzsuHbidDpzHyVKA/ex3pIPbwd/1yWyB8q.','[Eminem, The Weeknd, Drake, Future, Travis Scott, Kanye West]'),(9,'ROLE_USER','caps@naver.com','beoo','$2a$10$vYljt6n034AeI0Gb6viSd.donS6hgLA6kCGjsaaL/aUMQZBix8DX6','[Drake, The Weeknd, Eminem, Kanye West, Future, Travis Scott]'),(10,'ROLE_USER','capdd@gmail.com','beou','$2a$10$KzgElI5d0vvJk2FoA241PeVgkzlkjS2y5NipgSlTcDczaouayN1je','[Lil Wayne, JAY-Z, Eminem, Kanye West, Travis Scott, Drake]');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-06 14:20:07
