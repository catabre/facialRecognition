CREATE TABLE `face` (
  `id` int NOT NULL AUTO_INCREMENT,
  `faceId` varchar(255) NOT NULL,
  `imageId` varchar(255) NOT NULL,
  `imageURL` varchar(255) NOT NULL,
  `personName` varchar(255) DEFAULT 'UNKNOWN', 
  `left` varchar(255) NOT NULL,
  `top` varchar(255) NOT NULL,
  `height` varchar(255) NOT NULL,
  `width` varchar(255) NOT NULL,
  `is_active` int DEFAULT 1,
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `createdBy` varchar(255) DEFAULT NULL,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updatedBy` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`), 
  UNIQUE(faceId)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
