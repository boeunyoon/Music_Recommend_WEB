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
-- Table structure for table `playlists`
--

DROP TABLE IF EXISTS `playlists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlists` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `member_id` bigint NOT NULL,
  `title` varchar(255) NOT NULL,
  `song_id` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FKibwe1bfgmdinkd4y6b3k8yx8i` (`member_id`),
  CONSTRAINT `FKibwe1bfgmdinkd4y6b3k8yx8i` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=247 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlists`
--

LOCK TABLES `playlists` WRITE;
/*!40000 ALTER TABLE `playlists` DISABLE KEYS */;
INSERT INTO `playlists` VALUES (173,1,'Love Yourself','50kpGaPAhYJ3sGmk6vplg0'),(174,1,'Ghost','6I3mqTwhRpn34SLVafSH7G'),(175,1,'STAY (with Justin Bieber)','5HCyWlXZPP0y6Gqq8TgA20'),(176,1,'Private Landing (feat. Justin Bieber & Future)','52NGJPcLUzQq5w7uv4e5gf'),(177,1,'Set Fire to the Rain','73CMRj62VK8nUS4ezD2wvi'),(178,1,'Rolling in the Deep','1c8gk2PeTE04A1pIDH9YMk'),(179,1,'Someone Like You','1zwMYTA5nlNjZxYrvBB2pV'),(190,5,'Mockingbird','561jH07mF1jHuk7KlaeF0s'),(191,5,'Watch This - ARIZONATEARS Pluggnb Remix','0FA4wrjDJvJTTU8AepZTup'),(192,5,'The Real Slim Shady','3yfqSUWxFvZELEM4PmlwIR'),(193,5,'Without Me','7lQ8MOhq6IN2w8EYcFNSUk'),(194,5,'Rich Flex','1bDbXMyjaUIooNwFE9wn0N'),(195,5,'Passionfruit','5mCPDVBb16L4XQwDdbRUpz'),(196,5,'First Class','0wHFktze2PHC5jDt3B17DC'),(197,5,'INDUSTRY BABY (feat. Jack Harlow)','27NovPIUIRrOZoCHxABJwK'),(212,8,'Superman','4woTEX1wYOTGDqNXuavlRC'),(213,8,'Till I Collapse','4xkOaSrkexMciUUogZKVTS'),(214,8,'First Class','0wHFktze2PHC5jDt3B17DC'),(215,8,'INDUSTRY BABY (feat. Jack Harlow)','27NovPIUIRrOZoCHxABJwK'),(216,8,'WHATS POPPIN','1jaTQ3nqY3oAAYyCTbIvnM'),(217,8,'Die For You - Remix','7oDd86yk8itslrA9HRP2ki'),(218,8,'Starboy','7MXVkk9YMctZqd1Srtv4MB'),(219,8,'Blinding Lights','0VjIjW4GlUZAMYd2vXMi3b'),(220,8,'Love On The Brain','5oO3drDxtziYU2H1X23ZIp'),(221,8,'We Found Love','6qn9YLKt13AGvpq9jfO8py'),(222,8,'Still D.R.E.','503OTo2dSqe7qk76rgsbep'),(225,9,'Mockingbird','561jH07mF1jHuk7KlaeF0s'),(226,9,'Die For You - Remix','7oDd86yk8itslrA9HRP2ki'),(227,9,'Chemical','5w40ZYhbBMAlHYNDaVJIUu'),(228,9,'Watch This - ARIZONATEARS Pluggnb Remix','0FA4wrjDJvJTTU8AepZTup'),(230,9,'The Real Slim Shady','3yfqSUWxFvZELEM4PmlwIR'),(231,9,'First Class','0wHFktze2PHC5jDt3B17DC'),(232,9,'INDUSTRY BABY (feat. Jack Harlow)','27NovPIUIRrOZoCHxABJwK'),(233,9,'WHATS POPPIN','1jaTQ3nqY3oAAYyCTbIvnM'),(234,10,'Still D.R.E.','503OTo2dSqe7qk76rgsbep'),(235,10,'Flooded The Face','4daEMLSZCgZ2Mt7gNm2SRa'),(236,10,'The Spins','7FAFkQQZFeNwOFzTrSDFIh'),(237,10,'Mockingbird','561jH07mF1jHuk7KlaeF0s'),(238,10,'Die For You - Remix','7oDd86yk8itslrA9HRP2ki'),(239,10,'Watch This - ARIZONATEARS Pluggnb Remix','0FA4wrjDJvJTTU8AepZTup'),(240,10,'The Real Slim Shady','3yfqSUWxFvZELEM4PmlwIR'),(241,10,'3D (feat. Jack Harlow)','6ehWdR7cGDXnT7aKEASJxE'),(242,10,'INDUSTRY BABY (feat. Jack Harlow)','27NovPIUIRrOZoCHxABJwK'),(243,10,'First Class','0wHFktze2PHC5jDt3B17DC'),(246,10,'Super Shy','5sdQOyqq2IDhvmx2lHOpwd');
/*!40000 ALTER TABLE `playlists` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-06 14:20:08
