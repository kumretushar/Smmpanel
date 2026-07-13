-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 18, 2025 at 01:55 PM
-- Server version: 10.11.11-MariaDB
-- PHP Version: 8.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `boibipon_toup`
--

-- --------------------------------------------------------

--
-- Table structure for table `auto_vouchers`
--

CREATE TABLE `auto_vouchers` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `variation_id` bigint(20) UNSIGNED NOT NULL,
  `order_id` bigint(20) UNSIGNED DEFAULT NULL,
  `code` varchar(255) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `transaction_id` varchar(55) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `slot` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `title`, `slot`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Free Fire', '2', '1', '2025-08-03 11:38:01', '2025-08-03 12:59:58'),
(5, 'SPECIAL OFFERS', '1', '1', '2025-08-03 12:31:40', '2025-08-03 12:31:40'),
(6, 'LIKE-FOLLLOW-SUBSCRIBER', '3', '1', '2025-08-04 09:01:12', '2025-08-04 09:01:12'),
(7, 'Free Fire Uid topup', '1000', '1', '2025-08-17 22:57:01', '2025-08-18 12:17:44');

-- --------------------------------------------------------

--
-- Table structure for table `deposits`
--

CREATE TABLE `deposits` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `amount` decimal(16,2) NOT NULL DEFAULT 0.00,
  `track_id` varchar(25) NOT NULL,
  `status` enum('unpaid','paid') NOT NULL DEFAULT 'unpaid',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `deposits`
--

INSERT INTO `deposits` (`id`, `user_id`, `amount`, `track_id`, `status`, `created_at`, `updated_at`) VALUES
(94, 3976, 500.00, 'O15B448S554J', 'unpaid', '2025-08-18 02:14:40', '2025-08-18 02:14:40');

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `connection` text NOT NULL,
  `queue` text NOT NULL,
  `payload` longtext NOT NULL,
  `exception` longtext NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `queue` varchar(255) NOT NULL,
  `payload` longtext NOT NULL,
  `attempts` tinyint(3) UNSIGNED NOT NULL,
  `reserved_at` int(10) UNSIGNED DEFAULT NULL,
  `available_at` int(10) UNSIGNED NOT NULL,
  `created_at` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `media`
--

CREATE TABLE `media` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `model_type` varchar(255) NOT NULL,
  `model_id` bigint(20) UNSIGNED NOT NULL,
  `uuid` char(36) DEFAULT NULL,
  `collection_name` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `mime_type` varchar(255) DEFAULT NULL,
  `disk` varchar(255) NOT NULL,
  `conversions_disk` varchar(255) DEFAULT NULL,
  `size` bigint(20) NOT NULL,
  `manipulations` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`manipulations`)),
  `custom_properties` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`custom_properties`)),
  `generated_conversions` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`generated_conversions`)),
  `responsive_images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`responsive_images`)),
  `order_column` int(10) UNSIGNED DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `media`
--

INSERT INTO `media` (`id`, `model_type`, `model_id`, `uuid`, `collection_name`, `name`, `file_name`, `mime_type`, `disk`, `conversions_disk`, `size`, `manipulations`, `custom_properties`, `generated_conversions`, `responsive_images`, `order_column`, `created_at`, `updated_at`) VALUES
(122, 'App\\Models\\Product', 11, 'af45c925-0fdd-4f83-b7c4-b646b8b4de93', 'default', '20250715_224902~2', '01K0ZZKGC2JX6YY7QVEBZGA41J.jpg', 'image/jpeg', 'media', 'media', 141761, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:36:29', '2025-07-25 05:36:29'),
(123, 'App\\Models\\Product', 12, '76f05eca-b89d-4c58-8aa7-5e60065d4dde', 'default', '20250715_224602~2', '01K0ZZM8DEHNT9640X21C247SG.jpg', 'image/jpeg', 'media', 'media', 118565, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:36:54', '2025-07-25 05:36:54'),
(124, 'App\\Models\\Product', 13, '5a868aac-4f3d-4250-961a-fe98751d3231', 'default', '20250715_224231~2', '01K0ZZNASBCDTTF6PBVGVMHVA2.jpg', 'image/jpeg', 'media', 'media', 117133, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:37:29', '2025-07-25 05:37:29'),
(125, 'App\\Models\\Product', 14, 'a341fbc8-54e5-4fb6-a98c-9d5a828789f1', 'default', '20250715_224336~2', '01K0ZZP81HFFMPQWVDXV37K38A.jpg', 'image/jpeg', 'media', 'media', 121679, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:37:59', '2025-07-25 05:37:59'),
(126, 'App\\Models\\Product', 16, '3b5bb1e7-39bc-487f-9eac-83e336f2092e', 'default', '20250715_224134~2', '01K0ZZQ1VKS8DBVJFETYJ2BYP1.jpg', 'image/jpeg', 'media', 'media', 110712, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:38:25', '2025-07-25 05:38:25'),
(127, 'App\\Models\\Product', 17, '8ac3bf3f-a48f-4553-974f-725d21899612', 'default', '20250715_224447~2', '01K0ZZQS772SF928VG79QAKV1Z.jpg', 'image/jpeg', 'media', 'media', 114804, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:38:49', '2025-07-25 05:38:49'),
(128, 'App\\Models\\Product', 18, '6f87dda6-5e71-4d07-b035-1c1f488f03b7', 'default', '20250715_225020~2', '01K0ZZRZPCP0BVP6FW883ZVAQ6.jpg', 'image/jpeg', 'media', 'media', 139441, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:39:28', '2025-07-25 05:39:28'),
(129, 'App\\Models\\Product', 19, 'e72a265f-7e55-486c-9141-904eff05d4c8', 'default', '20250715_224725~2', '01K0ZZSY4ZHNKYN760ZGJCA2GN.jpg', 'image/jpeg', 'media', 'media', 120320, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:40:00', '2025-07-25 05:40:00'),
(130, 'App\\Models\\Product', 20, '57e4b7dc-6359-4116-9ea0-adfb4881416a', 'default', '20250716_000147~2', '01K0ZZTRRSE2CAC45ZQY6GDV8P.jpg', 'image/jpeg', 'media', 'media', 67676, '[]', '[]', '[]', '[]', 1, '2025-07-25 05:40:27', '2025-07-25 05:40:27'),
(138, 'App\\Models\\Product', 22, '82afda9c-c4b8-4d64-9364-fe58e515a1c7', 'default', '01K13PFJDSTEHJNY1G2223A3EK', '01K1QX215QYF99KS34RDJBMJJE.jpg', 'image/jpeg', 'media', 'media', 31984, '[]', '[]', '[]', '[]', 1, '2025-08-03 12:33:45', '2025-08-03 12:33:45'),
(142, 'App\\Models\\Product', 26, '37906ac9-5154-4c8d-b89e-dfa90af797aa', 'default', '1753803627', '01K1T3E5S9MC4B7P0MV6H5SMP1.png', 'image/png', 'media', 'media', 72300, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:03:44', '2025-08-04 09:03:44'),
(143, 'App\\Models\\Product', 27, '539bd30a-44db-4653-ba71-c20928dcdb0a', 'default', '1753803591', '01K1T3MMWXP1W4AARZ7TTN44GC.png', 'image/png', 'media', 'media', 76390, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:07:16', '2025-08-04 09:07:16'),
(144, 'App\\Models\\Product', 28, 'c0e197dc-af69-4b0c-b3c9-7664a2bf98e3', 'default', '1753803337', '01K1T3ZRDSA4MNPH6S6ESP4F5N.png', 'image/png', 'media', 'media', 73280, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:13:20', '2025-08-04 09:13:20'),
(145, 'App\\Models\\Product', 29, '30c5a313-e63b-474d-a8d4-f924ed1261cf', 'default', '1753803294', '01K1T42ZMKRCP1CNR6861R82S1.png', 'image/png', 'media', 'media', 71465, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:15:06', '2025-08-04 09:15:06'),
(146, 'App\\Models\\Product', 30, 'b55b8b5c-d6f4-458b-9044-78c599f96431', 'default', '1753803551', '01K1T46FJ6QT2KF6AWN5Y81RJW.png', 'image/png', 'media', 'media', 75835, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:17:00', '2025-08-04 09:17:00'),
(147, 'App\\Models\\Product', 31, 'e5343557-6d40-4b13-8daa-7f8b896e8a35', 'default', '1753803951', '01K1T4XS4A74CYSVVZ6GRH9GYY.png', 'image/png', 'media', 'media', 61961, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:29:44', '2025-08-04 09:29:44'),
(148, 'App\\Models\\Product', 32, '5e3c8ae8-5a0e-4746-ab3f-264248cdac38', 'default', '1753804256', '01K1T50F3HPK6PRFRBZHCYBS4P.png', 'image/png', 'media', 'media', 65376, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:31:12', '2025-08-04 09:31:12'),
(149, 'App\\Models\\Product', 33, '3d96c100-febe-4003-973f-f078d8c88fe2', 'default', '1753804177', '01K1T55SVBH445V533EKQC7QBH.png', 'image/png', 'media', 'media', 64517, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:34:07', '2025-08-04 09:34:07'),
(150, 'App\\Models\\Product', 34, '3648e034-c7b8-4b25-86a8-496d5079ce9c', 'default', '1753803197', '01K1T5AE6KXC6NX1QTGKBNTQYF.png', 'image/png', 'media', 'media', 66181, '[]', '[]', '[]', '[]', 1, '2025-08-04 09:36:38', '2025-08-04 09:36:38'),
(153, 'App\\Models\\Product', 23, '13372089-ad93-4c3c-9df7-8b8de5dcea01', 'default', '1753736119', '01K1TFN4GEYRDEMXDQQF09X67F.png', 'image/png', 'media', 'media', 601128, '[]', '[]', '[]', '[]', 1, '2025-08-04 12:37:15', '2025-08-04 12:37:15'),
(159, 'App\\Models\\Product', 36, '4ea8b343-a5c2-44c2-a5cd-ad41c966a3cf', 'default', 'Picsart_25-08-18_00-46-49-245', '01K2XHHTH4E2EQWPQHHR89F871.png', 'image/png', 'media', 'media', 1671112, '[]', '[]', '[]', '[]', 1, '2025-08-18 08:53:48', '2025-08-18 08:53:48'),
(160, 'App\\Models\\Product', 37, '0572c7e7-b6be-4327-b268-11f7216fd45f', 'default', '1000128824-300x180.jpg', '01K2XQVP30QT0G9V2SEAJJRBTH.webp', 'image/webp', 'media', 'media', 7530, '[]', '[]', '[]', '[]', 1, '2025-08-18 10:44:03', '2025-08-18 10:44:03'),
(161, 'App\\Models\\Slider', 9, '9455e1cc-1221-4677-ae60-495712050aeb', 'default', 'alert', '01K2XWP2X6PTBTZYSRATPYBHYR.jpg', 'image/jpeg', 'media', 'media', 87451, '[]', '[]', '[]', '[]', 1, '2025-08-18 12:08:22', '2025-08-18 12:08:22');

-- --------------------------------------------------------

--
-- Table structure for table `menus`
--

CREATE TABLE `menus` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `link` varchar(255) NOT NULL,
  `icon` text NOT NULL,
  `type` enum('user','guest','both') NOT NULL DEFAULT 'both',
  `order_column` int(11) NOT NULL DEFAULT 0,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `menus`
--

INSERT INTO `menus` (`id`, `name`, `link`, `icon`, `type`, `order_column`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Home', '/', '<svg data-v-7cfb45cd=\"\" width=\"25\" height=\"25\" viewBox=\"0 0 42 42\" class=\"inline-block mb-1\"><g data-v-7cfb45cd=\"\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\"><path data-v-7cfb45cd=\"\" d=\"M21.0847458,3.38674884 C17.8305085,7.08474576 17.8305085,10.7827427 21.0847458,14.4807396 C24.3389831,18.1787365 24.3389831,22.5701079 21.0847458,27.6548536 L21.0847458,42 L8.06779661,41.3066256 L6,38.5331279 L6,26.2681048 L6,17.2542373 L8.88135593,12.4006163 L21.0847458,2 L21.0847458,3.38674884 Z\" fill=\"currentColor\" fill-opacity=\"0.1\"></path> <path data-v-7cfb45cd=\"\" d=\"M11,8 L33,8 L11,8 Z M39,17 L39,36 C39,39.3137085 36.3137085,42 33,42 L11,42 C7.6862915,42 5,39.3137085 5,36 L5,17 L7,17 L7,36 C7,38.209139 8.790861,40 11,40 L33,40 C35.209139,40 37,38.209139 37,36 L37,17 L39,17 Z\" fill=\"currentColor\"></path> <path data-v-7cfb45cd=\"\" d=\"M22,27 C25.3137085,27 28,29.6862915 28,33 L28,41 L16,41 L16,33 C16,29.6862915 18.6862915,27 22,27 Z\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"currentColor\" fill-opacity=\"0.1\"></path> <rect data-v-7cfb45cd=\"\" fill=\"currentColor\" transform=\"translate(32.000000, 11.313708) scale(-1, 1) rotate(-45.000000) translate(-32.000000, -11.313708) \" x=\"17\" y=\"10.3137085\" width=\"30\" height=\"2\" rx=\"1\"></rect> <rect data-v-7cfb45cd=\"\" fill=\"currentColor\" transform=\"translate(12.000000, 11.313708) rotate(-45.000000) translate(-12.000000, -11.313708) \" x=\"-3\" y=\"10.3137085\" width=\"30\" height=\"2\" rx=\"1\"></rect></g></svg>', 'both', 0, 1, '2024-06-30 18:50:15', '2024-06-30 18:50:15'),
(2, 'Tutorial', '/page/tutorials', '<svg data-v-7cfb45cd=\"\" viewBox=\"0 0 24 24\" width=\"25\" height=\"25\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"inline-block mb-1\"><path data-v-7cfb45cd=\"\" d=\"M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z\"></path> <polygon data-v-7cfb45cd=\"\" points=\"9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02\"></polygon></svg>', 'guest', 0, 1, '2024-06-30 18:50:53', '2024-07-01 09:50:48'),
(3, 'Topup', '/?#topup', '<svg data-v-7cfb45cd=\"\" width=\"25\" height=\"25\" viewBox=\"0 0 42 42\" class=\"inline-block mb-1\"><g data-v-7cfb45cd=\"\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\"><path data-v-7cfb45cd=\"\" d=\"M20.5890101,0.254646884 C12.8696785,5.50211755 8.0025785,14.258415 14.1941217,18.8708225 C23.16683,25.5550669 13.3362326,40.2698884 33.1021758,38.4149164 C29.6814884,40.8311956 25.5065164,42.2507054 21,42.2507054 C9.40202025,42.2507054 0,32.8486852 0,21.2507054 C0,9.79003409 9.18071714,0.473634138 20.5890101,0.254646884 Z\" fill=\"currentColor\" opacity=\"0.1\"></path> <path data-v-7cfb45cd=\"\" d=\"M25.9500282,20.3643496 L22.4308312,38.2677802 C22.3775703,38.5387376 22.1147395,38.7152155 21.8437821,38.6619546 C21.6570955,38.6252584 21.507413,38.4857901 21.4576354,38.3021581 L16.5951895,20.3643496 L20.099732,4.44663907 C20.1385204,4.27046145 20.2692032,4.12883813 20.4417012,4.07604096 C20.7057521,3.99522179 20.9853245,4.14376046 21.0661436,4.40781135 L25.9500282,20.3643496 Z M21.3022963,22.2852638 C22.4068658,22.2852638 23.3022963,21.3898333 23.3022963,20.2852638 C23.3022963,19.1806943 22.4068658,18.2852638 21.3022963,18.2852638 C20.1977268,18.2852638 19.3022963,19.1806943 19.3022963,20.2852638 C19.3022963,21.3898333 20.1977268,22.2852638 21.3022963,22.2852638 Z\" fill=\"currentColor\" transform=\"translate(21.272609, 20.629524) rotate(-315.000000) translate(-21.272609, -20.629524) \"></path> <circle data-v-7cfb45cd=\"\" stroke=\"currentColor\" stroke-width=\"2\" cx=\"21\" cy=\"21\" r=\"20\"></circle></g></svg>', 'guest', 0, 1, '2024-06-30 18:51:37', '2024-06-30 18:51:37'),
(4, 'Add Fund', '/add-funds', '<svg data-v-7cfb45cd=\"\" width=\"25\" height=\"25\" viewBox=\"0 0 24 24\" class=\"w-6 h-6 inline-block mb-1\">\n  <g data-v-7cfb45cd=\"\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\">\n    <path data-v-7cfb45cd=\"\" fill=\"currentColor\" d=\"M3 0V3H0V5H3V8H5V5H8V3H5V0H3M10 3V5H19V7H13C11.9 7 11 7.9 11 9V15C11 16.1 11.9 17 13 17H19V19H5V10H3V19C3 20.1 3.89 21 5 21H19C20.1 21 21 20.1 21 19V16.72C21.59 16.37 22 15.74 22 15V9C22 8.26 21.59 7.63 21 7.28V5C21 3.9 20.1 3 19 3H10M13 9H20V15H13V9M16 10.5A1.5 1.5 0 0 0 14.5 12A1.5 1.5 0 0 0 16 13.5A1.5 1.5 0 0 0 17.5 12A1.5 1.5 0 0 0 16 10.5Z\"></path>\n  </g>\n</svg>', 'user', 0, 1, '2024-06-30 18:52:26', '2024-06-30 18:52:26'),
(5, 'My Orders', '/orders', '<svg data-v-7cfb45cd=\"\" width=\"25\" height=\"25\" viewBox=\"0 0 24 24\" class=\"w-6 h-6 inline-block mb-1\">\n  <g data-v-7cfb45cd=\"\" fill=\"none\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" stroke=\"currentColor\">\n    <path data-v-7cfb45cd=\"\" d=\"M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z\"></path>\n  </g>\n</svg>', 'user', 0, 1, '2024-06-30 18:52:51', '2024-06-30 18:52:51'),
(6, 'My Codes', '/codes', '<svg data-v-7cfb45cd=\"\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" class=\"css-i6dzq1 inline-block mb-1\" stroke=\"currentColor\" stroke-width=\"2\" fill=\"none\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect data-v-7cfb45cd=\"\" x=\"3\" y=\"3\" width=\"7\" height=\"7\"></rect> <rect data-v-7cfb45cd=\"\" x=\"14\" y=\"3\" width=\"7\" height=\"7\"></rect> <rect data-v-7cfb45cd=\"\" x=\"14\" y=\"14\" width=\"7\" height=\"7\"></rect> <rect data-v-7cfb45cd=\"\" x=\"3\" y=\"14\" width=\"7\" height=\"7\"></rect></svg>', 'user', 0, 1, '2024-06-30 18:53:13', '2024-06-30 18:53:13'),
(7, 'Account', '/account', '<svg data-v-7cfb45cd=\"\" width=\"25\" height=\"25\" viewBox=\"0 0 42 42\" class=\"inline-block mb-1\"><g data-v-7cfb45cd=\"\" stroke=\"none\" stroke-width=\"1\" fill=\"none\" fill-rule=\"evenodd\"><path data-v-7cfb45cd=\"\" d=\"M14.7118754,20.0876892 L8.03575361,20.0876892 C5.82661462,20.0876892 4.03575361,18.2968282 4.03575361,16.0876892 L4.03575361,12.031922 C4.03575361,8.1480343 6.79157254,4.90780265 10.4544842,4.15995321 C8.87553278,8.5612583 8.1226025,14.3600511 10.9452499,15.5413938 C13.710306,16.6986332 14.5947501,18.3118357 14.7118754,20.0876892 Z M14.2420017,23.8186831 C13.515543,27.1052019 12.7414284,30.2811559 18.0438552,31.7330419 L18.0438552,33.4450645 C18.0438552,35.6542035 16.2529942,37.4450645 14.0438552,37.4450645 L9.90612103,37.4450645 C6.14196811,37.4450645 3.09051926,34.3936157 3.09051926,30.6294627 L3.09051926,27.813861 C3.09051926,25.604722 4.88138026,23.813861 7.09051926,23.813861 L14.0438552,23.813861 C14.1102948,23.813861 14.1763561,23.8154808 14.2420017,23.8186831 Z M20.7553776,32.160536 C23.9336213,32.1190063 23.9061943,29.4103976 33.8698747,31.1666916 C34.7935223,31.3295026 35.9925894,31.0627305 37.3154077,30.4407183 C37.09778,34.8980343 33.4149547,38.4450645 28.9036761,38.4450645 C24.9909035,38.4450645 21.701346,35.7767637 20.7553776,32.160536 Z\" fill=\"currentColor\" opacity=\"0.1\"></path> <g data-v-7cfb45cd=\"\" transform=\"translate(2.000000, 3.000000)\"><path data-v-7cfb45cd=\"\" d=\"M8.5,1 C4.35786438,1 1,4.35786438 1,8.5 L1,13 C1,14.6568542 2.34314575,16 4,16 L13,16 C14.6568542,16 16,14.6568542 16,13 L16,4 C16,2.34314575 14.6568542,1 13,1 L8.5,1 Z\" stroke=\"currentColor\" stroke-width=\"2\"></path> <path data-v-7cfb45cd=\"\" d=\"M4,20 C2.34314575,20 1,21.3431458 1,23 L1,27.5 C1,31.6421356 4.35786438,35 8.5,35 L13,35 C14.6568542,35 16,33.6568542 16,32 L16,23 C16,21.3431458 14.6568542,20 13,20 L4,20 Z\" stroke=\"currentColor\" stroke-width=\"2\"></path> <path data-v-7cfb45cd=\"\" d=\"M23,1 C21.3431458,1 20,2.34314575 20,4 L20,13 C20,14.6568542 21.3431458,16 23,16 L32,16 C33.6568542,16 35,14.6568542 35,13 L35,8.5 C35,4.35786438 31.6421356,1 27.5,1 L23,1 Z\" stroke=\"currentColor\" stroke-width=\"2\"></path> <path data-v-7cfb45cd=\"\" d=\"M34.5825451,33.4769886 L38.3146092,33.4322291 C38.8602707,33.4256848 39.3079219,33.8627257 39.3144662,34.4083873 C39.3145136,34.4123369 39.3145372,34.4162868 39.3145372,34.4202367 L39.3145372,34.432158 C39.3145372,34.9797651 38.8740974,35.425519 38.3265296,35.4320861 L34.5944655,35.4768456 C34.048804,35.4833899 33.6011528,35.046349 33.5946085,34.5006874 C33.5945611,34.4967378 33.5945375,34.4927879 33.5945375,34.488838 L33.5945375,34.4769167 C33.5945375,33.9293096 34.0349773,33.4835557 34.5825451,33.4769886 Z\" fill=\"currentColor\" transform=\"translate(36.454537, 34.454537) rotate(-315.000000) translate(-36.454537, -34.454537) \"></path> <circle data-v-7cfb45cd=\"\" stroke=\"currentColor\" stroke-width=\"2\" cx=\"27.5\" cy=\"27.5\" r=\"7.5\"></circle></g></g></svg>', 'both', 0, 1, '2024-06-30 18:53:45', '2024-06-30 18:53:45');

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '2014_10_12_000000_create_users_table', 1),
(2, '2014_10_12_100000_create_password_reset_tokens_table', 1),
(3, '2019_08_19_000000_create_failed_jobs_table', 1),
(4, '2019_12_14_000001_create_personal_access_tokens_table', 1),
(5, '2022_12_14_083707_create_settings_table', 1),
(6, '2024_01_05_061344_create_media_table', 1),
(7, '2024_01_05_131145_create_pages_table', 1),
(8, '2024_01_05_131543_create_popups_table', 1),
(9, '2024_01_05_153517_create_deposits_table', 1),
(10, '2024_01_05_153552_create_products_table', 1),
(11, '2024_01_05_153632_create_sliders_table', 1),
(12, '2024_01_05_153653_create_transactions_table', 1),
(13, '2024_01_05_153738_create_variations_table', 1),
(14, '2024_01_05_153813_create_vouchers_table', 1),
(15, '2024_01_05_153814_create_orders_table', 1),
(16, '2024_01_16_060402_create_general_settings', 1),
(17, '2024_03_10_112630_create_jobs_table', 1),
(18, '2024_04_23_071649_create_menus_table', 1),
(19, '2024_06_28_151327_create_auto_vouchers_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `product_id` bigint(20) UNSIGNED DEFAULT NULL,
  `variation_id` bigint(20) UNSIGNED DEFAULT NULL,
  `amount` decimal(16,2) NOT NULL DEFAULT 0.00,
  `delivery_message` text DEFAULT NULL,
  `account_info` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`account_info`)),
  `provider_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`provider_data`)),
  `voucher_code` text DEFAULT NULL,
  `track_id` varchar(25) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `attempts` tinyint(4) NOT NULL DEFAULT 0,
  `status` enum('completed','processing','auto-processing','hold','pending','cancelled') NOT NULL DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `profit` decimal(16,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `product_id`, `variation_id`, `amount`, `delivery_message`, `account_info`, `provider_data`, `voucher_code`, `track_id`, `quantity`, `attempts`, `status`, `created_at`, `updated_at`, `deleted_at`, `profit`) VALUES
(146, 3976, 36, 253, 19.00, NULL, '{\"player_id\":\"5161949494\"}', NULL, NULL, 'H3K8Q5SU55FP', 1, 0, 'pending', '2025-08-18 01:09:04', '2025-08-18 01:12:39', '2025-08-18 01:12:39', 19.00),
(147, 3976, 36, 253, 19.00, NULL, '{\"player_id\":\"5161949494\"}', NULL, NULL, '9937YE3NJJF2', 1, 0, 'pending', '2025-08-18 01:09:26', '2025-08-18 01:12:35', '2025-08-18 01:12:35', 19.00),
(148, 3976, 36, 253, 19.00, NULL, '{\"player_id\":\"\\u09eb\\u09ea\\u09ef\\u09ea\\u09ef\\u09ea\"}', NULL, NULL, '8CZ1CKBFT8AO', 1, 0, 'pending', '2025-08-18 01:11:37', '2025-08-18 01:12:43', '2025-08-18 01:12:43', 19.00),
(149, 3976, 36, 253, 19.00, NULL, '{\"player_id\":\"5885588\"}', NULL, NULL, '5645RBNEXV77', 1, 0, 'pending', '2025-08-18 01:29:38', '2025-08-18 01:29:38', NULL, 19.00),
(150, 3978, 36, 253, 19.00, NULL, '{\"player_id\":\"9577946881\"}', NULL, NULL, 'N5BKX4RY7X22', 1, 0, 'pending', '2025-08-18 13:10:56', '2025-08-18 13:10:56', NULL, 19.00),
(151, 1, 36, 253, 19.00, NULL, '{\"player_id\":\"5885588\"}', NULL, NULL, '5FG5T2TQ6QJ7', 1, 0, 'pending', '2025-08-18 13:24:24', '2025-08-18 13:24:24', NULL, 19.00),
(152, 3978, 36, 253, 19.00, NULL, '{\"player_id\":\"9577946881\"}', NULL, NULL, '5J8XGYOXJS86', 1, 0, 'pending', '2025-08-18 13:47:43', '2025-08-18 13:47:43', NULL, 19.00),
(153, 3978, 36, 253, 19.00, NULL, '{\"player_id\":\"9577946881\"}', NULL, NULL, '87939T823J5U', 1, 0, 'pending', '2025-08-18 13:49:54', '2025-08-18 13:49:54', NULL, 19.00),
(154, 1, 37, 254, 320.00, NULL, '{\"player_id\":\"2523798928\"}', NULL, NULL, '73UYFU3NS33M', 1, 0, 'pending', '2025-08-18 14:27:45', '2025-08-18 14:27:45', NULL, 20.00),
(155, 1, 37, 254, 320.00, NULL, '{\"player_id\":\"2523798928\"}', NULL, NULL, 'JGM9MDRTTXSS', 1, 0, 'processing', '2025-08-18 14:40:51', '2025-08-18 14:40:51', NULL, 20.00),
(156, 1, 36, 253, 19.00, NULL, '{\"player_id\":\"2523798929\"}', NULL, NULL, 'YXB34A7FRQTV', 1, 0, 'processing', '2025-08-18 14:45:15', '2025-08-18 14:45:15', NULL, 19.00),
(157, 1, 36, 253, 19.00, NULL, '{\"player_id\":\"9577946881\"}', NULL, NULL, 'T8MVGBNSFCFV', 1, 0, 'processing', '2025-08-18 14:47:00', '2025-08-18 14:47:00', NULL, 19.00),
(158, 3980, 36, 253, 19.00, NULL, '{\"player_id\":\"9577946881\"}', NULL, NULL, '4E6ZOR7SBPO7', 1, 0, 'pending', '2025-08-18 14:54:34', '2025-08-18 14:54:34', NULL, 19.00);

-- --------------------------------------------------------

--
-- Table structure for table `pages`
--

CREATE TABLE `pages` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `order_column` int(11) NOT NULL DEFAULT 0,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pages`
--

INSERT INTO `pages` (`id`, `title`, `slug`, `content`, `order_column`, `status`, `created_at`, `updated_at`) VALUES
(2, 'Tutorial', 'tutorials', '<h2>কিভাবে আমাদের ওয়েবসাইটে একাউন্ট খুলবেন?</h2><p>ভিডিও দেখতে ক্লিক করুন- See Video</p><h2>কিভাবে ওয়ালেটে টাকা এড করবেন?</h2><p>ভিডিও দেখতে ক্লিক করুন- See Video</p><h2>কিভাবে ওয়ালেট ব্যবহার করে অর্ডার করবেন?</h2><p>ভিডিও দেখতে ক্লিক করুন- See Video</p><h2>কিভাবে গুগল ব্যাকআপ কোড পাবেন?</h2><p>ভিডিও দেখতে ক্লিক করুন- See Video</p><h2>কিভাবে ফেসবুক ব্যাকআপ কোড পাবেন?</h2><p>ভিডিও দেখতে ক্লিক করুন- See Video</p>', 1, 1, '2024-07-01 09:36:02', '2024-07-03 07:04:28'),
(3, 'Terms And Conditions', 'terms-and-conditions', '<h2>নিয়ম ও শর্তাবলী</h2><h3>পরিচিতিঃ-</h3><p>বিডি গেমস্ বাজার এ আপনাকে স্বাগতম। বিডি গেমস্ বাজার দ্বারা পরিচালিত এই সাইট ব্যবহার করার আগে অনুগ্রহ করে এই ব্যবহারকারীর শর্তগুলি পড়ুন। আমরা আমাদের পণ্য বিক্রয়ের উদ্দেশ্যে এই সাইটটি পরিচালনা করি। আপনি যদি আমাদের পণ্যগুলো ক্রয় করতে আগ্রহী হন তবে আমাদের শর্তাবলির সাথে সম্মত হওয়া বাধ্যতামূলক।</p><h3>প্রোডাক্ট বিক্রয়ঃ-</h3><p>বিডি গেমস্ বাজার ওয়েবসাইটে শুধুমাত্র ভার্চুয়াল বা ডিজিটাল পণ্য বিক্রয় করা হয়। এক্ষেত্রে আমরা বিভিন্ন গেমস এর মূদ্রা ক্রয় করতে বিভিন্ন রকম কারেন্সি ব্যবহার করে থাকি যেমন:(BDT/USD/AUD/RS)। এবং সেসব কারেন্সি ব্যবহার করে আমরা ব্যবহারকারীর পছন্দমতো পণ্য তাদের কাছে ভার্চুয়ালি ডেলিভার করে থাকি। এছাড়াও আমরা ব্যবহারকারীর ভার্চুয়াল ওয়ালেটে কারেন্সি ও প্রদান করে থাকি।</p><h3>ডেলিভারির সময়সীমাঃ-</h3><p>বিডি গেমস্ বাজার এর সকল ভার্চুয়াল প্রোডাক্ট অথবা ডিজিটাল প্রোডাক্ট ডেলিভারির সময়সীমা ১-১০ মিনিট। কোনো যান্ত্রিক ত্রুটি অথবা ওয়েবসাইট কর্মকর্তাদের কোনো সমস্যার কারণে ডেলিভারি সময়ে কিছুটা পরিবর্তন আসতে পারে তবে এ পরিবর্তন অবশ্যই ২৪ ঘন্টার বেশি নয়। এককথায় কোনো সমস্যা না থাকলে আমরা ১-১০ মিনিটের মধ্যে অর্ডারগুলো সম্পন্ন করে থাকি।</p><h3>রিটার্ন এবং রিফান্ড নীতিঃ-</h3><p><strong>রিফান্ড নীতি-</strong> ওয়েবসাইটের ওয়ালেটে টাকা এড করার পর সেটি দিয়ে আপনি ওয়েবসাইটের যেকোনো প্রোডাক্ট অর্ডার করতে পারবেন তবে ওয়ালেটের টাকা উত্তোলন করা সম্ভব নয়। আমাদের সিস্টেমে কোনো সমস্যা হওয়ার কারনে যদি আপনার অর্ডার এ ব্যঘাত ঘটে তাহলে আমরা সেই অর্ডারের সম্পূর্ন মূল্য আপনার ওয়েবসাইট ওয়ালেটে রিফান্ড দিয়ে দিবো। এছাড়াও আপনার গেম আইডি অথবা ডিজিটাল প্রোডাক্ট ডেলিভারির আইডি তে যদি কোনো সমস্যা থেকে থাকে এবং উক্ত সমস্যার কারণে যদি আমরা আপনার অর্ডার টি ডেলিভারি না করতে পারি তাহলেও আপনাকে আপনার প্রোডাক্ট এর সম্পূর্ণ মূল্য ওয়েবসাইট ওয়ালেটে রিফান্ড দেওয়া হবে।</p><p><strong>রিটার্ন নীতি-</strong> যেহেতু আমাদের ওয়েবসাইট পুরোপুরি ভার্চুয়াল এবং ডিজিটাল পণ্য বিক্রয় করে থাকে সেহেতু আমাদের কোনো প্রোডাক্ট রিটার্ন নেওয়া সম্ভব নয়। প্রোডাক্ট ডেলিভারির পর সম্পূর্ণ দায়ভার ওয়েবসাইট ব্যবহারকারীদের নেওয়া বাধ্যতামূলক।</p><h3>বিক্রয় পরবর্তী সেবাঃ-</h3><p>সার্ভিস এবং প্রোডাক্ট বিক্রয়ের পর আমরা ব্যবহারকারীদের প্রোডাক্ট সম্পর্কে তথ্য অথবা প্রোডাক্ট এর বিবরণ এবং প্রোডাক্ট ব্যবহার করা সম্পর্কে সহ যতটুকু সম্ভব সেবা দিয়ে থাকি। তবে প্রোডাক্ট বহির্ভূত কোনো সেবা আমরা প্রোডাক্ট বিক্রয়ের পর দিয়ে থাকি না।</p><p><br></p>', 3, 1, '2024-07-03 07:02:56', '2024-07-03 07:04:28'),
(4, 'Return And Refund Policy', 'return-and-refund-policy', '<h3>রিফান্ড পলিসিঃ-</h3><p>ওয়েবসাইটের ওয়ালেটে টাকা এড করার পর সেটি দিয়ে আপনি ওয়েবসাইটের যেকোনো প্রডাক্ট অর্ডার করতে পারবেন তবে ওয়ালেটের টাকা উত্তোলন করা সম্ভব নয়। আমাদের সিস্টেমে কোনো সমস্যা হওয়ার কারনে যদি আপনার অর্ডার এ ব্যঘাত ঘটে তাহলে আমরা সেই অর্ডারের সম্পূর্ন মূল্য আপনার ওয়েবসাইট ওয়ালেটে রিফান্ড দিয়ে দিবো। এছাড়াও আপনার গেম আইডি অথবা ডিজিটাল প্রোডাক্ট ডেলিভারির আইডি তে যদি কোনো সমস্যা থেকে থাকে এবং উক্ত সমস্যার কারণে যদি আমরা আপনার অর্ডার টি ডেলিভারি না করতে পারি তাহলেও আপনাকে আপনার প্রোডাক্ট এর সম্পূর্ণ মূল্য ওয়েবসাইট ওয়ালেটে রিফান্ড দেওয়া হবে।</p><h3>রিটার্ন পলিসিঃ-</h3><p>যেহেতু আমাদের ওয়েবসাইট পুরোপুরি ভার্চুয়াল এবং ডিজিটাল পণ্য বিক্রয় করে থাকে সেহেতু আমাদের কোনো প্রোডাক্ট রিটার্ন নেওয়া সম্ভব নয়। প্রোডাক্ট ডেলিভারির পর সম্পূর্ণ দায়ভার ওয়েবসাইট কাস্টমারের।</p><h3>সার্ভিস এবং প্রোডাক্ট বিক্রয়ের পর সেবাঃ-</h3><p>সার্ভিস এবং প্রোডাক্ট বিক্রয়ের পর আমরা আপনাকে প্রোডাক্ট সম্পর্কে তথ্য অথবা প্রোডাক্ট এর বিবরণ সহ যতটুকু সম্ভব সেবা দিয়ে থাকি। তবে নিয়ম বহির্ভূত কোনো সেবা আমরা প্রোডাক্ট বিক্রয়ের পর দিয়ে থাকি না।</p><p><br></p>', 4, 1, '2024-07-03 07:03:20', '2024-07-03 07:04:28'),
(5, 'Contact Us', 'contact-us', '<h1>Start a Conversation</h1><p><br></p><p><br></p><p>Whatsapphttps://wa.me/message/DSO5225YDAAVG1</p><p>No time to wait around? we us usally respond within a few minutes.</p><p><br></p><p><br></p><p>Phone : 01797385660</p><p>we re online right a few now, talk with are team in real time.</p><p><br></p><p>Email fftopupzone0@gmail.com</p><p>No time to wait around? we us usally respond within a few hours.</p><p><br></p>', 2, 1, '2024-07-03 07:04:12', '2025-08-18 11:53:04');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `password_reset_tokens`
--

INSERT INTO `password_reset_tokens` (`email`, `token`, `created_at`) VALUES
('alviahmed@gmail.com', '$2y$12$R.o7zRNf7oVXUwPiOHyGi.tLj9ctqrmC1Kn.7HVViw5QJbDHtqoOm', '2025-08-18 14:51:26');

-- --------------------------------------------------------

--
-- Table structure for table `personal_access_tokens`
--

CREATE TABLE `personal_access_tokens` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `tokenable_type` varchar(255) NOT NULL,
  `tokenable_id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `token` varchar(64) NOT NULL,
  `abilities` text DEFAULT NULL,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `expires_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `popups`
--

CREATE TABLE `popups` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `button_text` varchar(255) DEFAULT NULL,
  `type` enum('once','daily') NOT NULL DEFAULT 'once',
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `title` text NOT NULL,
  `slug` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `type` enum('ingame','topup','voucher','subscription') NOT NULL,
  `percentage` int(11) DEFAULT 0,
  `order_column` int(11) NOT NULL DEFAULT 0,
  `categorie_id` varchar(255) NOT NULL DEFAULT '1',
  `input` varchar(255) DEFAULT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `uid_checker` tinyint(1) NOT NULL DEFAULT 0,
  `has_tutorial` tinyint(1) NOT NULL DEFAULT 0,
  `tutorial_link` varchar(1024) DEFAULT NULL,
  `tutorial_text` varchar(1024) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `title`, `slug`, `content`, `type`, `percentage`, `order_column`, `categorie_id`, `input`, `status`, `created_at`, `updated_at`, `uid_checker`, `has_tutorial`, `tutorial_link`, `tutorial_text`) VALUES
(36, 'Free Fire Uid Top Up', 'ff', '<ul><li><em>শুধুমাত্র Bangladesh সার্ভারে ID Code দিয়ে টপ আপ হবে।</em></li><li><em>Player ID Code ভুল দিয়ে Diamond না পেলে&nbsp; RED TOP কর্তৃপক্ষ দায়ী নয় ।</em></li><li><em>Order কমপ্লিট হওয়ার পরেও আইডিতে ডাইমন্ড না গেলে চেক করার জন্য ID Pass দিতে হবে।</em><br><em>অর্ডার Cancel হলে কি কারণে তা Cancel হয়েছে তা অর্ডার হিস্টোরিতে দেওয়া থাকে অনুগ্রহ পুর্বক দেখে পুনরায় সঠিক তথ্য দিয়ে অর্ডার করবেন।</em></li></ul><p>STAY CONNECTED</p><p><br></p>', 'topup', 0, 0, '7', 'Enter Video Url', 1, '2025-08-17 23:00:45', '2025-08-17 23:35:10', 1, 0, NULL, NULL),
(37, 'Weekly/ Monthly Discount Offer', 'weekly-monthly', '<ul><li><em>শুধুমাত্র Bangladesh সার্ভারে ID Code দিয়ে টপ আপ হবে।</em></li><li><em>Player ID Code ভুল দিয়ে Diamond না পেলে&nbsp; Red Topup</em><figure data-trix-attachment=\"{&quot;contentType&quot;:&quot;image/jpeg&quot;,&quot;filename&quot;:&quot;Screenshot_2025-08-18-00-20-51-31_948cd9899890cbd5c2798760b2b95377.jpg&quot;,&quot;filesize&quot;:151555,&quot;height&quot;:716,&quot;href&quot;:&quot;https://redtopup.top/uploads/gC2gWBoRFEINFrV4lnGj0wALZAR749JtnGpIpvaj.jpg&quot;,&quot;url&quot;:&quot;https://redtopup.top/uploads/gC2gWBoRFEINFrV4lnGj0wALZAR749JtnGpIpvaj.jpg&quot;,&quot;width&quot;:720}\" data-trix-content-type=\"image/jpeg\" data-trix-attributes=\"{&quot;presentation&quot;:&quot;gallery&quot;}\" class=\"attachment attachment--preview attachment--jpg\"><a href=\"https://redtopup.top/uploads/gC2gWBoRFEINFrV4lnGj0wALZAR749JtnGpIpvaj.jpg\"><img src=\"https://redtopup.top/uploads/gC2gWBoRFEINFrV4lnGj0wALZAR749JtnGpIpvaj.jpg\" width=\"720\" height=\"716\"><figcaption class=\"attachment__caption\"><span class=\"attachment__name\">Screenshot_2025-08-18-00-20-51-31_948cd9899890cbd5c2798760b2b95377.jpg</span> <span class=\"attachment__size\">148 KB</span></figcaption></a></figure><em> কর্তৃপক্ষ দায়ী নয় ।</em></li><li><em>Order কমপ্লিট হওয়ার পরেও আইডিতে ডাইমন্ড না গেলে চেক করার জন্য ID Pass দিতে হবে।</em><br><em>অর্ডার Cancel হলে কি কারণে তা Cancel হয়েছে তা অর্ডার হিস্টোরিতে দেওয়া থাকে অনুগ্রহ পুর্বক দেখে পুনরায় সঠিক তথ্য দিয়ে অর্ডার করবেন।</em></li></ul><p>STAY CONNECTED</p><p><br></p>', 'topup', 0, 0, '5', 'Enter Video Url', 1, '2025-08-18 00:26:12', '2025-08-18 14:26:59', 1, 0, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `group` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `locked` tinyint(1) NOT NULL DEFAULT 0,
  `payload` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`payload`)),
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `settings`
--

INSERT INTO `settings` (`id`, `group`, `name`, `locked`, `payload`, `created_at`, `updated_at`) VALUES
(1, 'general', 'site_name', 0, '\"RED TOP UP \"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(2, 'general', 'site_title', 0, '\"Buy Free Fire Diamonds Easily\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(3, 'general', 'home_title', 0, '\"Home - RED TOP UP\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(4, 'general', 'paginate_per_page', 0, '20', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(5, 'general', 'logo', 0, '\"settings\\/01K2WKPQ3WK1AWXTFWBH2X41N3.png\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(6, 'general', 'favicon', 0, '\"settings\\/01K2WGVBJH6EHYW99A8FJGVZSE.jpg\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(7, 'general', 'add_money_video_link', 0, '\"https:\\/\\/youtu.be\\/\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(8, 'general', 'backup_code_video_link', 0, '\"https:\\/\\/youtu.be\\/\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(9, 'general', 'tutorial_video_link', 0, '\"https:\\/\\/youtu.be\\/\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(10, 'general', 'google_client_id', 0, '\"########\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(11, 'general', 'google_client_secret', 0, '\"########\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(12, 'general', 'header_tags', 0, 'null', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(13, 'general', 'footer_js', 0, 'null', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(14, 'general', 'wallet', 0, 'true', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(15, 'general', 'smtp_from_address', 0, '\"redtopup@boibiponi.com\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(16, 'general', 'smtp_host', 0, '\"mail.boibiponi.com\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(17, 'general', 'smtp_port', 0, '\"465\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(18, 'general', 'smtp_username', 0, '\"redtopup@boibiponi.com\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(19, 'general', 'smtp_password', 0, '\"Alvi_2002\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(20, 'general', 'uddoktapay_api_key', 0, '\"########\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(21, 'general', 'uddoktapay_api_url', 0, '\"Ggg\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(22, 'general', 'uddoktapay_min_amount', 0, '10', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(23, 'general', 'uddoktapay_max_amount', 0, '10000', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(24, 'general', 'facebook_link', 0, '\"https:\\/\\/facebook.com\\/\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(25, 'general', 'youtube_link', 0, '\"https:\\/\\/www.youtube.com\\/\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(26, 'general', 'messenger_link', 0, '\"https:\\/\\/wa.me\\/\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(27, 'general', 'whatsapp_number', 0, '\"01935096812\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(28, 'general', 'support_number', 0, '\"01797385660\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(29, 'general', 'email_address', 0, '\"rxcodecommunity@gmail.com\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(30, 'general', 'support_time', 0, '\"9AM - 10PM\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(31, 'general', 'background_image', 0, 'true', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(32, 'general', 'footer_menu', 0, 'true', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(33, 'general', 'theme_color', 0, '\"#4627ab\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(34, 'general', 'logo_color', 0, '\"#362194\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(35, 'general', 'background_color', 0, '\"#f8f9fc\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(36, 'general', 'font_color', 0, '\"#000000\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(37, 'general', 'navigation_background_color', 0, '\"rgba(255, 255, 255, 0.3)\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(38, 'general', 'navigation_font_color', 0, '\"#131da1\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(39, 'general', 'footer_color', 0, '\"#6e3fba\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(40, 'general', 'footer_font_color', 0, '\"#f2f2f2\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(41, 'general', 'content_box_color', 0, '\"#ffffff\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(42, 'general', 'notice_background_color', 0, '\"#6b2096\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(43, 'general', 'notice_font_color', 0, '\"#ffffff\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(44, 'general', 'seo_description', 0, '\"Rx Code Community \\u0986\\u09ae\\u09be\\u09a6\\u09c7\\u09b0 \\u09b8\\u09be\\u09b0\\u09cd\\u09ad\\u09bf\\u09b8 \\u09e8\\u09ea \\u0998\\u09a8\\u09cd\\u099f\\u09be \\u0996\\u09cb\\u09b2\\u09be \\u09a5\\u09be\\u0995\\u09c7\\u0964 :- \\u0986\\u09aa\\u09a8\\u09be\\u09b0\\u09be \\u09b0\\u09be\\u09a4-\\u09a6\\u09bf\\u09a8 \\u09e8\\u09ea \\u0998\\u09a8\\u09cd\\u099f\\u09be \\u09e7 \\u09ae\\u09bf\\u09a8\\u09bf\\u099f\\u09c7\\u09b0 \\u09ae\\u09a7\\u09cd\\u09af\\u09c7 \\u0985\\u09b0\\u09cd\\u09a1\\u09be\\u09b0 \\u0995\\u09ae\\u09aa\\u09cd\\u09b2\\u09bf\\u099f \\u09aa\\u09c7\\u09df\\u09c7 \\u09af\\u09be\\u09ac\\u09c7\\u09a8\\u0964 \\u09af\\u09c7\\u0995\\u09cb\\u09a8\\u09cb \\u09b8\\u09ae\\u09b8\\u09cd\\u09af\\u09be\\u09df \\u09b9\\u09b2\\u09c7 \\u0986\\u09ae\\u09be\\u09a6\\u09c7\\u09b0 \\u09b9\\u09cb\\u09af\\u09bc\\u09be\\u099f\\u09b8\\u0985\\u09cd\\u09af\\u09be\\u09aa-\\u098f \\u09ae\\u09c7\\u09b8\\u09c7\\u099c \\u09a6\\u09bf\\u09a8\\u0964\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(45, 'general', 'seo_keywords', 0, '\"\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(46, 'general', 'fb_og_image', 0, 'null', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(47, 'general', 'twitter_og_image', 0, 'null', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(48, 'general', 'enable_notice', 0, 'false', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(49, 'general', 'notice_title', 0, '\"Rx Code Community\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(50, 'general', 'notice_content', 0, '\"\\u200c\\u221a \\u00ae\\u0986\\u09ae\\u09be\\u09a6\\u09c7\\u09b0 \\u09b8\\u09be\\u09b0\\u09cd\\u09ad\\u09bf\\u09b8 \\u09e8\\u09ea \\u0998\\u09a8\\u09cd\\u099f\\u09be \\u0996\\u09cb\\u09b2\\u09be \\u09a5\\u09be\\u0995\\u09c7\\u0964 \\u0986\\u09aa\\u09a8\\u09be\\u09b0\\u09be \\u09b0\\u09be\\u09a4-\\u09a6\\u09bf\\u09a8 \\u09e8\\u09ea \\u0998\\u09a8\\u09cd\\u099f\\u09be \\u09e7 \\u09ae\\u09bf\\u09a8\\u09bf\\u099f\\u09c7\\u09b0 \\u09ae\\u09a7\\u09cd\\u09af\\u09c7 \\u0985\\u09b0\\u09cd\\u09a1\\u09be\\u09b0 \\u0995\\u09ae\\u09aa\\u09cd\\u09b2\\u09bf\\u099f \\u09aa\\u09c7\\u09df\\u09c7 \\u09af\\u09be\\u09ac\\u09c7\\u09a8\\u0964 \\u09af\\u09c7\\u0995\\u09cb\\u09a8\\u09cb \\u09b8\\u09ae\\u09b8\\u09cd\\u09af\\u09be\\u09df \\u09b9\\u09b2\\u09c7 \\u0986\\u09ae\\u09be\\u09a6\\u09c7\\u09b0 \\u09b9\\u09cb\\u09af\\u09bc\\u09be\\u099f\\u09b8\\u0985\\u09cd\\u09af\\u09be\\u09aa-\\u098f \\u09ae\\u09c7\\u09b8\\u09c7\\u099c\\u0964 \"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(51, 'general', 'base_currency', 0, '\"BDT\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(52, 'general', 'currency_symbol', 0, '\"\\u09f3\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(53, 'general', 'enable_pwa', 0, 'true', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(54, 'general', 'pwa_icon', 0, '\"settings\\/01K2XZRDJ1WHDFMAYDYCKS6KGM.png\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(55, 'general', 'enable_uid_checker', 0, 'true', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(56, 'general', 'enable_auto_topup', 0, 'false', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(57, 'general', 'topup_provider', 0, '\"FreeFire\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(58, 'general', 'free_fire_server_url', 0, '\"https:\\/\\/t.me\\/crazy_lab_bd\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(59, 'general', 'free_fire_server_api_key', 0, '\"https:\\/\\/t.me\\/crazy_lab_bd\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(60, 'general', 'version', 0, '\"1.1.4\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(8430, 'general', 'telegram_bot_token', 0, '\"########\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33'),
(8431, 'general', 'telegram_chat_id', 0, '\"########\"', '2024-06-30 17:25:57', '2025-08-18 14:41:33');

-- --------------------------------------------------------

--
-- Table structure for table `sliders`
--

CREATE TABLE `sliders` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `order_column` int(11) NOT NULL DEFAULT 0,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sliders`
--

INSERT INTO `sliders` (`id`, `url`, `order_column`, `status`, `created_at`, `updated_at`) VALUES
(9, NULL, 0, 1, '2025-08-18 12:08:22', '2025-08-18 12:08:22');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `order_id` bigint(20) UNSIGNED DEFAULT NULL,
  `deposit_id` bigint(20) UNSIGNED DEFAULT NULL,
  `amount` decimal(16,2) NOT NULL DEFAULT 0.00,
  `payment_method` varchar(55) NOT NULL,
  `transaction_id` varchar(55) NOT NULL,
  `trx_type` enum('+','-') NOT NULL DEFAULT '-',
  `remarks` text NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `user_id`, `order_id`, `deposit_id`, `amount`, `payment_method`, `transaction_id`, `trx_type`, `remarks`, `created_at`, `updated_at`) VALUES
(97, 1, 155, NULL, 320.00, 'wallet', '2XP9SU6O35RV', '-', 'Product is being purchased using the wallet, Order ID: 155', '2025-08-18 14:40:51', '2025-08-18 14:40:51'),
(98, 1, 156, NULL, 19.00, 'wallet', '8Q9GP88AKO85', '-', 'Product is being purchased using the wallet, Order ID: 156', '2025-08-18 14:45:15', '2025-08-18 14:45:15'),
(99, 1, 157, NULL, 19.00, 'wallet', '79KGC8YQJGGF', '-', 'Product is being purchased using the wallet, Order ID: 157', '2025-08-18 14:47:00', '2025-08-18 14:47:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `role` enum('user','admin') NOT NULL DEFAULT 'user',
  `balance` decimal(16,2) NOT NULL DEFAULT 0.00,
  `password` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `gauth_id` varchar(255) DEFAULT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `is_reseller` tinyint(1) NOT NULL DEFAULT 0,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `phone`, `role`, `balance`, `password`, `email_verified_at`, `gauth_id`, `remember_token`, `is_reseller`, `status`, `created_at`, `updated_at`) VALUES
(1, 'Super Admin', 'admin@gmail.com', '01777777777', 'admin', 3642.00, '$2y$12$iRUhsnuHOlDk/EhhSizX/eYCvxJRgCOeype6ejZYnyINopbQumI3m', NULL, NULL, 'Mhy9aUy0xc06ggWQNTZYbedjSgHT1GeZXZhv2oNrDDeXY1OAk7u1o9xnhlpC', 0, 1, '2024-06-30 17:25:58', '2025-08-18 14:47:00'),
(3975, 'Fahad', 'fftopupzone0@gmail.com', '01797385660', 'user', 0.00, '$2y$12$7M.LpNz0pwfiGq4w.xJNc.XX9FZWDDI9znYzRSReMme2OSP.bYeOu', NULL, NULL, NULL, 0, 1, '2025-08-17 22:56:09', '2025-08-17 22:56:09'),
(3976, 'Xrfahad', 'fahadfahim853@gmail.com', '01935096812', 'user', 0.00, '$2y$12$eXhl7plapx5hNNllCKtkbO.4qw.2hgHrnluxks2FOF5R0YO/ZFq5G', NULL, NULL, NULL, 0, 1, '2025-08-17 23:25:37', '2025-08-17 23:25:37'),
(3977, 'hgwgdgg', 'hasanariyan853@gmail.com', '01322449541', 'user', 0.00, '$2y$12$IefUMw/Yg0B6lSlz5mJlFOwuPmJaBrs8iwrxULc6R5yTM2FTA4br.', NULL, NULL, NULL, 0, 1, '2025-08-18 00:29:09', '2025-08-18 00:29:09'),
(3978, 'Stub sell', 'samad@gmail.com', '01832560070', 'user', 100.00, '$2y$12$ibWxvykS8sNWxtK/Hat8f.PM7X9XnozMmmNbaPUT37.T82oMy/4C2', NULL, NULL, NULL, 0, 1, '2025-08-18 13:05:04', '2025-08-18 13:08:50'),
(3979, 'ALVI AHMED', 'alviahmed@gmail.com', '01312345678', 'user', 0.00, '$2y$12$CZryHWa4Wvnx1I2DAHLA7ee8Md0DxrRcm.Fr9HgOIuzXVTkD6VvMa', NULL, NULL, NULL, 0, 1, '2025-08-18 13:51:31', '2025-08-18 13:51:31'),
(3980, 'ridoy King', 'mobotopup.com@gmail.com', '01613953104', 'user', 0.00, '$2y$12$I8/IdUj5uF6gH15iAQTGLuwDBG6JrLvjV8rHzg98YNvPpheh1XbzG', NULL, NULL, NULL, 0, 1, '2025-08-18 14:53:36', '2025-08-18 14:53:36');

-- --------------------------------------------------------

--
-- Table structure for table `variations`
--

CREATE TABLE `variations` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `product_id` bigint(20) UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `price` decimal(16,2) NOT NULL DEFAULT 0.00,
  `stock` int(11) NOT NULL DEFAULT 0,
  `automatic` tinyint(4) NOT NULL DEFAULT 0,
  `provider` varchar(255) DEFAULT NULL,
  `provider_product_id` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `buy_rate` decimal(16,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `variations`
--

INSERT INTO `variations` (`id`, `product_id`, `title`, `price`, `stock`, `automatic`, `provider`, `provider_product_id`, `created_at`, `updated_at`, `buy_rate`) VALUES
(253, 36, '25 Diamond', 19.00, 9998, 0, NULL, NULL, '2025-08-18 01:08:41', '2025-08-18 14:47:00', 0.00),
(254, 37, '2x Weekly', 320.00, 19, 0, NULL, NULL, '2025-08-18 14:25:38', '2025-08-18 14:40:51', 300.00);

-- --------------------------------------------------------

--
-- Table structure for table `visitors`
--

CREATE TABLE `visitors` (
  `id` int(11) NOT NULL,
  `ip_address` varchar(45) NOT NULL,
  `visited_at` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `visitors`
--

INSERT INTO `visitors` (`id`, `ip_address`, `visited_at`, `created_at`, `updated_at`) VALUES
(4144, '103.15.42.71', '2025-08-16', '2025-08-16 10:35:16', '2025-08-16 10:35:16'),
(4145, '103.203.178.19', '2025-08-17', '2025-08-17 16:15:26', '2025-08-17 16:15:26'),
(4146, '54.38.94.194', '2025-08-17', '2025-08-17 16:15:52', '2025-08-17 16:15:52'),
(4147, '196.251.72.125', '2025-08-17', '2025-08-17 16:15:58', '2025-08-17 16:15:58'),
(4148, '207.46.13.9', '2025-08-17', '2025-08-17 16:19:25', '2025-08-17 16:19:25'),
(4149, '35.202.8.234', '2025-08-17', '2025-08-17 16:20:08', '2025-08-17 16:20:08'),
(4150, '208.110.64.178', '2025-08-17', '2025-08-17 16:20:38', '2025-08-17 16:20:38'),
(4151, '217.182.158.226', '2025-08-17', '2025-08-17 16:21:22', '2025-08-17 16:21:22'),
(4152, '207.46.13.6', '2025-08-17', '2025-08-17 16:25:46', '2025-08-17 16:25:46'),
(4153, '69.197.135.226', '2025-08-17', '2025-08-17 16:26:21', '2025-08-17 16:26:21'),
(4154, '203.161.32.106', '2025-08-17', '2025-08-17 16:26:57', '2025-08-17 16:26:57'),
(4155, '104.28.208.86', '2025-08-17', '2025-08-17 16:30:16', '2025-08-17 16:30:16'),
(4156, '104.28.208.86', '2025-08-17', '2025-08-17 16:30:16', '2025-08-17 16:30:16'),
(4157, '104.28.155.26', '2025-08-17', '2025-08-17 16:30:29', '2025-08-17 16:30:29'),
(4158, '104.28.208.87', '2025-08-17', '2025-08-17 16:30:40', '2025-08-17 16:30:40'),
(4159, '103.87.250.233', '2025-08-17', '2025-08-17 16:31:56', '2025-08-17 16:31:56'),
(4160, '149.154.161.212', '2025-08-17', '2025-08-17 16:32:25', '2025-08-17 16:32:25'),
(4161, '149.154.161.217', '2025-08-17', '2025-08-17 16:32:26', '2025-08-17 16:32:26'),
(4162, '4.240.89.23', '2025-08-17', '2025-08-17 16:32:31', '2025-08-17 16:32:31'),
(4163, '52.167.144.231', '2025-08-17', '2025-08-17 16:32:47', '2025-08-17 16:32:47'),
(4164, '117.62.235.53', '2025-08-17', '2025-08-17 16:33:42', '2025-08-17 16:33:42'),
(4165, '66.249.73.198', '2025-08-17', '2025-08-17 16:34:59', '2025-08-17 16:34:59'),
(4166, '66.249.73.199', '2025-08-17', '2025-08-17 16:35:41', '2025-08-17 16:35:41'),
(4167, '204.12.252.98', '2025-08-17', '2025-08-17 16:36:05', '2025-08-17 16:36:05'),
(4168, '103.196.232.135', '2025-08-17', '2025-08-17 16:36:19', '2025-08-17 16:36:19'),
(4169, '77.223.120.93', '2025-08-17', '2025-08-17 16:38:02', '2025-08-17 16:38:02'),
(4170, '207.46.13.64', '2025-08-17', '2025-08-17 16:40:18', '2025-08-17 16:40:18'),
(4171, '103.4.251.86', '2025-08-17', '2025-08-17 16:40:30', '2025-08-17 16:40:30'),
(4172, '107.172.195.19', '2025-08-17', '2025-08-17 16:40:34', '2025-08-17 16:40:34'),
(4173, '64.15.129.101', '2025-08-17', '2025-08-17 16:40:50', '2025-08-17 16:40:50'),
(4174, '64.15.129.118', '2025-08-17', '2025-08-17 16:40:51', '2025-08-17 16:40:51'),
(4175, '192.175.111.252', '2025-08-17', '2025-08-17 16:40:54', '2025-08-17 16:40:54'),
(4176, '64.15.129.109', '2025-08-17', '2025-08-17 16:40:55', '2025-08-17 16:40:55'),
(4177, '192.175.111.241', '2025-08-17', '2025-08-17 16:40:59', '2025-08-17 16:40:59'),
(4178, '64.15.129.113', '2025-08-17', '2025-08-17 16:41:02', '2025-08-17 16:41:02'),
(4179, '64.15.129.111', '2025-08-17', '2025-08-17 16:41:03', '2025-08-17 16:41:03'),
(4180, '192.175.111.239', '2025-08-17', '2025-08-17 16:41:04', '2025-08-17 16:41:04'),
(4181, '178.239.147.98', '2025-08-17', '2025-08-17 16:43:36', '2025-08-17 16:43:36'),
(4182, '157.143.53.238', '2025-08-17', '2025-08-17 16:43:47', '2025-08-17 16:43:47'),
(4183, '34.90.37.123', '2025-08-17', '2025-08-17 16:44:14', '2025-08-17 16:44:14'),
(4184, '207.46.13.36', '2025-08-17', '2025-08-17 16:47:48', '2025-08-17 16:47:48'),
(4185, '186.194.54.93', '2025-08-17', '2025-08-17 16:49:10', '2025-08-17 16:49:10'),
(4186, '52.167.144.198', '2025-08-17', '2025-08-17 16:50:09', '2025-08-17 16:50:09'),
(4187, '18.236.211.120', '2025-08-17', '2025-08-17 16:53:28', '2025-08-17 16:53:28'),
(4188, '52.167.144.186', '2025-08-17', '2025-08-17 16:53:37', '2025-08-17 16:53:37'),
(4189, '216.55.146.53', '2025-08-17', '2025-08-17 16:54:41', '2025-08-17 16:54:41'),
(4190, '91.134.91.17', '2025-08-17', '2025-08-17 16:54:55', '2025-08-17 16:54:55'),
(4191, '103.38.55.59', '2025-08-17', '2025-08-17 16:55:06', '2025-08-17 16:55:06'),
(4192, '85.208.96.203', '2025-08-17', '2025-08-17 16:55:37', '2025-08-17 16:55:37'),
(4193, '207.46.13.78', '2025-08-17', '2025-08-17 16:56:49', '2025-08-17 16:56:49'),
(4194, '111.119.237.15', '2025-08-17', '2025-08-17 16:58:31', '2025-08-17 16:58:31'),
(4195, '103.174.50.98', '2025-08-17', '2025-08-17 17:00:08', '2025-08-17 17:00:08'),
(4196, '44.250.233.77', '2025-08-17', '2025-08-17 17:00:13', '2025-08-17 17:00:13'),
(4197, '44.249.78.50', '2025-08-17', '2025-08-17 17:00:30', '2025-08-17 17:00:30'),
(4198, '18.237.107.122', '2025-08-17', '2025-08-17 17:00:55', '2025-08-17 17:00:55'),
(4199, '35.92.246.77', '2025-08-17', '2025-08-17 17:00:55', '2025-08-17 17:00:55'),
(4200, '34.208.118.74', '2025-08-17', '2025-08-17 17:01:27', '2025-08-17 17:01:27'),
(4201, '34.221.248.178', '2025-08-17', '2025-08-17 17:05:23', '2025-08-17 17:05:23'),
(4202, '162.240.97.19', '2025-08-17', '2025-08-17 17:05:43', '2025-08-17 17:05:43'),
(4203, '162.241.126.57', '2025-08-17', '2025-08-17 17:11:16', '2025-08-17 17:11:16'),
(4204, '157.55.39.49', '2025-08-17', '2025-08-17 17:12:02', '2025-08-17 17:12:02'),
(4205, '44.244.56.212', '2025-08-17', '2025-08-17 17:13:04', '2025-08-17 17:13:04'),
(4206, '3.1.124.203', '2025-08-17', '2025-08-17 17:16:53', '2025-08-17 17:16:53'),
(4207, '103.28.116.120', '2025-08-17', '2025-08-17 17:19:09', '2025-08-17 17:19:09'),
(4208, '157.55.39.58', '2025-08-17', '2025-08-17 17:20:23', '2025-08-17 17:20:23'),
(4209, '157.245.89.176', '2025-08-17', '2025-08-17 17:22:27', '2025-08-17 17:22:27'),
(4210, '34.63.16.111', '2025-08-17', '2025-08-17 17:22:36', '2025-08-17 17:22:36'),
(4211, '3.81.221.154', '2025-08-17', '2025-08-17 17:23:56', '2025-08-17 17:23:56'),
(4212, '65.108.64.152', '2025-08-17', '2025-08-17 17:24:04', '2025-08-17 17:24:04'),
(4213, '20.229.51.198', '2025-08-17', '2025-08-17 17:25:49', '2025-08-17 17:25:49'),
(4214, '185.149.192.18', '2025-08-17', '2025-08-17 17:28:03', '2025-08-17 17:28:03'),
(4215, '199.247.0.252', '2025-08-17', '2025-08-17 17:33:27', '2025-08-17 17:33:27'),
(4216, '66.249.73.200', '2025-08-17', '2025-08-17 17:34:01', '2025-08-17 17:34:01'),
(4217, '109.123.236.202', '2025-08-17', '2025-08-17 17:39:00', '2025-08-17 17:39:00'),
(4218, '157.55.39.10', '2025-08-17', '2025-08-17 17:40:05', '2025-08-17 17:40:05'),
(4219, '213.136.93.169', '2025-08-17', '2025-08-17 17:44:32', '2025-08-17 17:44:32'),
(4220, '44.222.233.203', '2025-08-17', '2025-08-17 17:45:01', '2025-08-17 17:45:01'),
(4221, '157.55.39.200', '2025-08-17', '2025-08-17 17:46:38', '2025-08-17 17:46:38'),
(4222, '35.240.164.217', '2025-08-17', '2025-08-17 17:46:46', '2025-08-17 17:46:46'),
(4223, '185.191.171.11', '2025-08-17', '2025-08-17 17:47:57', '2025-08-17 17:47:57'),
(4224, '43.157.153.236', '2025-08-17', '2025-08-17 17:49:58', '2025-08-17 17:49:58'),
(4225, '34.57.96.86', '2025-08-17', '2025-08-17 17:53:43', '2025-08-17 17:53:43'),
(4226, '123.6.49.15', '2025-08-17', '2025-08-17 17:53:52', '2025-08-17 17:53:52'),
(4227, '123.6.49.18', '2025-08-17', '2025-08-17 17:53:52', '2025-08-17 17:53:52'),
(4228, '27.115.124.101', '2025-08-17', '2025-08-17 17:53:53', '2025-08-17 17:53:53'),
(4229, '43.157.170.13', '2025-08-17', '2025-08-17 17:54:58', '2025-08-17 17:54:58'),
(4230, '137.184.164.14', '2025-08-17', '2025-08-17 17:55:38', '2025-08-17 17:55:38'),
(4231, '65.108.64.152', '2025-08-18', '2025-08-17 18:00:07', '2025-08-17 18:00:07'),
(4232, '146.185.78.137', '2025-08-18', '2025-08-17 18:01:11', '2025-08-17 18:01:11'),
(4233, '103.87.250.233', '2025-08-18', '2025-08-17 18:01:13', '2025-08-17 18:01:13'),
(4234, '208.110.64.178', '2025-08-18', '2025-08-17 18:01:21', '2025-08-17 18:01:21'),
(4235, '157.55.39.9', '2025-08-18', '2025-08-17 18:02:47', '2025-08-17 18:02:47'),
(4236, '157.55.39.49', '2025-08-18', '2025-08-17 18:02:59', '2025-08-17 18:02:59'),
(4237, '43.166.136.202', '2025-08-18', '2025-08-17 18:05:19', '2025-08-17 18:05:19'),
(4238, '51.38.127.224', '2025-08-18', '2025-08-17 18:06:38', '2025-08-17 18:06:38'),
(4239, '103.203.178.19', '2025-08-18', '2025-08-17 18:07:04', '2025-08-17 18:07:04'),
(4240, '45.112.73.148', '2025-08-18', '2025-08-17 18:07:53', '2025-08-17 18:07:53'),
(4241, '207.46.13.141', '2025-08-18', '2025-08-17 18:08:47', '2025-08-17 18:08:47'),
(4242, '191.202.64.62', '2025-08-18', '2025-08-17 18:11:50', '2025-08-17 18:11:50'),
(4243, '107.130.219.56', '2025-08-18', '2025-08-17 18:12:14', '2025-08-17 18:12:14'),
(4244, '179.198.155.36', '2025-08-18', '2025-08-17 18:13:33', '2025-08-17 18:13:33'),
(4245, '131.153.143.50', '2025-08-18', '2025-08-17 18:14:01', '2025-08-17 18:14:01'),
(4246, '131.153.240.178', '2025-08-18', '2025-08-17 18:14:07', '2025-08-17 18:14:07'),
(4247, '43.135.138.128', '2025-08-18', '2025-08-17 18:15:23', '2025-08-17 18:15:23'),
(4248, '40.77.167.158', '2025-08-18', '2025-08-17 18:16:55', '2025-08-17 18:16:55'),
(4249, '196.251.72.125', '2025-08-18', '2025-08-17 18:17:30', '2025-08-17 18:17:30'),
(4250, '207.46.13.64', '2025-08-18', '2025-08-17 18:17:46', '2025-08-17 18:17:46'),
(4251, '154.26.128.67', '2025-08-18', '2025-08-17 18:18:57', '2025-08-17 18:18:57'),
(4252, '43.157.153.236', '2025-08-18', '2025-08-17 18:23:14', '2025-08-17 18:23:14'),
(4253, '94.247.172.129', '2025-08-18', '2025-08-17 18:28:24', '2025-08-17 18:28:24'),
(4254, '85.208.96.198', '2025-08-18', '2025-08-17 18:28:57', '2025-08-17 18:28:57'),
(4255, '204.12.252.98', '2025-08-18', '2025-08-17 18:29:29', '2025-08-17 18:29:29'),
(4256, '34.141.254.56', '2025-08-18', '2025-08-17 18:30:13', '2025-08-17 18:30:13'),
(4257, '162.62.213.165', '2025-08-18', '2025-08-17 18:32:42', '2025-08-17 18:32:42'),
(4258, '52.167.144.24', '2025-08-18', '2025-08-17 18:36:57', '2025-08-17 18:36:57'),
(4259, '66.249.73.198', '2025-08-18', '2025-08-17 18:38:12', '2025-08-17 18:38:12'),
(4260, '69.197.135.226', '2025-08-18', '2025-08-17 18:40:13', '2025-08-17 18:40:13'),
(4261, '113.191.209.251', '2025-08-18', '2025-08-17 18:41:20', '2025-08-17 18:41:20'),
(4262, '113.169.175.159', '2025-08-18', '2025-08-17 18:42:04', '2025-08-17 18:42:04'),
(4263, '43.154.250.181', '2025-08-18', '2025-08-17 18:46:54', '2025-08-17 18:46:54'),
(4264, '157.55.39.197', '2025-08-18', '2025-08-17 18:49:08', '2025-08-17 18:49:08'),
(4265, '185.191.171.9', '2025-08-18', '2025-08-17 18:53:38', '2025-08-17 18:53:38'),
(4266, '43.164.197.224', '2025-08-18', '2025-08-17 18:54:29', '2025-08-17 18:54:29'),
(4267, '104.232.194.211', '2025-08-18', '2025-08-17 18:57:23', '2025-08-17 18:57:23'),
(4268, '207.46.13.102', '2025-08-18', '2025-08-17 19:00:59', '2025-08-17 19:00:59'),
(4269, '52.167.144.192', '2025-08-18', '2025-08-17 19:01:20', '2025-08-17 19:01:20'),
(4270, '104.28.240.86', '2025-08-18', '2025-08-17 19:01:54', '2025-08-17 19:01:54'),
(4271, '104.232.195.75', '2025-08-18', '2025-08-17 19:03:56', '2025-08-17 19:03:56'),
(4272, '170.106.72.93', '2025-08-18', '2025-08-17 19:04:51', '2025-08-17 19:04:51'),
(4273, '104.232.194.65', '2025-08-18', '2025-08-17 19:08:04', '2025-08-17 19:08:04'),
(4274, '113.166.216.198', '2025-08-18', '2025-08-17 19:12:52', '2025-08-17 19:12:52'),
(4275, '49.51.72.236', '2025-08-18', '2025-08-17 19:13:38', '2025-08-17 19:13:38'),
(4276, '154.210.100.145', '2025-08-18', '2025-08-17 19:16:18', '2025-08-17 19:16:18'),
(4277, '154.210.100.72', '2025-08-18', '2025-08-17 19:18:08', '2025-08-17 19:18:08'),
(4278, '14.188.1.46', '2025-08-18', '2025-08-17 19:21:46', '2025-08-17 19:21:46'),
(4279, '201.81.2.124', '2025-08-18', '2025-08-17 19:21:59', '2025-08-17 19:21:59'),
(4280, '104.28.208.87', '2025-08-18', '2025-08-17 19:22:04', '2025-08-17 19:22:04'),
(4281, '104.28.164.57', '2025-08-18', '2025-08-17 19:22:07', '2025-08-17 19:22:07'),
(4282, '104.194.200.111', '2025-08-18', '2025-08-17 19:23:03', '2025-08-17 19:23:03'),
(4283, '157.55.39.195', '2025-08-18', '2025-08-17 19:27:45', '2025-08-17 19:27:45'),
(4284, '207.46.13.92', '2025-08-18', '2025-08-17 19:27:52', '2025-08-17 19:27:52'),
(4285, '34.55.28.147', '2025-08-18', '2025-08-17 19:27:59', '2025-08-17 19:27:59'),
(4286, '104.232.195.26', '2025-08-18', '2025-08-17 19:29:41', '2025-08-17 19:29:41'),
(4287, '40.77.167.241', '2025-08-18', '2025-08-17 19:29:43', '2025-08-17 19:29:43'),
(4288, '104.232.195.151', '2025-08-18', '2025-08-17 19:33:24', '2025-08-17 19:33:24'),
(4289, '66.249.73.200', '2025-08-18', '2025-08-17 19:34:44', '2025-08-17 19:34:44'),
(4290, '43.155.162.41', '2025-08-18', '2025-08-17 19:35:30', '2025-08-17 19:35:30'),
(4291, '154.210.100.85', '2025-08-18', '2025-08-17 19:38:36', '2025-08-17 19:38:36'),
(4292, '104.194.200.6', '2025-08-18', '2025-08-17 19:45:07', '2025-08-17 19:45:07'),
(4293, '154.210.110.185', '2025-08-18', '2025-08-17 19:45:11', '2025-08-17 19:45:11'),
(4294, '17.241.227.242', '2025-08-18', '2025-08-17 19:47:07', '2025-08-17 19:47:07'),
(4295, '49.51.195.195', '2025-08-18', '2025-08-17 19:47:50', '2025-08-17 19:47:50'),
(4296, '18.234.245.223', '2025-08-18', '2025-08-17 19:49:27', '2025-08-17 19:49:27'),
(4297, '17.22.237.162', '2025-08-18', '2025-08-17 19:49:54', '2025-08-17 19:49:54'),
(4298, '157.55.39.200', '2025-08-18', '2025-08-17 19:53:42', '2025-08-17 19:53:42'),
(4299, '157.55.39.53', '2025-08-18', '2025-08-17 19:56:33', '2025-08-17 19:56:33'),
(4300, '207.46.13.6', '2025-08-18', '2025-08-17 19:58:57', '2025-08-17 19:58:57'),
(4301, '43.157.147.3', '2025-08-18', '2025-08-17 19:59:59', '2025-08-17 19:59:59'),
(4302, '157.55.39.59', '2025-08-18', '2025-08-17 20:02:28', '2025-08-17 20:02:28'),
(4303, '62.210.105.214', '2025-08-18', '2025-08-17 20:07:01', '2025-08-17 20:07:01'),
(4304, '207.46.13.127', '2025-08-18', '2025-08-17 20:07:36', '2025-08-17 20:07:36'),
(4305, '43.155.188.157', '2025-08-18', '2025-08-17 20:12:13', '2025-08-17 20:12:13'),
(4306, '43.130.67.6', '2025-08-18', '2025-08-17 20:19:51', '2025-08-17 20:19:51'),
(4307, '43.135.139.165', '2025-08-18', '2025-08-17 20:28:34', '2025-08-17 20:28:34'),
(4308, '157.143.53.238', '2025-08-18', '2025-08-17 20:30:21', '2025-08-17 20:30:21'),
(4309, '40.77.167.19', '2025-08-18', '2025-08-17 20:34:07', '2025-08-17 20:34:07'),
(4310, '43.166.136.24', '2025-08-18', '2025-08-17 20:39:34', '2025-08-17 20:39:34'),
(4311, '87.236.176.99', '2025-08-18', '2025-08-17 20:44:08', '2025-08-17 20:44:08'),
(4312, '87.236.176.21', '2025-08-18', '2025-08-17 20:44:09', '2025-08-17 20:44:09'),
(4313, '64.227.109.89', '2025-08-18', '2025-08-17 20:44:11', '2025-08-17 20:44:11'),
(4314, '104.28.208.86', '2025-08-18', '2025-08-17 20:45:43', '2025-08-17 20:45:43'),
(4315, '157.55.39.10', '2025-08-18', '2025-08-17 20:50:40', '2025-08-17 20:50:40'),
(4316, '207.46.13.54', '2025-08-18', '2025-08-17 20:55:43', '2025-08-17 20:55:43'),
(4317, '158.140.182.77', '2025-08-18', '2025-08-17 20:57:08', '2025-08-17 20:57:08'),
(4318, '65.108.78.33', '2025-08-18', '2025-08-17 21:01:12', '2025-08-17 21:01:12'),
(4319, '103.118.78.131', '2025-08-18', '2025-08-17 21:01:24', '2025-08-17 21:01:24'),
(4320, '52.167.144.236', '2025-08-18', '2025-08-17 21:06:12', '2025-08-17 21:06:12'),
(4321, '66.249.73.199', '2025-08-18', '2025-08-17 21:08:05', '2025-08-17 21:08:05'),
(4322, '207.46.13.18', '2025-08-18', '2025-08-17 21:12:24', '2025-08-17 21:12:24'),
(4323, '107.22.154.107', '2025-08-18', '2025-08-17 21:16:18', '2025-08-17 21:16:18'),
(4324, '52.167.144.162', '2025-08-18', '2025-08-17 21:23:45', '2025-08-17 21:23:45'),
(4325, '3.126.248.32', '2025-08-18', '2025-08-17 21:37:46', '2025-08-17 21:37:46'),
(4326, '40.77.167.12', '2025-08-18', '2025-08-17 21:47:15', '2025-08-17 21:47:15'),
(4327, '207.46.13.17', '2025-08-18', '2025-08-17 21:50:29', '2025-08-17 21:50:29'),
(4328, '51.159.103.27', '2025-08-18', '2025-08-17 22:02:41', '2025-08-17 22:02:41'),
(4329, '207.46.13.36', '2025-08-18', '2025-08-17 22:18:11', '2025-08-17 22:18:11'),
(4330, '34.42.200.26', '2025-08-18', '2025-08-17 22:18:55', '2025-08-17 22:18:55'),
(4331, '40.77.167.0', '2025-08-18', '2025-08-17 22:21:19', '2025-08-17 22:21:19'),
(4332, '167.94.138.200', '2025-08-18', '2025-08-17 22:25:40', '2025-08-17 22:25:40'),
(4333, '37.27.51.146', '2025-08-18', '2025-08-17 22:28:04', '2025-08-17 22:28:04'),
(4334, '182.42.104.32', '2025-08-18', '2025-08-17 22:37:51', '2025-08-17 22:37:51'),
(4335, '37.187.89.104', '2025-08-18', '2025-08-17 22:43:43', '2025-08-17 22:43:43'),
(4336, '17.241.227.49', '2025-08-18', '2025-08-17 22:44:10', '2025-08-17 22:44:10'),
(4337, '157.55.39.56', '2025-08-18', '2025-08-17 22:52:44', '2025-08-17 22:52:44'),
(4338, '52.167.144.158', '2025-08-18', '2025-08-17 23:00:21', '2025-08-17 23:00:21'),
(4339, '85.208.96.193', '2025-08-18', '2025-08-17 23:00:26', '2025-08-17 23:00:26'),
(4340, '103.28.116.120', '2025-08-18', '2025-08-17 23:06:15', '2025-08-17 23:06:15'),
(4341, '207.46.13.86', '2025-08-18', '2025-08-17 23:15:37', '2025-08-17 23:15:37'),
(4342, '54.161.126.158', '2025-08-18', '2025-08-17 23:44:13', '2025-08-17 23:44:13'),
(4343, '91.134.91.17', '2025-08-18', '2025-08-17 23:47:48', '2025-08-17 23:47:48'),
(4344, '40.77.167.27', '2025-08-18', '2025-08-17 23:54:39', '2025-08-17 23:54:39'),
(4345, '66.249.90.166', '2025-08-18', '2025-08-17 23:58:11', '2025-08-17 23:58:11'),
(4346, '157.55.39.63', '2025-08-18', '2025-08-18 00:10:03', '2025-08-18 00:10:03'),
(4347, '40.77.167.143', '2025-08-18', '2025-08-18 00:18:40', '2025-08-18 00:18:40'),
(4348, '207.46.13.51', '2025-08-18', '2025-08-18 00:22:14', '2025-08-18 00:22:14'),
(4349, '159.203.56.28', '2025-08-18', '2025-08-18 00:32:41', '2025-08-18 00:32:41'),
(4350, '40.77.167.25', '2025-08-18', '2025-08-18 00:42:00', '2025-08-18 00:42:00'),
(4351, '85.208.96.211', '2025-08-18', '2025-08-18 00:44:38', '2025-08-18 00:44:38'),
(4352, '196.251.88.64', '2025-08-18', '2025-08-18 00:56:30', '2025-08-18 00:56:30'),
(4353, '183.197.174.71', '2025-08-18', '2025-08-18 01:00:17', '2025-08-18 01:00:17'),
(4354, '157.55.39.204', '2025-08-18', '2025-08-18 01:15:30', '2025-08-18 01:15:30'),
(4355, '52.167.144.145', '2025-08-18', '2025-08-18 01:15:36', '2025-08-18 01:15:36'),
(4356, '45.148.10.80', '2025-08-18', '2025-08-18 01:16:26', '2025-08-18 01:16:26'),
(4357, '59.14.17.48', '2025-08-18', '2025-08-18 01:20:52', '2025-08-18 01:20:52'),
(4358, '157.100.107.247', '2025-08-18', '2025-08-18 01:23:07', '2025-08-18 01:23:07'),
(4359, '133.218.144.6', '2025-08-18', '2025-08-18 01:25:00', '2025-08-18 01:25:00'),
(4360, '157.55.39.201', '2025-08-18', '2025-08-18 01:25:20', '2025-08-18 01:25:20'),
(4361, '157.55.39.52', '2025-08-18', '2025-08-18 01:33:31', '2025-08-18 01:33:31'),
(4362, '185.191.171.13', '2025-08-18', '2025-08-18 01:34:56', '2025-08-18 01:34:56'),
(4363, '118.89.233.234', '2025-08-18', '2025-08-18 01:35:50', '2025-08-18 01:35:50'),
(4364, '170.79.4.93', '2025-08-18', '2025-08-18 01:51:47', '2025-08-18 01:51:47'),
(4365, '43.156.204.134', '2025-08-18', '2025-08-18 01:52:39', '2025-08-18 01:52:39'),
(4366, '170.106.181.163', '2025-08-18', '2025-08-18 02:00:46', '2025-08-18 02:00:46'),
(4367, '52.167.144.176', '2025-08-18', '2025-08-18 02:01:09', '2025-08-18 02:01:09'),
(4368, '101.33.80.42', '2025-08-18', '2025-08-18 02:08:57', '2025-08-18 02:08:57'),
(4369, '40.77.167.28', '2025-08-18', '2025-08-18 02:12:11', '2025-08-18 02:12:11'),
(4370, '98.98.171.121', '2025-08-18', '2025-08-18 02:18:08', '2025-08-18 02:18:08'),
(4371, '20.171.207.235', '2025-08-18', '2025-08-18 02:29:08', '2025-08-18 02:29:08'),
(4372, '134.255.148.94', '2025-08-18', '2025-08-18 02:34:26', '2025-08-18 02:34:26'),
(4373, '5.160.146.1', '2025-08-18', '2025-08-18 02:43:57', '2025-08-18 02:43:57'),
(4374, '167.99.114.88', '2025-08-18', '2025-08-18 02:49:09', '2025-08-18 02:49:09'),
(4375, '20.229.51.198', '2025-08-18', '2025-08-18 02:56:34', '2025-08-18 02:56:34'),
(4376, '113.36.242.226', '2025-08-18', '2025-08-18 02:59:38', '2025-08-18 02:59:38'),
(4377, '155.4.47.54', '2025-08-18', '2025-08-18 03:04:59', '2025-08-18 03:04:59'),
(4378, '18.224.58.237', '2025-08-18', '2025-08-18 03:12:48', '2025-08-18 03:12:48'),
(4379, '40.77.167.14', '2025-08-18', '2025-08-18 03:18:16', '2025-08-18 03:18:16'),
(4380, '157.245.6.207', '2025-08-18', '2025-08-18 03:21:03', '2025-08-18 03:21:03'),
(4381, '44.196.119.63', '2025-08-18', '2025-08-18 03:26:26', '2025-08-18 03:26:26'),
(4382, '205.169.39.17', '2025-08-18', '2025-08-18 03:29:24', '2025-08-18 03:29:24'),
(4383, '205.169.39.135', '2025-08-18', '2025-08-18 03:30:09', '2025-08-18 03:30:09'),
(4384, '34.72.176.129', '2025-08-18', '2025-08-18 03:30:43', '2025-08-18 03:30:43'),
(4385, '91.211.87.110', '2025-08-18', '2025-08-18 03:31:49', '2025-08-18 03:31:49'),
(4386, '31.59.10.180', '2025-08-18', '2025-08-18 03:31:50', '2025-08-18 03:31:50'),
(4387, '34.116.148.88', '2025-08-18', '2025-08-18 03:32:05', '2025-08-18 03:32:05'),
(4388, '104.239.3.165', '2025-08-18', '2025-08-18 03:32:11', '2025-08-18 03:32:11'),
(4389, '23.27.91.249', '2025-08-18', '2025-08-18 03:32:14', '2025-08-18 03:32:14'),
(4390, '205.169.39.51', '2025-08-18', '2025-08-18 03:34:12', '2025-08-18 03:34:12'),
(4391, '52.57.143.52', '2025-08-18', '2025-08-18 03:37:10', '2025-08-18 03:37:10'),
(4392, '34.122.147.229', '2025-08-18', '2025-08-18 03:37:34', '2025-08-18 03:37:34'),
(4393, '104.197.69.115', '2025-08-18', '2025-08-18 03:38:05', '2025-08-18 03:38:05'),
(4394, '152.228.215.155', '2025-08-18', '2025-08-18 03:42:08', '2025-08-18 03:42:08'),
(4395, '167.71.166.141', '2025-08-18', '2025-08-18 03:42:27', '2025-08-18 03:42:27'),
(4396, '69.163.163.201', '2025-08-18', '2025-08-18 03:47:49', '2025-08-18 03:47:49'),
(4397, '54.92.221.4', '2025-08-18', '2025-08-18 03:48:48', '2025-08-18 03:48:48'),
(4398, '37.187.27.125', '2025-08-18', '2025-08-18 03:50:35', '2025-08-18 03:50:35'),
(4399, '116.203.211.224', '2025-08-18', '2025-08-18 03:52:19', '2025-08-18 03:52:19'),
(4400, '189.37.72.33', '2025-08-18', '2025-08-18 03:52:22', '2025-08-18 03:52:22'),
(4401, '185.197.195.89', '2025-08-18', '2025-08-18 03:53:10', '2025-08-18 03:53:10'),
(4402, '65.0.3.244', '2025-08-18', '2025-08-18 03:58:33', '2025-08-18 03:58:33'),
(4403, '94.191.24.214', '2025-08-18', '2025-08-18 04:04:03', '2025-08-18 04:04:03'),
(4404, '103.172.41.201', '2025-08-18', '2025-08-18 04:12:05', '2025-08-18 04:12:05'),
(4405, '146.70.185.32', '2025-08-18', '2025-08-18 04:14:22', '2025-08-18 04:14:22'),
(4406, '50.6.4.158', '2025-08-18', '2025-08-18 04:20:07', '2025-08-18 04:20:07'),
(4407, '216.131.114.26', '2025-08-18', '2025-08-18 04:22:07', '2025-08-18 04:22:07'),
(4408, '82.223.70.74', '2025-08-18', '2025-08-18 04:25:32', '2025-08-18 04:25:32'),
(4409, '52.167.144.231', '2025-08-18', '2025-08-18 04:26:22', '2025-08-18 04:26:22'),
(4410, '213.136.93.169', '2025-08-18', '2025-08-18 04:30:58', '2025-08-18 04:30:58'),
(4411, '3.109.103.5', '2025-08-18', '2025-08-18 04:36:22', '2025-08-18 04:36:22'),
(4412, '42.0.7.229', '2025-08-18', '2025-08-18 04:37:23', '2025-08-18 04:37:23'),
(4413, '66.249.73.196', '2025-08-18', '2025-08-18 04:39:33', '2025-08-18 04:39:33'),
(4414, '52.167.144.211', '2025-08-18', '2025-08-18 04:41:45', '2025-08-18 04:41:45'),
(4415, '185.150.190.222', '2025-08-18', '2025-08-18 04:41:46', '2025-08-18 04:41:46'),
(4416, '103.126.22.5', '2025-08-18', '2025-08-18 04:47:31', '2025-08-18 04:47:31'),
(4417, '104.156.244.244', '2025-08-18', '2025-08-18 04:57:55', '2025-08-18 04:57:55'),
(4418, '51.75.128.94', '2025-08-18', '2025-08-18 04:59:37', '2025-08-18 04:59:37'),
(4419, '13.125.4.74', '2025-08-18', '2025-08-18 05:03:23', '2025-08-18 05:03:23'),
(4420, '57.128.47.115', '2025-08-18', '2025-08-18 05:08:46', '2025-08-18 05:08:46'),
(4421, '40.77.167.71', '2025-08-18', '2025-08-18 05:13:05', '2025-08-18 05:13:05'),
(4422, '142.171.182.233', '2025-08-18', '2025-08-18 05:14:08', '2025-08-18 05:14:08'),
(4423, '54.167.171.208', '2025-08-18', '2025-08-18 05:16:16', '2025-08-18 05:16:16'),
(4424, '34.239.226.236', '2025-08-18', '2025-08-18 05:16:55', '2025-08-18 05:16:55'),
(4425, '192.227.184.130', '2025-08-18', '2025-08-18 05:19:39', '2025-08-18 05:19:39'),
(4426, '179.48.100.77', '2025-08-18', '2025-08-18 05:21:54', '2025-08-18 05:21:54'),
(4427, '45.171.165.178', '2025-08-18', '2025-08-18 05:23:45', '2025-08-18 05:23:45'),
(4428, '52.167.144.174', '2025-08-18', '2025-08-18 05:24:59', '2025-08-18 05:24:59'),
(4429, '5.255.112.147', '2025-08-18', '2025-08-18 05:25:07', '2025-08-18 05:25:07'),
(4430, '78.192.104.125', '2025-08-18', '2025-08-18 05:36:05', '2025-08-18 05:36:05'),
(4431, '103.74.121.5', '2025-08-18', '2025-08-18 05:41:39', '2025-08-18 05:41:39'),
(4432, '91.213.188.12', '2025-08-18', '2025-08-18 05:47:14', '2025-08-18 05:47:14'),
(4433, '157.55.39.193', '2025-08-18', '2025-08-18 05:49:06', '2025-08-18 05:49:06'),
(4434, '167.172.113.201', '2025-08-18', '2025-08-18 05:52:47', '2025-08-18 05:52:47'),
(4435, '61.221.51.11', '2025-08-18', '2025-08-18 05:59:15', '2025-08-18 05:59:15'),
(4436, '35.198.195.184', '2025-08-18', '2025-08-18 06:01:34', '2025-08-18 06:01:34'),
(4437, '185.146.3.15', '2025-08-18', '2025-08-18 06:09:25', '2025-08-18 06:09:25'),
(4438, '52.167.144.215', '2025-08-18', '2025-08-18 06:15:36', '2025-08-18 06:15:36'),
(4439, '43.199.66.183', '2025-08-18', '2025-08-18 06:18:52', '2025-08-18 06:18:52'),
(4440, '20.11.41.35', '2025-08-18', '2025-08-18 06:20:35', '2025-08-18 06:20:35'),
(4441, '207.46.13.128', '2025-08-18', '2025-08-18 06:21:57', '2025-08-18 06:21:57'),
(4442, '51.38.119.44', '2025-08-18', '2025-08-18 06:26:10', '2025-08-18 06:26:10'),
(4443, '159.89.17.163', '2025-08-18', '2025-08-18 06:26:41', '2025-08-18 06:26:41'),
(4444, '93.158.91.33', '2025-08-18', '2025-08-18 06:28:11', '2025-08-18 06:28:11'),
(4445, '135.125.240.194', '2025-08-18', '2025-08-18 06:31:50', '2025-08-18 06:31:50'),
(4446, '152.53.90.232', '2025-08-18', '2025-08-18 06:43:06', '2025-08-18 06:43:06'),
(4447, '135.220.169.33', '2025-08-18', '2025-08-18 06:52:46', '2025-08-18 06:52:46'),
(4448, '207.46.13.87', '2025-08-18', '2025-08-18 06:59:44', '2025-08-18 06:59:44'),
(4449, '149.154.161.216', '2025-08-18', '2025-08-18 07:00:10', '2025-08-18 07:00:10'),
(4450, '35.225.183.27', '2025-08-18', '2025-08-18 07:00:13', '2025-08-18 07:00:13'),
(4451, '43.153.23.245', '2025-08-18', '2025-08-18 07:00:23', '2025-08-18 07:00:23'),
(4452, '103.87.251.120', '2025-08-18', '2025-08-18 07:00:54', '2025-08-18 07:00:54'),
(4453, '202.173.120.132', '2025-08-18', '2025-08-18 07:01:05', '2025-08-18 07:01:05'),
(4454, '103.163.214.6', '2025-08-18', '2025-08-18 07:05:58', '2025-08-18 07:05:58'),
(4455, '217.76.154.93', '2025-08-18', '2025-08-18 07:17:33', '2025-08-18 07:17:33'),
(4456, '103.234.167.5', '2025-08-18', '2025-08-18 07:19:24', '2025-08-18 07:19:24'),
(4457, '167.94.138.33', '2025-08-18', '2025-08-18 07:22:51', '2025-08-18 07:22:51'),
(4458, '40.77.167.132', '2025-08-18', '2025-08-18 07:27:20', '2025-08-18 07:27:20'),
(4459, '52.167.144.136', '2025-08-18', '2025-08-18 07:29:00', '2025-08-18 07:29:00'),
(4460, '190.8.18.119', '2025-08-18', '2025-08-18 07:32:11', '2025-08-18 07:32:11'),
(4461, '45.170.80.136', '2025-08-18', '2025-08-18 07:32:29', '2025-08-18 07:32:29'),
(4462, '45.118.245.68', '2025-08-18', '2025-08-18 07:51:01', '2025-08-18 07:51:01'),
(4463, '103.126.22.7', '2025-08-18', '2025-08-18 07:51:06', '2025-08-18 07:51:06'),
(4464, '154.30.17.15', '2025-08-18', '2025-08-18 07:56:10', '2025-08-18 07:56:10'),
(4465, '103.87.250.147', '2025-08-18', '2025-08-18 08:13:55', '2025-08-18 08:13:55'),
(4466, '170.106.167.214', '2025-08-18', '2025-08-18 08:18:02', '2025-08-18 08:18:02'),
(4467, '34.56.9.83', '2025-08-18', '2025-08-18 08:20:57', '2025-08-18 08:20:57'),
(4468, '103.138.173.13', '2025-08-18', '2025-08-18 08:23:39', '2025-08-18 08:23:39'),
(4469, '34.71.190.63', '2025-08-18', '2025-08-18 08:26:41', '2025-08-18 08:26:41'),
(4470, '172.233.62.72', '2025-08-18', '2025-08-18 08:38:04', '2025-08-18 08:38:04'),
(4471, '103.234.167.4', '2025-08-18', '2025-08-18 08:50:37', '2025-08-18 08:50:37'),
(4472, '116.203.34.44', '2025-08-18', '2025-08-18 08:54:17', '2025-08-18 08:54:17'),
(4473, '103.196.232.132', '2025-08-18', '2025-08-18 08:54:28', '2025-08-18 08:54:28'),
(4474, '103.196.232.133', '2025-08-18', '2025-08-18 08:54:34', '2025-08-18 08:54:34'),
(4475, '202.173.122.68', '2025-08-18', '2025-08-18 08:54:39', '2025-08-18 08:54:39');

-- --------------------------------------------------------

--
-- Table structure for table `vouchers`
--

CREATE TABLE `vouchers` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `variation_id` bigint(20) UNSIGNED NOT NULL,
  `order_id` bigint(20) UNSIGNED DEFAULT NULL,
  `code` varchar(255) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `transaction_id` varchar(55) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auto_vouchers`
--
ALTER TABLE `auto_vouchers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `auto_vouchers_variation_id_foreign` (`variation_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deposits`
--
ALTER TABLE `deposits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `deposits_user_id_foreign` (`user_id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `media`
--
ALTER TABLE `media`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `media_uuid_unique` (`uuid`),
  ADD KEY `media_model_type_model_id_index` (`model_type`,`model_id`),
  ADD KEY `media_order_column_index` (`order_column`);

--
-- Indexes for table `menus`
--
ALTER TABLE `menus`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_user_id_foreign` (`user_id`);

--
-- Indexes for table `pages`
--
ALTER TABLE `pages`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pages_slug_unique` (`slug`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `personal_access_tokens_token_unique` (`token`),
  ADD KEY `personal_access_tokens_tokenable_type_tokenable_id_index` (`tokenable_type`,`tokenable_id`);

--
-- Indexes for table `popups`
--
ALTER TABLE `popups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `products_slug_unique` (`slug`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `settings_group_name_unique` (`group`,`name`);

--
-- Indexes for table `sliders`
--
ALTER TABLE `sliders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `transactions_transaction_id_unique` (`transaction_id`),
  ADD KEY `transactions_user_id_foreign` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- Indexes for table `variations`
--
ALTER TABLE `variations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `variations_product_id_foreign` (`product_id`);

--
-- Indexes for table `visitors`
--
ALTER TABLE `visitors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `vouchers`
--
ALTER TABLE `vouchers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vouchers_variation_id_foreign` (`variation_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auto_vouchers`
--
ALTER TABLE `auto_vouchers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `deposits`
--
ALTER TABLE `deposits`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6773;

--
-- AUTO_INCREMENT for table `media`
--
ALTER TABLE `media`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=162;

--
-- AUTO_INCREMENT for table `menus`
--
ALTER TABLE `menus`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=159;

--
-- AUTO_INCREMENT for table `pages`
--
ALTER TABLE `pages`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `personal_access_tokens`
--
ALTER TABLE `personal_access_tokens`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `popups`
--
ALTER TABLE `popups`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10360;

--
-- AUTO_INCREMENT for table `sliders`
--
ALTER TABLE `sliders`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3981;

--
-- AUTO_INCREMENT for table `variations`
--
ALTER TABLE `variations`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=255;

--
-- AUTO_INCREMENT for table `visitors`
--
ALTER TABLE `visitors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4476;

--
-- AUTO_INCREMENT for table `vouchers`
--
ALTER TABLE `vouchers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=143;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auto_vouchers`
--
ALTER TABLE `auto_vouchers`
  ADD CONSTRAINT `auto_vouchers_variation_id_foreign` FOREIGN KEY (`variation_id`) REFERENCES `variations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `deposits`
--
ALTER TABLE `deposits`
  ADD CONSTRAINT `deposits_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `variations`
--
ALTER TABLE `variations`
  ADD CONSTRAINT `variations_product_id_foreign` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `vouchers`
--
ALTER TABLE `vouchers`
  ADD CONSTRAINT `vouchers_variation_id_foreign` FOREIGN KEY (`variation_id`) REFERENCES `variations` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
