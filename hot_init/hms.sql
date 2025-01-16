-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : lun. 13 jan. 2025 à 05:49
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `hms`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add client', 7, 'add_client'),
(26, 'Can change client', 7, 'change_client'),
(27, 'Can delete client', 7, 'delete_client'),
(28, 'Can view client', 7, 'view_client'),
(29, 'Can add type historique', 8, 'add_typehistorique'),
(30, 'Can change type historique', 8, 'change_typehistorique'),
(31, 'Can delete type historique', 8, 'delete_typehistorique'),
(32, 'Can view type historique', 8, 'view_typehistorique'),
(33, 'Can add historique', 9, 'add_historique'),
(34, 'Can change historique', 9, 'change_historique'),
(35, 'Can delete historique', 9, 'delete_historique'),
(36, 'Can view historique', 9, 'view_historique'),
(37, 'Can add history room', 10, 'add_historyroom'),
(38, 'Can change history room', 10, 'change_historyroom'),
(39, 'Can delete history room', 10, 'delete_historyroom'),
(40, 'Can view history room', 10, 'view_historyroom'),
(41, 'Can add hotel info', 11, 'add_hotelinfo'),
(42, 'Can change hotel info', 11, 'change_hotelinfo'),
(43, 'Can delete hotel info', 11, 'delete_hotelinfo'),
(44, 'Can view hotel info', 11, 'view_hotelinfo'),
(45, 'Can add room', 12, 'add_room'),
(46, 'Can change room', 12, 'change_room'),
(47, 'Can delete room', 12, 'delete_room'),
(48, 'Can view room', 12, 'view_room'),
(49, 'Can add commande room', 13, 'add_commanderoom'),
(50, 'Can change commande room', 13, 'change_commanderoom'),
(51, 'Can delete commande room', 13, 'delete_commanderoom'),
(52, 'Can view commande room', 13, 'view_commanderoom'),
(53, 'Can add room image', 14, 'add_roomimage'),
(54, 'Can change room image', 14, 'change_roomimage'),
(55, 'Can delete room image', 14, 'delete_roomimage'),
(56, 'Can view room image', 14, 'view_roomimage'),
(57, 'Can add service', 15, 'add_service'),
(58, 'Can change service', 15, 'change_service'),
(59, 'Can delete service', 15, 'delete_service'),
(60, 'Can view service', 15, 'view_service'),
(61, 'Can add status', 16, 'add_status'),
(62, 'Can change status', 16, 'change_status'),
(63, 'Can delete status', 16, 'delete_status'),
(64, 'Can view status', 16, 'view_status'),
(65, 'Can add service item', 17, 'add_serviceitem'),
(66, 'Can change service item', 17, 'change_serviceitem'),
(67, 'Can delete service item', 17, 'delete_serviceitem'),
(68, 'Can view service item', 17, 'view_serviceitem'),
(69, 'Can add commande service', 18, 'add_commandeservice'),
(70, 'Can change commande service', 18, 'change_commandeservice'),
(71, 'Can delete commande service', 18, 'delete_commandeservice'),
(72, 'Can view commande service', 18, 'view_commandeservice'),
(73, 'Can add item image', 19, 'add_itemimage'),
(74, 'Can change item image', 19, 'change_itemimage'),
(75, 'Can delete item image', 19, 'delete_itemimage'),
(76, 'Can view item image', 19, 'view_itemimage'),
(77, 'Can add role', 20, 'add_role'),
(78, 'Can change role', 20, 'change_role'),
(79, 'Can delete role', 20, 'delete_role'),
(80, 'Can view role', 20, 'view_role'),
(81, 'Can add user', 21, 'add_user'),
(82, 'Can change user', 21, 'change_user'),
(83, 'Can delete user', 21, 'delete_user'),
(84, 'Can view user', 21, 'view_user'),
(85, 'Can add user preference', 22, 'add_userpreference'),
(86, 'Can change user preference', 22, 'change_userpreference'),
(87, 'Can delete user preference', 22, 'delete_userpreference'),
(88, 'Can view user preference', 22, 'view_userpreference');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'hot_clients', 'client'),
(9, 'hot_history', 'historique'),
(10, 'hot_history', 'historyroom'),
(8, 'hot_history', 'typehistorique'),
(11, 'hot_hotel', 'hotelinfo'),
(13, 'hot_rooms', 'commanderoom'),
(12, 'hot_rooms', 'room'),
(14, 'hot_rooms', 'roomimage'),
(18, 'hot_services', 'commandeservice'),
(19, 'hot_services', 'itemimage'),
(15, 'hot_services', 'service'),
(17, 'hot_services', 'serviceitem'),
(16, 'hot_services', 'status'),
(20, 'hot_users', 'role'),
(21, 'hot_users', 'user'),
(22, 'hot_users', 'userpreference'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-01-13 04:27:21.353157'),
(2, 'auth', '0001_initial', '2025-01-13 04:27:27.824385'),
(3, 'admin', '0001_initial', '2025-01-13 04:27:31.384589'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-01-13 04:27:31.859687'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-01-13 04:27:32.306254'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-01-13 04:27:34.259478'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-01-13 04:27:34.854118'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-01-13 04:27:35.315480'),
(9, 'auth', '0004_alter_user_username_opts', '2025-01-13 04:27:35.795966'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-01-13 04:27:37.351569'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-01-13 04:27:37.360352'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-01-13 04:27:37.381705'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-01-13 04:27:39.000783'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-01-13 04:27:41.026052'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-01-13 04:27:42.105844'),
(16, 'auth', '0011_update_proxy_permissions', '2025-01-13 04:27:42.726318'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-01-13 04:27:42.915714'),
(18, 'hot_clients', '0001_initial', '2025-01-13 04:27:42.984722'),
(19, 'hot_clients', '0002_alter_client_cin_alter_client_email', '2025-01-13 04:27:46.129032'),
(20, 'hot_clients', '0003_alter_client_idclient', '2025-01-13 04:27:46.136057'),
(21, 'hot_users', '0001_initial', '2025-01-13 04:27:46.590523'),
(22, 'hot_users', '0002_user_passwordversion', '2025-01-13 04:27:46.705132'),
(23, 'hot_users', '0003_user_image', '2025-01-13 04:27:46.803271'),
(24, 'hot_services', '0001_initial', '2025-01-13 04:27:47.993225'),
(25, 'hot_rooms', '0001_initial', '2025-01-13 04:27:48.913196'),
(26, 'hot_rooms', '0002_alter_room_price_roomimage', '2025-01-13 04:27:49.110054'),
(27, 'hot_rooms', '0003_commanderoom_price_commanderoom_total', '2025-01-13 04:27:49.332293'),
(28, 'hot_history', '0001_initial', '2025-01-13 04:27:50.252133'),
(29, 'hot_history', '0002_rename_iduser_historique_idadmin_and_more', '2025-01-13 04:27:50.814675'),
(30, 'hot_history', '0003_historyroom', '2025-01-13 04:27:51.150815'),
(31, 'hot_hotel', '0001_initial', '2025-01-13 04:27:51.220048'),
(32, 'hot_services', '0002_serviceitem_iduser', '2025-01-13 04:27:51.401357'),
(33, 'hot_services', '0003_commandeservice_total', '2025-01-13 04:27:51.531828'),
(34, 'hot_services', '0004_itemimage', '2025-01-13 04:27:51.733776'),
(35, 'hot_rooms', '0004_alter_commanderoom_idclient_and_more', '2025-01-13 04:27:53.213844'),
(36, 'hot_rooms', '0005_commanderoom_payed', '2025-01-13 04:27:53.321444'),
(37, 'hot_rooms', '0006_alter_commanderoom_datestart_alter_room_idroom_and_more', '2025-01-13 04:27:53.571170'),
(38, 'hot_services', '0005_alter_service_idservice', '2025-01-13 04:27:53.590688'),
(39, 'hot_users', '0004_alter_role_idrole_alter_role_poste_alter_user_iduser', '2025-01-13 04:27:53.688271'),
(40, 'sessions', '0001_initial', '2025-01-13 04:27:53.783328');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_clients_client`
--

DROP TABLE IF EXISTS `hot_clients_client`;
CREATE TABLE IF NOT EXISTS `hot_clients_client` (
  `idClient` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `firstName` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `genre` varchar(10) DEFAULT NULL,
  `adress` longtext,
  `cin` varchar(50) DEFAULT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`idClient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_history_historique`
--

DROP TABLE IF EXISTS `hot_history_historique`;
CREATE TABLE IF NOT EXISTS `hot_history_historique` (
  `idHistorique` int NOT NULL AUTO_INCREMENT,
  `description` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idCommandeRoom_id` int DEFAULT NULL,
  `idCommandeService_id` int DEFAULT NULL,
  `idType_id` int NOT NULL,
  `idAdmin_id` int NOT NULL,
  PRIMARY KEY (`idHistorique`),
  KEY `hot_history_historiq_idCommandeService_id_bc038ce7_fk_hot_servi` (`idCommandeService_id`),
  KEY `hot_history_historiq_idType_id_45b9b1bb_fk_hot_histo` (`idType_id`),
  KEY `hot_history_historiq_idAdmin_id_6e1fdc2d_fk_hot_users` (`idAdmin_id`),
  KEY `hot_history_historiq_idCommandeRoom_id_70052aa3_fk_hot_rooms` (`idCommandeRoom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_history_historyroom`
--

DROP TABLE IF EXISTS `hot_history_historyroom`;
CREATE TABLE IF NOT EXISTS `hot_history_historyroom` (
  `idHistory` int NOT NULL AUTO_INCREMENT,
  `description` longtext,
  `createdAt` datetime(6) NOT NULL,
  `idAdmin_id` int NOT NULL,
  `idRoom_id` int NOT NULL,
  PRIMARY KEY (`idHistory`),
  KEY `hot_history_historyr_idAdmin_id_0c65c871_fk_hot_users` (`idAdmin_id`),
  KEY `hot_history_historyr_idRoom_id_70a327d0_fk_hot_rooms` (`idRoom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_history_typehistorique`
--

DROP TABLE IF EXISTS `hot_history_typehistorique`;
CREATE TABLE IF NOT EXISTS `hot_history_typehistorique` (
  `idType` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`idType`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `hot_history_typehistorique`
--

INSERT INTO `hot_history_typehistorique` (`idType`, `name`) VALUES
(1, 'Commande Room'),
(2, 'Commande Service');

-- --------------------------------------------------------

--
-- Structure de la table `hot_hotel_hotelinfo`
--

DROP TABLE IF EXISTS `hot_hotel_hotelinfo`;
CREATE TABLE IF NOT EXISTS `hot_hotel_hotelinfo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `color` varchar(50) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `adress` longtext,
  `homeImage` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_rooms_commanderoom`
--

DROP TABLE IF EXISTS `hot_rooms_commanderoom`;
CREATE TABLE IF NOT EXISTS `hot_rooms_commanderoom` (
  `idCommande` int NOT NULL AUTO_INCREMENT,
  `DateStart` datetime(6) NOT NULL,
  `DateEnd` datetime(6) NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idAdmin_id` int DEFAULT NULL,
  `idClient_id` int DEFAULT NULL,
  `idRoom_id` int DEFAULT NULL,
  `idStatus_id` int DEFAULT NULL,
  `price` int NOT NULL,
  `total` int NOT NULL,
  `payed` int DEFAULT NULL,
  PRIMARY KEY (`idCommande`),
  KEY `hot_rooms_commandero_idAdmin_id_5d348ef4_fk_hot_users` (`idAdmin_id`),
  KEY `hot_rooms_commandero_idClient_id_cad0ff1d_fk_hot_clien` (`idClient_id`),
  KEY `hot_rooms_commandero_idRoom_id_19edb1ba_fk_hot_rooms` (`idRoom_id`),
  KEY `hot_rooms_commandero_idStatus_id_e18248fe_fk_hot_servi` (`idStatus_id`),
  KEY `hot_rooms_commanderoom_DateStart_c24d31f1` (`DateStart`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_rooms_room`
--

DROP TABLE IF EXISTS `hot_rooms_room`;
CREATE TABLE IF NOT EXISTS `hot_rooms_room` (
  `idRoom` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `subTitle` varchar(255) DEFAULT NULL,
  `description` longtext,
  `price` int NOT NULL,
  `available` tinyint(1) NOT NULL,
  `dateAvailable` datetime(6) DEFAULT NULL,
  `info` json DEFAULT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idAdmin_id` int NOT NULL,
  PRIMARY KEY (`idRoom`),
  KEY `hot_rooms_room_idAdmin_id_faa838ee_fk_hot_users_user_idUser` (`idAdmin_id`),
  KEY `hot_rooms_room_subTitle_58b0717d` (`subTitle`),
  KEY `hot_rooms_room_title_4f20f6cd` (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_rooms_roomimage`
--

DROP TABLE IF EXISTS `hot_rooms_roomimage`;
CREATE TABLE IF NOT EXISTS `hot_rooms_roomimage` (
  `idImage` int NOT NULL AUTO_INCREMENT,
  `image` varchar(200) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `idRoom_id` int NOT NULL,
  PRIMARY KEY (`idImage`),
  KEY `hot_rooms_roomimage_idRoom_id_3b02ce0b_fk_hot_rooms_room_idRoom` (`idRoom_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_services_commandeservice`
--

DROP TABLE IF EXISTS `hot_services_commandeservice`;
CREATE TABLE IF NOT EXISTS `hot_services_commandeservice` (
  `idCommande` int NOT NULL AUTO_INCREMENT,
  `number` int NOT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idAdmin_id` int DEFAULT NULL,
  `idClient_id` int NOT NULL,
  `idItem_id` int NOT NULL,
  `idStatus_id` int NOT NULL,
  `total` int NOT NULL,
  PRIMARY KEY (`idCommande`),
  KEY `hot_services_command_idAdmin_id_a8c7dc48_fk_hot_users` (`idAdmin_id`),
  KEY `hot_services_command_idClient_id_477351c7_fk_hot_clien` (`idClient_id`),
  KEY `hot_services_command_idItem_id_0c23a7bd_fk_hot_servi` (`idItem_id`),
  KEY `hot_services_command_idStatus_id_27eeaabf_fk_hot_servi` (`idStatus_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_services_itemimage`
--

DROP TABLE IF EXISTS `hot_services_itemimage`;
CREATE TABLE IF NOT EXISTS `hot_services_itemimage` (
  `idImage` int NOT NULL AUTO_INCREMENT,
  `image` varchar(200) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `idItem_id` int NOT NULL,
  PRIMARY KEY (`idImage`),
  KEY `hot_services_itemima_idItem_id_d3185906_fk_hot_servi` (`idItem_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_services_service`
--

DROP TABLE IF EXISTS `hot_services_service`;
CREATE TABLE IF NOT EXISTS `hot_services_service` (
  `idService` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idUser_id` int NOT NULL,
  PRIMARY KEY (`idService`),
  KEY `hot_services_service_idUser_id_432c7993_fk_hot_users_user_idUser` (`idUser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_services_serviceitem`
--

DROP TABLE IF EXISTS `hot_services_serviceitem`;
CREATE TABLE IF NOT EXISTS `hot_services_serviceitem` (
  `idItem` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `subTitle` varchar(255) DEFAULT NULL,
  `description` longtext,
  `price` int NOT NULL,
  `unity` varchar(50) DEFAULT NULL,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idService_id` int NOT NULL,
  `idUser_id` int DEFAULT NULL,
  PRIMARY KEY (`idItem`),
  KEY `hot_services_service_idService_id_48b3f652_fk_hot_servi` (`idService_id`),
  KEY `hot_services_service_idUser_id_2aa863fb_fk_hot_users` (`idUser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `hot_services_status`
--

DROP TABLE IF EXISTS `hot_services_status`;
CREATE TABLE IF NOT EXISTS `hot_services_status` (
  `idStatus` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`idStatus`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `hot_services_status`
--

INSERT INTO `hot_services_status` (`idStatus`, `name`) VALUES
(2, 'Canceled'),
(3, 'Confirmed'),
(4, 'Pending'),
(1, 'Reserved');

-- --------------------------------------------------------

--
-- Structure de la table `hot_users_role`
--

DROP TABLE IF EXISTS `hot_users_role`;
CREATE TABLE IF NOT EXISTS `hot_users_role` (
  `idRole` int NOT NULL AUTO_INCREMENT,
  `poste` varchar(255) NOT NULL,
  PRIMARY KEY (`idRole`),
  KEY `hot_users_role_poste_700625c9` (`poste`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `hot_users_role`
--

INSERT INTO `hot_users_role` (`idRole`, `poste`) VALUES
(1, 'Administrator');

-- --------------------------------------------------------

--
-- Structure de la table `hot_users_user`
--

DROP TABLE IF EXISTS `hot_users_user`;
CREATE TABLE IF NOT EXISTS `hot_users_user` (
  `idUser` int NOT NULL AUTO_INCREMENT,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `genre` varchar(10) DEFAULT NULL,
  `adress` longtext,
  `createdAt` datetime(6) NOT NULL,
  `updatedAt` datetime(6) NOT NULL,
  `deletedAt` datetime(6) DEFAULT NULL,
  `idRole_id` int NOT NULL,
  `passwordVersion` int NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idUser`),
  UNIQUE KEY `login` (`login`),
  UNIQUE KEY `email` (`email`),
  KEY `hot_users_user_idRole_id_437d67f2_fk_hot_users_role_idRole` (`idRole_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `hot_users_user`
--

INSERT INTO `hot_users_user` (`idUser`, `login`, `password`, `name`, `firstname`, `phone`, `email`, `genre`, `adress`, `createdAt`, `updatedAt`, `deletedAt`, `idRole_id`, `passwordVersion`, `image`) VALUES
(1, 'admin', 'pbkdf2_sha256$870000$GaUhbLQeNir6GRdv5W6ys4$AZ8eBmMcecBfTjLNYHJZVhYpDW8KPs/ZMfCd9i0YEp8=', 'Admin', 'HSM', '0202020020', 'nomail@gmail.com', 'HOMME', 'Tananarive Madagascar', '2025-01-13 05:41:53.410672', '2025-01-13 05:41:53.410672', NULL, 1, 1, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `hot_users_userpreference`
--

DROP TABLE IF EXISTS `hot_users_userpreference`;
CREATE TABLE IF NOT EXISTS `hot_users_userpreference` (
  `idPreference` int NOT NULL AUTO_INCREMENT,
  `theme` varchar(50) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `idUser_id` int NOT NULL,
  PRIMARY KEY (`idPreference`),
  KEY `hot_users_userprefer_idUser_id_c99e734a_fk_hot_users` (`idUser_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `hot_history_historique`
--
ALTER TABLE `hot_history_historique`
  ADD CONSTRAINT `hot_history_historiq_idAdmin_id_6e1fdc2d_fk_hot_users` FOREIGN KEY (`idAdmin_id`) REFERENCES `hot_users_user` (`idUser`),
  ADD CONSTRAINT `hot_history_historiq_idCommandeRoom_id_70052aa3_fk_hot_rooms` FOREIGN KEY (`idCommandeRoom_id`) REFERENCES `hot_rooms_commanderoom` (`idCommande`),
  ADD CONSTRAINT `hot_history_historiq_idCommandeService_id_bc038ce7_fk_hot_servi` FOREIGN KEY (`idCommandeService_id`) REFERENCES `hot_services_commandeservice` (`idCommande`),
  ADD CONSTRAINT `hot_history_historiq_idType_id_45b9b1bb_fk_hot_histo` FOREIGN KEY (`idType_id`) REFERENCES `hot_history_typehistorique` (`idType`);

--
-- Contraintes pour la table `hot_history_historyroom`
--
ALTER TABLE `hot_history_historyroom`
  ADD CONSTRAINT `hot_history_historyr_idAdmin_id_0c65c871_fk_hot_users` FOREIGN KEY (`idAdmin_id`) REFERENCES `hot_users_user` (`idUser`),
  ADD CONSTRAINT `hot_history_historyr_idRoom_id_70a327d0_fk_hot_rooms` FOREIGN KEY (`idRoom_id`) REFERENCES `hot_rooms_room` (`idRoom`);

--
-- Contraintes pour la table `hot_rooms_commanderoom`
--
ALTER TABLE `hot_rooms_commanderoom`
  ADD CONSTRAINT `hot_rooms_commandero_idAdmin_id_5d348ef4_fk_hot_users` FOREIGN KEY (`idAdmin_id`) REFERENCES `hot_users_user` (`idUser`),
  ADD CONSTRAINT `hot_rooms_commandero_idClient_id_cad0ff1d_fk_hot_clien` FOREIGN KEY (`idClient_id`) REFERENCES `hot_clients_client` (`idClient`),
  ADD CONSTRAINT `hot_rooms_commandero_idRoom_id_19edb1ba_fk_hot_rooms` FOREIGN KEY (`idRoom_id`) REFERENCES `hot_rooms_room` (`idRoom`),
  ADD CONSTRAINT `hot_rooms_commandero_idStatus_id_e18248fe_fk_hot_servi` FOREIGN KEY (`idStatus_id`) REFERENCES `hot_services_status` (`idStatus`);

--
-- Contraintes pour la table `hot_rooms_room`
--
ALTER TABLE `hot_rooms_room`
  ADD CONSTRAINT `hot_rooms_room_idAdmin_id_faa838ee_fk_hot_users_user_idUser` FOREIGN KEY (`idAdmin_id`) REFERENCES `hot_users_user` (`idUser`);

--
-- Contraintes pour la table `hot_rooms_roomimage`
--
ALTER TABLE `hot_rooms_roomimage`
  ADD CONSTRAINT `hot_rooms_roomimage_idRoom_id_3b02ce0b_fk_hot_rooms_room_idRoom` FOREIGN KEY (`idRoom_id`) REFERENCES `hot_rooms_room` (`idRoom`);

--
-- Contraintes pour la table `hot_services_commandeservice`
--
ALTER TABLE `hot_services_commandeservice`
  ADD CONSTRAINT `hot_services_command_idAdmin_id_a8c7dc48_fk_hot_users` FOREIGN KEY (`idAdmin_id`) REFERENCES `hot_users_user` (`idUser`),
  ADD CONSTRAINT `hot_services_command_idClient_id_477351c7_fk_hot_clien` FOREIGN KEY (`idClient_id`) REFERENCES `hot_clients_client` (`idClient`),
  ADD CONSTRAINT `hot_services_command_idItem_id_0c23a7bd_fk_hot_servi` FOREIGN KEY (`idItem_id`) REFERENCES `hot_services_serviceitem` (`idItem`),
  ADD CONSTRAINT `hot_services_command_idStatus_id_27eeaabf_fk_hot_servi` FOREIGN KEY (`idStatus_id`) REFERENCES `hot_services_status` (`idStatus`);

--
-- Contraintes pour la table `hot_services_itemimage`
--
ALTER TABLE `hot_services_itemimage`
  ADD CONSTRAINT `hot_services_itemima_idItem_id_d3185906_fk_hot_servi` FOREIGN KEY (`idItem_id`) REFERENCES `hot_services_serviceitem` (`idItem`);

--
-- Contraintes pour la table `hot_services_service`
--
ALTER TABLE `hot_services_service`
  ADD CONSTRAINT `hot_services_service_idUser_id_432c7993_fk_hot_users_user_idUser` FOREIGN KEY (`idUser_id`) REFERENCES `hot_users_user` (`idUser`);

--
-- Contraintes pour la table `hot_services_serviceitem`
--
ALTER TABLE `hot_services_serviceitem`
  ADD CONSTRAINT `hot_services_service_idService_id_48b3f652_fk_hot_servi` FOREIGN KEY (`idService_id`) REFERENCES `hot_services_service` (`idService`),
  ADD CONSTRAINT `hot_services_service_idUser_id_2aa863fb_fk_hot_users` FOREIGN KEY (`idUser_id`) REFERENCES `hot_users_user` (`idUser`);

--
-- Contraintes pour la table `hot_users_user`
--
ALTER TABLE `hot_users_user`
  ADD CONSTRAINT `hot_users_user_idRole_id_437d67f2_fk_hot_users_role_idRole` FOREIGN KEY (`idRole_id`) REFERENCES `hot_users_role` (`idRole`);

--
-- Contraintes pour la table `hot_users_userpreference`
--
ALTER TABLE `hot_users_userpreference`
  ADD CONSTRAINT `hot_users_userprefer_idUser_id_c99e734a_fk_hot_users` FOREIGN KEY (`idUser_id`) REFERENCES `hot_users_user` (`idUser`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
