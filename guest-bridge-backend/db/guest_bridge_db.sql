-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2025 at 10:01 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

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
(1, 'Jázmin Apartmanház', b'1', '751824', NULL, 'YjRlNzU0ZTgtYTJlZC00NDI2LTg2YWMtZDFlM2Y1ZWVhMzYx', 'N2Y3MmY5MjMtNWRlNi00NTkwLWI1MGQtZTU4YzYzMjUzZTM3', '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-11-26 20:09:41', NULL, NULL, 'Test Elek', '+367558461', 'nincs@nincshu', 'MA234567GD123', 1),
(2, 'Ilonka Villa', b'1', '1435157', NULL, 'NmQ3YjA0ZDctMzhjZS00YWVjLTg2OGQtMGI5MjNmNDI0MTA5', 'Mzc0ZjJiMWMtMzY4Yy00MTY1LWEzYzEtMGQ1MDkxZDhmMTk0', '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-11-26 20:15:22', NULL, NULL, 'Én vagyok', NULL, 'valami@valami.com', 'yxyxyxyxx', 4),
(3, 'Fészek Apartman', b'1', NULL, NULL, 'ZWJhZGMzY2ItYmE0Zi00Nzk2LTk3NDktNGYxMDQzNDRlNDA3', 'M2U2NTA2YTYtMzhhOS00NDEwLThiMTctOWJjMmFlNWVlYmRm', '2025-05-15 15:43:02', 'norbert.balogh', NULL, '2025-11-22 12:36:46', NULL, NULL, 'xy', NULL, NULL, '', 3),
(20, 'Teszt szállás', b'1', '12312', NULL, '', '', '2025-12-11 15:30:26', 'nickdale', NULL, '2025-12-11 14:30:26', NULL, NULL, NULL, NULL, NULL, 'NA001', 8);

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
(1, 'H. Edina', 'pista.test@gmail.com', 'adoszam', 'Magyarország', '8230', 'Balatonfüred', 'Móra Ferenc u.', '9', '', '11 ajtó', '2025-05-16 10:52:12', 'norbert.balogh', 'nickdale', '2025-12-11 15:27:13'),
(3, NULL, NULL, NULL, 'Magyarország', '1010', 'Budapest', 'Fő utca', '10', '', '', '2025-05-16 13:32:39', 'norbert.balogh', NULL, '2025-05-16 13:32:39'),
(4, 'H. Zsuzsa', NULL, NULL, 'Magyarország', '8230', 'Balatonfüred', 'Garay János utca', '13', '', '', '2025-05-16 13:32:39', 'norbert.balogh', NULL, '2025-11-26 20:08:38'),
(6, NULL, NULL, NULL, 'Magyarország', '', 'Kalocsa', '10. utca', '30', NULL, NULL, '2025-12-11 11:54:42', 'nickdale', NULL, '2025-12-11 10:54:42'),
(7, NULL, NULL, NULL, 'Magyarország', '', 'Kalocsa', 'kis utca', '10', NULL, NULL, '2025-12-11 15:12:57', 'nickdale', NULL, '2025-12-11 14:12:57'),
(8, NULL, NULL, NULL, 'Magyarország', '', 'Kalocsa', 'Teszt', '10', NULL, NULL, '2025-12-11 15:30:26', 'nickdale', NULL, '2025-12-11 14:30:26');

-- --------------------------------------------------------

--
-- Table structure for table `room_mappings`
--

CREATE TABLE `room_mappings` (
  `id` int(11) NOT NULL,
  `accommodation_id` int(11) NOT NULL,
  `szallas_hu_ext_room_id` varchar(255) DEFAULT NULL,
  `szallas_hu_ext_room_name` varchar(255) DEFAULT NULL,
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
(5, 3, NULL, 'szoba 1', 'Y2YwODNiOGYtZWNhZi00YmQ2LTllNDgtMmI4OWNlOWI1Y2Nm', '1. szoba', '2025-11-22 12:41:20', 'balogh.norbert', NULL, '2025-11-22 12:41:41'),
(6, 3, NULL, 'szoba 2', 'ZWFkMjNmNWItODlkOS00OWY4LWFiZGYtMzYzNTAwZWQzNzA5', '2. szoba', '2025-11-22 12:41:20', 'balogh.norbert', NULL, '2025-11-22 12:41:46'),
(7, 3, NULL, 'szoba 3', 'Nzg2N2RhYjItN2U0ZC00MWU1LTkxYWMtMWNjNGRiZGMyMzUw', '3. szoba', '2025-11-22 12:41:20', 'balogh.norbert', NULL, '2025-11-22 12:41:51'),
(8, 3, NULL, 'extra szoba (4)', 'MThlNTEzM2MtYmI2Yi00NDkwLTg2MGQtNWI5ZjdkZTUyN2M0', '4. szoba', '2025-11-22 12:41:20', 'balogh.norbert', NULL, '2025-11-22 12:42:01'),
(9, 2, NULL, 'földszinti 2', 'ZmNmYzgxOTQtODYyNC00N2I0LTk2M2YtYzFiNjU0M2ZmOGVi', '2. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-22 12:50:56'),
(10, 2, NULL, '5-ös szoba', 'OWEzN2FkODctODQyZi00ZjdkLTlhZjMtMWIzZmIzZjI0MTEw', '5. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:19:01'),
(11, 2, NULL, '8-as szoba', 'YmJmNDExZTItZmI0Zi00MGM3LTljOGItYTk4NTMxNTRlODRh', '8. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:18:53'),
(12, 2, NULL, '1-es szoba', 'YzlmMjMzNGYtZmQ1Yi00MDNiLWFiYjYtYTczMzdiNjlmZTE4', '1. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:16:10'),
(13, 2, NULL, '3-as szoba', 'Y2NmMmNiNDUtYTI5OC00Y2FhLTk0YTAtMTAxODJhYjlkMGRj', '3. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:18:09'),
(15, 2, NULL, '7-es szoba', 'ZTNlNzA2ZGEtZWNmOC00NGQ5LWEyZDQtNGVlMmU0ZTUyM2Fj', '7. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:19:19'),
(16, 2, NULL, '6-os szoba', 'NmIzOGY4MjgtODhhYi00NjgzLWIwNmMtMTA0NTc2YjkwYjM5', '6. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:19:30'),
(17, 2, NULL, '4-es szoba', 'NjQ2YWZiZDctYmM2ZS00ZTc5LWE2YjUtNTRiNmM4NTI4M2E0', '4. szoba', '2025-11-22 12:44:45', 'balogh.norbert', NULL, '2025-11-26 20:19:37'),
(18, 1, NULL, '2 szobás,  amerikai konyhás, teraszos, 1-es számú apartman.', 'ZjkxY2Q5ODAtMzFjNC00YzYxLTlkZWItM2EzNTU1NzNjYjQ0', '1-es', '2025-11-22 12:47:28', 'balogh.norbert', NULL, '2025-12-11 17:36:31'),
(19, 1, NULL, 'Panorámás, erkélyes, 4-es számú apartman', 'NjYyMTRmODQtMGQ3NC00Njg4LTk1MTAtMzg3N2RkYWY1MmJm', '4-es', '2025-11-22 12:47:28', 'balogh.norbert', NULL, '2025-11-26 20:06:03'),
(20, 1, NULL, 'Erkélyes, 2-es számú apartman', 'Mzg3MjllNjItZTA3Yi00NTFiLTkxODktMmJjYzhiMDZmYzlj', '2-es', '2025-11-22 12:47:28', 'balogh.norbert', NULL, '2025-11-26 20:05:42'),
(21, 1, NULL, 'Emeleti 4 fős, 5-ös számú apartman', 'NTIxYmQxOTctZDFjMS00ZmJiLWFhNDUtODgxNzhkMWZhMTJk', '5-ös', '2025-11-22 12:47:28', 'balogh.norbert', NULL, '2025-11-26 20:05:32'),
(22, 1, NULL, 'Erkélyes, konyhás, 3-as számú apartman', 'ODk1MTE3Y2MtZDQzNi00OTNjLTg3ODgtYTk0NzM0YmQ2MjAy', '3-as', '2025-11-22 12:47:28', 'balogh.norbert', NULL, '2025-11-26 20:05:54');

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
-- Table structure for table `sync_histories`
--

CREATE TABLE `sync_histories` (
  `id` int(11) NOT NULL,
  `accommodation_id` int(11) NOT NULL,
  `debug_message` varchar(255) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `error_message` varchar(255) DEFAULT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `sync_histories`
--

INSERT INTO `sync_histories` (`id`, `accommodation_id`, `debug_message`, `status`, `error_message`, `created_date`, `created_by`) VALUES
(1, 2, 'test', 'ok', NULL, '2025-11-22 15:05:14', 'balogh.norbert'),
(3, 1, NULL, 'FAILED', NULL, '2025-12-02 10:04:53', 'user_id:1'),
(4, 1, NULL, 'OK', NULL, '2025-12-02 10:15:32', 'user_id:1'),
(5, 1, NULL, 'OK', NULL, '2025-12-02 12:22:34', 'user_id:1'),
(14, 1, NULL, 'OK', NULL, '2025-12-11 17:42:17', 'user_id:2'),
(18, 1, NULL, 'OK', NULL, '2025-12-11 18:08:01', 'user_id:2'),
(23, 1, NULL, 'OK', NULL, '2025-12-11 18:34:52', 'user_id:2');

-- --------------------------------------------------------

--
-- Table structure for table `sync_history_details`
--

CREATE TABLE `sync_history_details` (
  `id` int(11) NOT NULL,
  `sync_id` int(11) NOT NULL,
  `reservation_id` varchar(255) DEFAULT NULL,
  `debug_message` varchar(255) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `error_message` varchar(255) DEFAULT NULL,
  `created_date` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_hungarian_ci;

--
-- Dumping data for table `sync_history_details`
--

INSERT INTO `sync_history_details` (`id`, `sync_id`, `reservation_id`, `debug_message`, `type`, `status`, `error_message`, `created_date`, `created_by`) VALUES
(1, 1, 'test_sz001', 'test_sz001 id ~~ szoba x  --> vendegem y', 'foglalas', 'ok', NULL, '2025-11-22 15:07:23', 'balogh.norbert'),
(2, 1, 'test_sz002', 'test_sz002 id ~~ szoba x  --> vendegem y', 'lemondas', 'ok', NULL, '2025-11-22 15:07:23', 'balogh.norbert'),
(3, 4, '16487331', 'Sync szallas_hu reservation [16487331] to Vendegem ', 'INSERT', 'OK', NULL, '2025-12-02 10:16:14', NULL),
(4, 4, '16460149', 'Sync szallas_hu reservation [16460149] to Vendegem ', 'INSERT', 'OK', NULL, '2025-12-02 10:16:21', NULL),
(11, 23, '16776475', 'Szallas_hu foglalas [16776475] törlése a Vendegemből - szobaId[MDI4NWRjZDYtN2Y1MS00MWMzLWE5MzctODA3OGIwOTJmM2Jk]', 'DELETE', 'OK', NULL, '2025-12-11 18:34:56', NULL),
(12, 23, '16782835', 'Szallas_hu foglalás [16782835] rögzítése a Vendegembe', 'INSERT', 'OK', NULL, '2025-12-11 18:34:57', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) DEFAULT NULL,
  `full_name` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  `billing_address_id` int(11) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `activation_date` datetime DEFAULT NULL,
  `blocked_date` datetime DEFAULT NULL,
  `subscription_type_id` int(11) DEFAULT NULL,
  `encrypted_secret` varchar(255) DEFAULT NULL,
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
(2, 'owner_1', 'H. Edina', 'balogh.norbert92+he@gmail.com', 1, 3, '2025-12-11 15:26:38', NULL, 1, 'qwe123', NULL, '2025-05-15 13:17:40', 'balogh.norbert', 'nickdale', '2025-12-11 15:27:13'),
(3, 'owner_2', 'Kiss G', 'balogh.norbert92+kissg@gmail.com', 1, 3, NULL, '2025-11-26 20:11:22', 1, '1234', NULL, '2025-05-15 13:17:40', 'balogh.norbert', 'nickdale', '2025-11-26 20:11:22'),
(4, 'emp_1', 'H. Zsuzsa', 'balogh.norbert92+zsn@gmail.com', 1, 3, '2025-11-26 21:48:44', NULL, 1, '1234', NULL, '2025-05-15 13:17:40', 'balogh.norbert', 'nickdale', '2025-11-26 21:48:44'),
(25, NULL, 'P. Kati', 'balogh.norbert92+pk@gmail.com', NULL, 3, '2025-11-26 21:55:32', NULL, NULL, NULL, NULL, '2025-11-26 21:55:32', 'nickdale', NULL, '2025-11-26 20:55:32'),
(27, NULL, 'Test', 'test@test.hu', NULL, 3, '2025-12-11 15:08:18', NULL, NULL, NULL, NULL, '2025-12-11 15:08:18', 'nickdale', NULL, '2025-12-11 14:08:18'),
(28, NULL, 'Test2', 'test2@test.hu', NULL, 3, '2025-12-11 15:08:45', NULL, NULL, NULL, NULL, '2025-12-11 15:08:45', 'nickdale', NULL, '2025-12-11 14:08:45'),
(29, NULL, 'Bemutato', 'bemut@tato.hu', NULL, 3, '2025-12-11 15:18:45', NULL, NULL, NULL, NULL, '2025-12-11 15:18:45', 'nickdale', NULL, '2025-12-11 14:18:45'),
(30, NULL, 'Bemutató Felhasználó', 'bemuttato@felh.hu', NULL, 3, '2025-12-11 15:25:39', NULL, NULL, NULL, NULL, '2025-12-11 15:25:39', 'nickdale', NULL, '2025-12-11 14:25:39');

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
(2, 2, 4, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-11-22 12:48:44', NULL, NULL),
(5, 3, 3, '2025-05-15 15:45:43', 'norbert.balogh', NULL, '2025-11-22 12:49:05', NULL, NULL),
(15, 2, 25, '2025-11-26 21:57:11', 'nickdale', NULL, '2025-11-26 21:57:11', NULL, NULL),
(18, 20, 2, '2025-12-11 15:30:26', 'nickdale', NULL, '2025-12-11 14:30:26', NULL, NULL);

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
-- Indexes for table `sync_histories`
--
ALTER TABLE `sync_histories`
  ADD PRIMARY KEY (`id`),
  ADD KEY `accommodation_id` (`accommodation_id`);

--
-- Indexes for table `sync_history_details`
--
ALTER TABLE `sync_history_details`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sync_id` (`sync_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `addresses`
--
ALTER TABLE `addresses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `room_mappings`
--
ALTER TABLE `room_mappings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `subscription_types`
--
ALTER TABLE `subscription_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `sync_histories`
--
ALTER TABLE `sync_histories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `sync_history_details`
--
ALTER TABLE `sync_history_details`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `user_accommodations`
--
ALTER TABLE `user_accommodations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

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
-- Constraints for table `sync_histories`
--
ALTER TABLE `sync_histories`
  ADD CONSTRAINT `sync_histories_ibfk_1` FOREIGN KEY (`accommodation_id`) REFERENCES `accommodations` (`id`);

--
-- Constraints for table `sync_history_details`
--
ALTER TABLE `sync_history_details`
  ADD CONSTRAINT `sync_history_details_ibfk_1` FOREIGN KEY (`sync_id`) REFERENCES `sync_histories` (`id`);

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
