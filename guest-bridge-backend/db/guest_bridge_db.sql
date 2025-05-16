-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 16, 2025 at 04:23 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `guest_bridge`
--
CREATE DATABASE IF NOT EXISTS `guest_bridge` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_hungarian_ci;
USE `guest_bridge`;

-- --------------------------------------------------------

--
-- Table structure for table `accommodations`
--

CREATE TABLE `accommodations` (
  `id` int(11) NOT NULL,
  `display_name` varchar(200) DEFAULT NULL,
  `active` bit(1) DEFAULT b'1',
  `szallas_hu_external_id` varchar(255) DEFAULT NULL,
  `szallas_hu_external_ref` varchar(255) DEFAULT NULL,
  `vendegem_external_id` varchar(255) DEFAULT NULL,
  `vendegem_external_ref` varchar(255) DEFAULT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) NOT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `modified_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_date` datetime DEFAULT NULL,
  `deleted_by` varchar(100) DEFAULT NULL,
  `contact_name` varchar(100) DEFAULT NULL,
  `contact_phone` varchar(100) DEFAULT NULL,
  `contact_email` varchar(100) DEFAULT NULL,
  `reg_number` varchar(100) NOT NULL,
  `address_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `accommodations`
--

INSERT INTO `accommodations` (`id`, `display_name`, `active`, `szallas_hu_external_id`, `szallas_hu_external_ref`, `vendegem_external_id`, `vendegem_external_ref`, `created_date`, `created_by`, `modified_by`, `modified_date`, `deleted_date`, `deleted_by`, `contact_name`, `contact_phone`, `contact_email`, `reg_number`, `address_id`) VALUES
(1, 'teszt szallas 1', b'1', NULL, NULL, NULL, NULL, '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-16 13:32:56', NULL, NULL, 'Test Elek', '+367558461', 'nincs@nincshu', 'MA234567GD123', 4),
(2, 'teszt szallas 2', b'1', '1', 'ref1', 'ZWJhZGMzY2ItYmE0Zi00Nzk2LTk3NDktNGYxMDQzNDRlNDA3', 'vref1', '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-16 15:15:07', NULL, NULL, 'Én vagyok', NULL, 'valami@valami.com', 'yxyxyxyxx', 2),
(3, 'teszt szallas X', b'1', NULL, NULL, NULL, NULL, '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-16 13:49:59', NULL, NULL, 'xy', NULL, NULL, '', 3),
(4, 'teszt szallas almádi', b'1', NULL, NULL, NULL, NULL, '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-16 13:32:59', NULL, NULL, NULL, NULL, NULL, '', 3),
(5, 'Apartman 2', b'1', NULL, NULL, NULL, NULL, '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-15 15:43:02', NULL, NULL, NULL, NULL, NULL, '', NULL),
(6, 'Apartman füred', b'1', NULL, NULL, NULL, NULL, '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-16 13:50:13', NULL, NULL, 'kis Piroska', '22222', NULL, '', 2),
(7, 'Apartman almádi', b'1', NULL, NULL, NULL, NULL, '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-05-15 15:43:02', NULL, NULL, NULL, NULL, NULL, '', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `addresses`
--

CREATE TABLE `addresses` (
  `id` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `tax_number` varchar(50) DEFAULT NULL,
  `country` varchar(20) DEFAULT NULL,
  `postcode` varchar(20) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `street_number` varchar(10) DEFAULT NULL,
  `floor` varchar(10) DEFAULT NULL,
  `door` varchar(10) DEFAULT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) NOT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `modified_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `addresses`
--

INSERT INTO `addresses` (`id`, `name`, `email`, `tax_number`, `country`, `postcode`, `city`, `street`, `street_number`, `floor`, `door`, `created_date`, `created_by`, `modified_by`, `modified_date`) VALUES
(1, 'Kiss Pista', 'kis.pista.test@gmail.com', 'tax', 'Magyarország', '6726', 'Szeged', 'Dugonics tér', '1', '1. elmelet', '11 ajtó', '2025-05-16 10:52:12', 'norbert.balogh', NULL, '2025-05-16 10:52:12'),
(2, NULL, NULL, NULL, 'Magyarország', '6000', 'Kecskemét', 'Fő utca', '10', '2', '5A', '2025-05-16 13:32:39', 'norbert.balogh', NULL, '2025-05-16 13:32:39'),
(3, NULL, NULL, NULL, 'Magyarország', '1010', 'Budapest', 'Fő utca', '10', '', '', '2025-05-16 13:32:39', 'norbert.balogh', NULL, '2025-05-16 13:32:39'),
(4, NULL, NULL, NULL, 'Magyarország', '8230', 'Balatonfüred', 'Garay János utca', '13', '', '', '2025-05-16 13:32:39', 'norbert.balogh', NULL, '2025-05-16 13:32:39');

-- --------------------------------------------------------

--
-- Table structure for table `room_mappings`
--

CREATE TABLE `room_mappings` (
  `id` int(11) NOT NULL,
  `accommodation_id` int(11) NOT NULL,
  `szallas_hu_ext_room_id` varchar(255) DEFAULT NULL,
  `szallas_hu_ext_room_name` varchar(50) DEFAULT NULL,
  `vendegem_ext_room_id` varchar(255) DEFAULT NULL,
  `vendegem_ext_room_name` varchar(50) DEFAULT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) NOT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `modified_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `room_mappings`
--

INSERT INTO `room_mappings` (`id`, `accommodation_id`, `szallas_hu_ext_room_id`, `szallas_hu_ext_room_name`, `vendegem_ext_room_id`, `vendegem_ext_room_name`, `created_date`, `created_by`, `modified_by`, `modified_date`) VALUES
(1, 4, '1', 'Földszinti 1-es szoba', 'Y2YwODNiOGYtZWNhZi00YmQ2LTllNDgtMmI4OWNlOWI1Y2Nm', '1. szoba', '2025-05-16 14:55:05', 'norbert.balogh', NULL, '2025-05-16 14:55:05'),
(2, 4, '2', 'Földszinti 2-es szoba', 'ZWFkMjNmNWItODlkOS00OWY4LWFiZGYtMzYzNTAwZWQzNzA5', '2. szoba', '2025-05-16 14:55:05', 'norbert.balogh', NULL, '2025-05-16 14:55:05'),
(3, 4, '3', 'Emeleti erkélyes szoba', 'Nzg2N2RhYjItN2U0ZC00MWU1LTkxYWMtMWNjNGRiZGMyMzUw', '3. szoba', '2025-05-16 14:55:05', 'norbert.balogh', NULL, '2025-05-16 14:55:05'),
(4, 4, '4', 'Emeleti Lakosztály', 'MThlNTEzM2MtYmI2Yi00NDkwLTg2MGQtNWI5ZjdkZTUyN2M0', '4. szoba', '2025-05-16 14:55:05', 'norbert.balogh', NULL, '2025-05-16 14:55:05');

-- --------------------------------------------------------

--
-- Table structure for table `subscription_types`
--

CREATE TABLE `subscription_types` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `subscription_types`
--

INSERT INTO `subscription_types` (`id`, `name`) VALUES
(2, 'Éves előfizetés'),
(3, 'Havi előfizetés'),
(4, 'Negyedéves előfizetés'),
(1, 'Trial (Ingyenes időszak)');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `billing_address_id` int(11) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `activation_date` datetime DEFAULT NULL,
  `blocked_date` datetime DEFAULT NULL,
  `subscription_type_id` int(11) NOT NULL,
  `encrypted_secret` varchar(255) NOT NULL,
  `salt` varchar(255) DEFAULT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) NOT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `modified_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `full_name`, `email`, `billing_address_id`, `type_id`, `activation_date`, `blocked_date`, `subscription_type_id`, `encrypted_secret`, `salt`, `created_date`, `created_by`, `modified_by`, `modified_date`) VALUES
(1, 'nickdale', 'Balogh Norbert', 'balogh.norbert92@gmail.com', NULL, 1, '2025-02-26 00:00:00', NULL, 1, '123456', NULL, '2025-02-26 15:44:55', 'nickdale', NULL, '2025-02-26 15:44:55'),
(2, 'owner_1', 'teszt tulaj 1', 'test_t_1@gmail.com', 1, 3, NULL, NULL, 1, '1234', NULL, '2025-05-15 13:17:40', 'balogh.norbert', NULL, '2025-05-16 10:52:24'),
(3, 'owner_2', 'teszt tulaj 2', 'test_t_2@gmail.com', 1, 3, '2025-05-22 20:48:51', NULL, 1, '1234', NULL, '2025-05-15 13:17:40', 'balogh.norbert', NULL, '2025-05-16 10:52:38'),
(4, 'emp_1', 'teszt alk 1', 'test_emp_1@gmail.com', 1, 3, NULL, NULL, 1, '1234', NULL, '2025-05-15 13:17:40', 'balogh.norbert', NULL, '2025-05-16 10:58:24'),
(5, 'emp_2', 'teszt alk 2', 'test_emp_2@gmail.com', 1, 3, NULL, NULL, 1, '1234', NULL, '2025-05-15 13:17:40', 'balogh.norbert', NULL, '2025-05-16 10:58:38');

-- --------------------------------------------------------

--
-- Table structure for table `user_accommodations`
--

CREATE TABLE `user_accommodations` (
  `id` int(11) NOT NULL,
  `accommodation_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) NOT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  `modified_date` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_date` datetime DEFAULT NULL,
  `deleted_by` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `user_accommodations`
--

INSERT INTO `user_accommodations` (`id`, `accommodation_id`, `user_id`, `created_date`, `created_by`, `modified_by`, `modified_date`, `deleted_date`, `deleted_by`) VALUES
(1, 1, 2, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL),
(2, 2, 2, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL),
(3, 2, 4, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL),
(4, 2, 5, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL),
(5, 4, 2, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL),
(6, 6, 4, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL),
(7, 7, 5, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-05-15 15:45:43', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user_types`
--

CREATE TABLE `user_types` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `user_types`
--

INSERT INTO `user_types` (`id`, `name`) VALUES
(1, 'Admin'),
(3, 'Felhasználó');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accommodations`
--
ALTER TABLE `accommodations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accomodations_adfk_1` (`address_id`);

--
-- Indexes for table `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `room_mappings`
--
ALTER TABLE `room_mappings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accomodation_id` (`accommodation_id`);

--
-- Indexes for table `subscription_types`
--
ALTER TABLE `subscription_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `subscription_type_id` (`subscription_type_id`),
  ADD KEY `billing_address_id` (`billing_address_id`),
  ADD KEY `users_ibfk_2` (`type_id`);

--
-- Indexes for table `user_accommodations`
--
ALTER TABLE `user_accommodations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accomodation_id` (`accommodation_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user_types`
--
ALTER TABLE `user_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accommodations`
--
ALTER TABLE `accommodations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `addresses`
--
ALTER TABLE `addresses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `room_mappings`
--
ALTER TABLE `room_mappings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `subscription_types`
--
ALTER TABLE `subscription_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user_accommodations`
--
ALTER TABLE `user_accommodations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_types`
--
ALTER TABLE `user_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accommodations`
--
ALTER TABLE `accommodations`
  ADD CONSTRAINT `accomodations_adfk_1` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`id`);

--
-- Constraints for table `room_mappings`
--
ALTER TABLE `room_mappings`
  ADD CONSTRAINT `room_mappings_ibfk_1` FOREIGN KEY (`accommodation_id`) REFERENCES `accommodations` (`id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`subscription_type_id`) REFERENCES `subscription_types` (`id`),
  ADD CONSTRAINT `users_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `user_types` (`id`),
  ADD CONSTRAINT `users_ibfk_3` FOREIGN KEY (`billing_address_id`) REFERENCES `addresses` (`id`);

--
-- Constraints for table `user_accommodations`
--
ALTER TABLE `user_accommodations`
  ADD CONSTRAINT `user_accommodations_ibfk_1` FOREIGN KEY (`accommodation_id`) REFERENCES `accommodations` (`id`),
  ADD CONSTRAINT `user_accommodations_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
