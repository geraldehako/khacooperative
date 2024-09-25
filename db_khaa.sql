-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : ven. 04 août 2023 à 08:14
-- Version du serveur : 10.4.28-MariaDB
-- Version de PHP : 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `db.khaa`
--

-- --------------------------------------------------------

--
-- Structure de la table `accounts_utilisateurs`
--

CREATE TABLE `accounts_utilisateurs` (
  `id` bigint(20) NOT NULL,
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
  `photo` varchar(100) DEFAULT NULL,
  `role` varchar(30) NOT NULL,
  `statut` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `accounts_utilisateurs`
--

INSERT INTO `accounts_utilisateurs` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `photo`, `role`, `statut`) VALUES
(1, 'pbkdf2_sha256$390000$F1y3VvpFIB65kZV14kdkhY$2z2veugRtLxYqgWz/B+TE5SDRhVDrYS+aHbA4W7KDrY=', '2023-08-02 14:33:42.753135', 1, 'geraldehako', '', '', 'geraldehako@gmail.com', 1, 1, '2023-08-02 14:16:04.948932', '', 'ADMINISTRATEURSUPER', NULL),
(2, 'pbkdf2_sha256$390000$3kU5rDaWCT5RBp162bTgXY$jVZmgnb6mZR+seDsk4ph/WuxUb3wwtYFAumvuDKfROg=', NULL, 0, 'KOFFI CLARISSE', 'KOFFI', 'CLARISSE', 'd@gmail.com', 0, 1, '2023-08-02 16:34:16.437654', '', 'ACADEMIQUE', 'NON ACTIVE'),
(3, 'pbkdf2_sha256$390000$CW2p6kuYGI4V6VxTBz6XNF$lDx48YZYnRt+kfICUujbL1UBSmjDcAH0kz6PNAWKBHA=', NULL, 0, 'DO MARCEL', 'DO', 'MARCEL', 'b@gmail.com', 0, 1, '2023-08-02 17:16:12.558446', '', 'ACADEMIQUE', 'NON ACTIVE'),
(4, 'pbkdf2_sha256$390000$8OLSR3H5uJQeCHJJa5wh5a$I0+4LrRqZQFH6IzKLs2DyFzXakPJ258Ps1TccCJrADQ=', NULL, 0, 'EHAKO GERALD', 'EHAKO', 'GERALD', 'ded@gmail.com', 0, 1, '2023-08-04 05:10:56.200518', '', 'ACADEMIQUE', 'NON ACTIVE'),
(5, 'pbkdf2_sha256$390000$EzGallMnfZPdERiRKdq8rZ$aZH/Rw85e6FFFVr8I403+GQs/6ursRNs4PmxGLinBJc=', NULL, 0, 'Nja d', 'Nja', 'd', 'frd@gmail.com', 0, 1, '2023-08-04 05:15:09.749582', '', 'ACADEMIQUE', 'NON ACTIVE');

-- --------------------------------------------------------

--
-- Structure de la table `accounts_utilisateurs_groups`
--

CREATE TABLE `accounts_utilisateurs_groups` (
  `id` bigint(20) NOT NULL,
  `utilisateurs_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `accounts_utilisateurs_user_permissions`
--

CREATE TABLE `accounts_utilisateurs_user_permissions` (
  `id` bigint(20) NOT NULL,
  `utilisateurs_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add agent', 6, 'add_agent'),
(22, 'Can change agent', 6, 'change_agent'),
(23, 'Can delete agent', 6, 'delete_agent'),
(24, 'Can view agent', 6, 'view_agent'),
(25, 'Can add clients', 7, 'add_clients'),
(26, 'Can change clients', 7, 'change_clients'),
(27, 'Can delete clients', 7, 'delete_clients'),
(28, 'Can view clients', 7, 'view_clients'),
(29, 'Can add compte epargnes', 8, 'add_compteepargnes'),
(30, 'Can change compte epargnes', 8, 'change_compteepargnes'),
(31, 'Can delete compte epargnes', 8, 'delete_compteepargnes'),
(32, 'Can view compte epargnes', 8, 'view_compteepargnes'),
(33, 'Can add compte prets', 9, 'add_compteprets'),
(34, 'Can change compte prets', 9, 'change_compteprets'),
(35, 'Can delete compte prets', 9, 'delete_compteprets'),
(36, 'Can view compte prets', 9, 'view_compteprets'),
(37, 'Can add genres', 10, 'add_genres'),
(38, 'Can change genres', 10, 'change_genres'),
(39, 'Can delete genres', 10, 'delete_genres'),
(40, 'Can view genres', 10, 'view_genres'),
(41, 'Can add matrimoniales', 11, 'add_matrimoniales'),
(42, 'Can change matrimoniales', 11, 'change_matrimoniales'),
(43, 'Can delete matrimoniales', 11, 'delete_matrimoniales'),
(44, 'Can view matrimoniales', 11, 'view_matrimoniales'),
(45, 'Can add statuts', 12, 'add_statuts'),
(46, 'Can change statuts', 12, 'change_statuts'),
(47, 'Can delete statuts', 12, 'delete_statuts'),
(48, 'Can view statuts', 12, 'view_statuts'),
(49, 'Can add typeprets', 13, 'add_typeprets'),
(50, 'Can change typeprets', 13, 'change_typeprets'),
(51, 'Can delete typeprets', 13, 'delete_typeprets'),
(52, 'Can view typeprets', 13, 'view_typeprets'),
(53, 'Can add transaction pret', 14, 'add_transactionpret'),
(54, 'Can change transaction pret', 14, 'change_transactionpret'),
(55, 'Can delete transaction pret', 14, 'delete_transactionpret'),
(56, 'Can view transaction pret', 14, 'view_transactionpret'),
(57, 'Can add transaction epargne', 15, 'add_transactionepargne'),
(58, 'Can change transaction epargne', 15, 'change_transactionepargne'),
(59, 'Can delete transaction epargne', 15, 'delete_transactionepargne'),
(60, 'Can view transaction epargne', 15, 'view_transactionepargne'),
(61, 'Can add echeancier', 16, 'add_echeancier'),
(62, 'Can change echeancier', 16, 'change_echeancier'),
(63, 'Can delete echeancier', 16, 'delete_echeancier'),
(64, 'Can view echeancier', 16, 'view_echeancier'),
(65, 'Can add actionnaire', 17, 'add_actionnaire'),
(66, 'Can change actionnaire', 17, 'change_actionnaire'),
(67, 'Can delete actionnaire', 17, 'delete_actionnaire'),
(68, 'Can view actionnaire', 17, 'view_actionnaire'),
(69, 'Can add user', 18, 'add_utilisateurs'),
(70, 'Can change user', 18, 'change_utilisateurs'),
(71, 'Can delete user', 18, 'delete_utilisateurs'),
(72, 'Can view user', 18, 'view_utilisateurs'),
(73, 'Can add depense', 19, 'add_depense'),
(74, 'Can change depense', 19, 'change_depense'),
(75, 'Can delete depense', 19, 'delete_depense'),
(76, 'Can view depense', 19, 'view_depense');

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(18, 'accounts', 'utilisateurs'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(17, 'finances', 'actionnaire'),
(6, 'finances', 'agent'),
(7, 'finances', 'clients'),
(8, 'finances', 'compteepargnes'),
(9, 'finances', 'compteprets'),
(19, 'finances', 'depense'),
(16, 'finances', 'echeancier'),
(10, 'finances', 'genres'),
(11, 'finances', 'matrimoniales'),
(12, 'finances', 'statuts'),
(15, 'finances', 'transactionepargne'),
(14, 'finances', 'transactionpret'),
(13, 'finances', 'typeprets'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2023-08-02 14:06:01.842464'),
(2, 'contenttypes', '0002_remove_content_type_name', '2023-08-02 14:06:01.863355'),
(3, 'auth', '0001_initial', '2023-08-02 14:06:01.967445'),
(4, 'auth', '0002_alter_permission_name_max_length', '2023-08-02 14:06:02.003036'),
(5, 'auth', '0003_alter_user_email_max_length', '2023-08-02 14:06:02.011342'),
(6, 'auth', '0004_alter_user_username_opts', '2023-08-02 14:06:02.018431'),
(7, 'auth', '0005_alter_user_last_login_null', '2023-08-02 14:06:02.024883'),
(8, 'auth', '0006_require_contenttypes_0002', '2023-08-02 14:06:02.027413'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2023-08-02 14:06:02.033834'),
(10, 'auth', '0008_alter_user_username_max_length', '2023-08-02 14:06:02.039740'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2023-08-02 14:06:02.045352'),
(12, 'auth', '0010_alter_group_name_max_length', '2023-08-02 14:06:02.053933'),
(13, 'auth', '0011_update_proxy_permissions', '2023-08-02 14:06:02.058942'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2023-08-02 14:06:02.064475'),
(15, 'accounts', '0001_initial', '2023-08-02 14:06:02.198012'),
(16, 'admin', '0001_initial', '2023-08-02 14:06:02.243813'),
(17, 'admin', '0002_logentry_remove_auto_add', '2023-08-02 14:06:02.250615'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2023-08-02 14:06:02.257006'),
(19, 'finances', '0001_initial', '2023-08-02 14:06:02.710181'),
(20, 'sessions', '0001_initial', '2023-08-02 14:06:02.728788'),
(21, 'finances', '0002_actionnaire_apport_actionnaire_pourcentage', '2023-08-02 18:06:58.845711'),
(22, 'finances', '0003_echeancier_montant_interet_depense', '2023-08-03 11:32:48.481752');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('83g0hj5g7q0aw60xaaozmvonzm5e1a8t', 'e30:1qRCu1:3ibhh4XNrWbtCwk0iWLjlS1kVgqFkzMuBu9DenA7hPw', '2023-08-16 14:32:41.875568'),
('wgt6tvdpenzsm1ne3ybbfhz5jsns3zx5', '.eJxVjEEOwiAQRe_C2hAGUBiX7j0DGZipVA1NSrsy3l2bdKHb_977L5VoXWpau8xpZHVWoA6_W6bykLYBvlO7TbpMbZnHrDdF77Tr68TyvOzu30GlXr-19U7yEMOJ0eWIAmEQKw6sKRIMIxtvC0MBEe_AIOWA0RbxHo8uE6v3B-VJOAI:1qRCv0:TLiiHA0zTGFybdxGGaZXoOAOJ36eHTctMpNUbcQPaVk', '2023-08-16 14:33:42.757196');

-- --------------------------------------------------------

--
-- Structure de la table `finances_actionnaire`
--

CREATE TABLE `finances_actionnaire` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `adresse` varchar(200) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `apport` decimal(10,2) DEFAULT NULL,
  `pourcentage` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_actionnaire`
--

INSERT INTO `finances_actionnaire` (`id`, `nom`, `prenom`, `adresse`, `telephone`, `email`, `user_id`, `apport`, `pourcentage`) VALUES
(1, 'EHAKO', 'GERALD', '@', '0', 'ded@gmail.com', 4, 200000.00, 25.00),
(2, 'Nja', 'd', 'd', '0', 'frd@gmail.com', 5, 1000000.00, 10.00);

-- --------------------------------------------------------

--
-- Structure de la table `finances_agent`
--

CREATE TABLE `finances_agent` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `prenom` varchar(100) NOT NULL,
  `adresse` varchar(200) NOT NULL,
  `telephone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_agent`
--

INSERT INTO `finances_agent` (`id`, `nom`, `prenom`, `adresse`, `telephone`, `email`, `user_id`) VALUES
(1, 'KOFFI', 'CLARISSE', '@', '90', 'd@gmail.com', 2),
(2, 'DO', 'MARCEL', 'S', '0', 'b@gmail.com', 3);

-- --------------------------------------------------------

--
-- Structure de la table `finances_clients`
--

CREATE TABLE `finances_clients` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `prenom` varchar(100) DEFAULT NULL,
  `adresse` varchar(200) DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  `date_inscription` date DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `piece_identite_scan` varchar(100) DEFAULT NULL,
  `profession` varchar(100) DEFAULT NULL,
  `date_naissance` date NOT NULL,
  `lieu_naissance` varchar(100) DEFAULT NULL,
  `type_piece_identite` varchar(20) NOT NULL,
  `numero_piece_identite` varchar(100) DEFAULT NULL,
  `validite_piece_identite_debut` date NOT NULL,
  `validite_piece_identite_fin` date NOT NULL,
  `ville_village` varchar(100) DEFAULT NULL,
  `matrimoniale_id` bigint(20) DEFAULT NULL,
  `sexe_id` bigint(20) DEFAULT NULL,
  `statut_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_clients`
--

INSERT INTO `finances_clients` (`id`, `nom`, `prenom`, `adresse`, `telephone`, `email`, `date_inscription`, `photo`, `piece_identite_scan`, `profession`, `date_naissance`, `lieu_naissance`, `type_piece_identite`, `numero_piece_identite`, `validite_piece_identite_debut`, `validite_piece_identite_fin`, `ville_village`, `matrimoniale_id`, `sexe_id`, `statut_id`) VALUES
(1, 'DON1', 'EHAKO', 'N\'DA KOUAME GERALD', '07 47 86 21 68', 'd@gmail.com', '2023-08-02', 'Images/Photos/Clients/DSC_0368_copie.jpg', 'Images/Photos/Clients/Pieceidentite/DSC_0368_copie.jpg', 'INFORMATICIEN', '2023-08-02', 'YAKRO', 'CNI', 'CD', '2023-08-15', '2023-08-24', 'YAKRO', 2, 1, 1),
(2, 'xcv', 'xcv', 'd', 'fr', 'dcvf@gmail.com', '2023-08-03', 'Images/Photos/Clients/DSC_0368_copie_sQxsLma.jpg', 'Images/Photos/Clients/Pieceidentite/DSC_0368_copie_GYFRZhR.jpg', 'rr', '2023-08-04', 'rr', 'CNI', 'rr', '2023-08-10', '2023-08-11', 'rrr', 2, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `finances_compteepargnes`
--

CREATE TABLE `finances_compteepargnes` (
  `id` bigint(20) NOT NULL,
  `numero_compte` varchar(20) NOT NULL,
  `solde` decimal(10,2) NOT NULL,
  `client_id` bigint(20) DEFAULT NULL,
  `statut_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_compteepargnes`
--

INSERT INTO `finances_compteepargnes` (`id`, `numero_compte`, `solde`, `client_id`, `statut_id`) VALUES
(1, 'EP1', 100000.00, 1, 1),
(2, 'EP2', 0.00, 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `finances_compteprets`
--

CREATE TABLE `finances_compteprets` (
  `id` bigint(20) NOT NULL,
  `numero_compte` varchar(20) NOT NULL,
  `solde` decimal(10,2) NOT NULL,
  `taux_interet` decimal(5,2) NOT NULL,
  `duree_en_mois` int(10) UNSIGNED NOT NULL CHECK (`duree_en_mois` >= 0),
  `date_debut_pret` date NOT NULL,
  `date_fin_pret` date NOT NULL,
  `somme_initiale` decimal(10,2) NOT NULL,
  `domicile_bancaire` varchar(200) DEFAULT NULL,
  `date_demande` date DEFAULT NULL,
  `client_id` bigint(20) DEFAULT NULL,
  `statut_id` bigint(20) NOT NULL,
  `type_pret_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_compteprets`
--

INSERT INTO `finances_compteprets` (`id`, `numero_compte`, `solde`, `taux_interet`, `duree_en_mois`, `date_debut_pret`, `date_fin_pret`, `somme_initiale`, `domicile_bancaire`, `date_demande`, `client_id`, `statut_id`, `type_pret_id`) VALUES
(1, 'DONEPP', 56000.00, 1.00, 12, '2023-08-02', '2024-07-27', 50000.00, 'YAKRO', '2023-08-02', 1, 1, 1),
(2, 'BH', 1120000.00, 1.00, 12, '2023-08-02', '2024-07-27', 1000000.00, '-', '2023-08-02', 1, 2, 1),
(3, 'woun', 1250000.00, 1.00, 10, '2023-08-07', '2024-06-02', 1000000.00, 'vd', '2023-08-03', 1, 1, 2),
(4, 'xcohgn', 1650000.00, 1.00, 10, '2023-08-12', '2024-06-07', 1500000.00, 'woyv', '2023-08-03', 1, 1, 1),
(5, 'wq', 52500.00, 1.00, 5, '2023-08-07', '2024-01-04', 50000.00, 'kl', '2023-08-03', 1, 1, 1),
(6, 'qp0', 672000.00, 1.00, 12, '2023-08-11', '2024-08-05', 600000.00, 'qs', '2023-08-03', 2, 1, 3),
(7, 'xou', 1100000.00, 1.00, 10, '2023-08-07', '2024-06-02', 1000000.00, 'cfr', '2023-08-03', 2, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `finances_depense`
--

CREATE TABLE `finances_depense` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(100) NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `date` datetime(6) NOT NULL,
  `agent_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_depense`
--

INSERT INTO `finances_depense` (`id`, `nom`, `montant`, `date`, `agent_id`) VALUES
(1, 'courant', 21000.00, '2023-08-03 11:52:02.818789', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `finances_echeancier`
--

CREATE TABLE `finances_echeancier` (
  `id` bigint(20) NOT NULL,
  `date_echeance` date NOT NULL,
  `montant_echeance` decimal(10,2) NOT NULL,
  `est_paye` tinyint(1) NOT NULL,
  `compte_pret_id` bigint(20) NOT NULL,
  `montant_interet` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_echeancier`
--

INSERT INTO `finances_echeancier` (`id`, `date_echeance`, `montant_echeance`, `est_paye`, `compte_pret_id`, `montant_interet`) VALUES
(12, '2023-08-07', 93333.33, 1, 2, 10000.00),
(13, '2023-10-02', 93333.33, 1, 2, 10000.00),
(14, '2023-11-02', 93333.33, 1, 2, 10000.00),
(15, '2023-12-02', 93333.33, 1, 2, 10000.00),
(16, '2024-01-02', 93333.33, 1, 2, 10000.00),
(17, '2024-02-02', 93333.33, 1, 2, 10000.00),
(18, '2024-03-02', 93333.33, 1, 2, 10000.00),
(19, '2024-04-02', 93333.33, 1, 2, 10000.00),
(20, '2024-05-02', 93333.33, 1, 2, 10000.00),
(21, '2024-06-02', 93333.33, 1, 2, 10000.00),
(22, '2024-07-02', 93333.33, 1, 2, 10000.00),
(23, '2023-09-07', 125000.00, 0, 3, 25000.00),
(24, '2023-10-07', 125000.00, 0, 3, 25000.00),
(25, '2023-11-07', 125000.00, 0, 3, 25000.00),
(26, '2023-12-07', 125000.00, 0, 3, 25000.00),
(27, '2024-01-07', 125000.00, 0, 3, 25000.00),
(28, '2024-02-07', 125000.00, 0, 3, 25000.00),
(29, '2024-03-07', 125000.00, 0, 3, 25000.00),
(30, '2024-04-07', 125000.00, 0, 3, 25000.00),
(31, '2024-05-07', 125000.00, 0, 3, 25000.00),
(32, '2023-09-12', 165000.00, 0, 4, 15000.00),
(33, '2023-10-12', 165000.00, 0, 4, 15000.00),
(34, '2023-11-12', 165000.00, 0, 4, 15000.00),
(35, '2023-12-12', 165000.00, 0, 4, 15000.00),
(36, '2024-01-12', 165000.00, 0, 4, 15000.00),
(37, '2024-02-12', 165000.00, 0, 4, 15000.00),
(38, '2024-03-12', 165000.00, 0, 4, 15000.00),
(39, '2024-04-12', 165000.00, 0, 4, 15000.00),
(40, '2024-05-12', 165000.00, 0, 4, 15000.00),
(41, '2023-09-07', 10500.00, 0, 5, NULL),
(42, '2023-10-07', 10500.00, 0, 5, NULL),
(43, '2023-11-07', 10500.00, 0, 5, NULL),
(44, '2023-12-07', 10500.00, 0, 5, NULL),
(45, '2023-09-11', 56000.00, 0, 6, NULL),
(46, '2023-10-11', 56000.00, 0, 6, NULL),
(47, '2023-11-11', 56000.00, 0, 6, NULL),
(48, '2023-12-11', 56000.00, 0, 6, NULL),
(49, '2024-01-11', 56000.00, 0, 6, NULL),
(50, '2024-02-11', 56000.00, 0, 6, NULL),
(51, '2024-03-11', 56000.00, 0, 6, NULL),
(52, '2024-04-11', 56000.00, 0, 6, NULL),
(53, '2024-05-11', 56000.00, 0, 6, NULL),
(54, '2024-06-11', 56000.00, 0, 6, NULL),
(55, '2024-07-11', 56000.00, 0, 6, NULL),
(56, '2023-09-07', 110000.00, 0, 7, 10000.00),
(57, '2023-10-07', 110000.00, 0, 7, 10000.00),
(58, '2023-11-07', 110000.00, 0, 7, 10000.00),
(59, '2023-12-07', 110000.00, 0, 7, 10000.00),
(60, '2024-01-07', 110000.00, 0, 7, 10000.00),
(61, '2024-02-07', 110000.00, 0, 7, 10000.00),
(62, '2024-03-07', 110000.00, 0, 7, 10000.00),
(63, '2024-04-07', 110000.00, 0, 7, 10000.00),
(64, '2024-05-07', 110000.00, 0, 7, 10000.00);

-- --------------------------------------------------------

--
-- Structure de la table `finances_genres`
--

CREATE TABLE `finances_genres` (
  `id` bigint(20) NOT NULL,
  `sexe` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_genres`
--

INSERT INTO `finances_genres` (`id`, `sexe`) VALUES
(1, 'Masculin'),
(2, 'Féminin');

-- --------------------------------------------------------

--
-- Structure de la table `finances_matrimoniales`
--

CREATE TABLE `finances_matrimoniales` (
  `id` bigint(20) NOT NULL,
  `matrimoniale` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_matrimoniales`
--

INSERT INTO `finances_matrimoniales` (`id`, `matrimoniale`) VALUES
(1, 'Célibataire'),
(2, 'marié(e)'),
(3, 'Divorcé(e)'),
(4, 'Veuf(ve)');

-- --------------------------------------------------------

--
-- Structure de la table `finances_statuts`
--

CREATE TABLE `finances_statuts` (
  `id` bigint(20) NOT NULL,
  `statut` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_statuts`
--

INSERT INTO `finances_statuts` (`id`, `statut`) VALUES
(1, 'Actif'),
(2, 'Non Actif');

-- --------------------------------------------------------

--
-- Structure de la table `finances_transactionepargne`
--

CREATE TABLE `finances_transactionepargne` (
  `id` bigint(20) NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `type_transaction` varchar(20) NOT NULL,
  `date_transaction` datetime(6) NOT NULL,
  `agent_id` bigint(20) DEFAULT NULL,
  `compte_epargne_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_transactionepargne`
--

INSERT INTO `finances_transactionepargne` (`id`, `montant`, `type_transaction`, `date_transaction`, `agent_id`, `compte_epargne_id`) VALUES
(1, 100000.00, 'Depot', '2023-08-02 15:02:47.646141', NULL, 1);

-- --------------------------------------------------------

--
-- Structure de la table `finances_transactionpret`
--

CREATE TABLE `finances_transactionpret` (
  `id` bigint(20) NOT NULL,
  `montant` decimal(10,2) NOT NULL,
  `type_transaction` varchar(20) NOT NULL,
  `date_transaction` datetime(6) NOT NULL,
  `agent_id` bigint(20) DEFAULT NULL,
  `compte_pret_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `finances_typeprets`
--

CREATE TABLE `finances_typeprets` (
  `id` bigint(20) NOT NULL,
  `type_pret` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `finances_typeprets`
--

INSERT INTO `finances_typeprets` (`id`, `type_pret`) VALUES
(1, 'TYPE DE PRET le client ayant un compte avec KHA'),
(2, 'TYPE DE PRET avec versement d’une garantie'),
(3, 'TYPE DE PRET ss verset de la garantie au prealabl');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `accounts_utilisateurs`
--
ALTER TABLE `accounts_utilisateurs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `accounts_utilisateurs_groups`
--
ALTER TABLE `accounts_utilisateurs_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_utilisateurs_gr_utilisateurs_id_group_id_05896068_uniq` (`utilisateurs_id`,`group_id`),
  ADD KEY `accounts_utilisateurs_groups_group_id_87ba4522_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `accounts_utilisateurs_user_permissions`
--
ALTER TABLE `accounts_utilisateurs_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `accounts_utilisateurs_us_utilisateurs_id_permissi_dae4d4bb_uniq` (`utilisateurs_id`,`permission_id`),
  ADD KEY `accounts_utilisateur_permission_id_52450dcb_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_accounts_utilisateurs_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `finances_actionnaire`
--
ALTER TABLE `finances_actionnaire`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Index pour la table `finances_agent`
--
ALTER TABLE `finances_agent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Index pour la table `finances_clients`
--
ALTER TABLE `finances_clients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `finances_clients_matrimoniale_id_ed505b55_fk_finances_` (`matrimoniale_id`),
  ADD KEY `finances_clients_sexe_id_b22a5896_fk_finances_genres_id` (`sexe_id`),
  ADD KEY `finances_clients_statut_id_13c78f8a_fk_finances_statuts_id` (`statut_id`);

--
-- Index pour la table `finances_compteepargnes`
--
ALTER TABLE `finances_compteepargnes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_compte` (`numero_compte`),
  ADD KEY `finances_compteeparg_statut_id_3b006718_fk_finances_` (`statut_id`),
  ADD KEY `finances_compteeparg_client_id_29ebde75_fk_finances_` (`client_id`);

--
-- Index pour la table `finances_compteprets`
--
ALTER TABLE `finances_compteprets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_compte` (`numero_compte`),
  ADD KEY `finances_compteprets_statut_id_9bfb8505_fk_finances_statuts_id` (`statut_id`),
  ADD KEY `finances_compteprets_type_pret_id_0baebd7b_fk_finances_` (`type_pret_id`),
  ADD KEY `finances_compteprets_client_id_0af08e8e_fk_finances_clients_id` (`client_id`);

--
-- Index pour la table `finances_depense`
--
ALTER TABLE `finances_depense`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finances_depense_agent_id_e7be01f6_fk_finances_agent_id` (`agent_id`);

--
-- Index pour la table `finances_echeancier`
--
ALTER TABLE `finances_echeancier`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finances_echeancier_compte_pret_id_42532909_fk_finances_` (`compte_pret_id`);

--
-- Index pour la table `finances_genres`
--
ALTER TABLE `finances_genres`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `finances_matrimoniales`
--
ALTER TABLE `finances_matrimoniales`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `finances_statuts`
--
ALTER TABLE `finances_statuts`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `finances_transactionepargne`
--
ALTER TABLE `finances_transactionepargne`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finances_transaction_agent_id_4d0ed1bc_fk_finances_` (`agent_id`),
  ADD KEY `finances_transaction_compte_epargne_id_0b5eb1a4_fk_finances_` (`compte_epargne_id`);

--
-- Index pour la table `finances_transactionpret`
--
ALTER TABLE `finances_transactionpret`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finances_transactionpret_agent_id_1f094ca2_fk_finances_agent_id` (`agent_id`),
  ADD KEY `finances_transaction_compte_pret_id_a2f6cb77_fk_finances_` (`compte_pret_id`);

--
-- Index pour la table `finances_typeprets`
--
ALTER TABLE `finances_typeprets`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `accounts_utilisateurs`
--
ALTER TABLE `accounts_utilisateurs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `accounts_utilisateurs_groups`
--
ALTER TABLE `accounts_utilisateurs_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `accounts_utilisateurs_user_permissions`
--
ALTER TABLE `accounts_utilisateurs_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT pour la table `finances_actionnaire`
--
ALTER TABLE `finances_actionnaire`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `finances_agent`
--
ALTER TABLE `finances_agent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `finances_clients`
--
ALTER TABLE `finances_clients`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `finances_compteepargnes`
--
ALTER TABLE `finances_compteepargnes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `finances_compteprets`
--
ALTER TABLE `finances_compteprets`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT pour la table `finances_depense`
--
ALTER TABLE `finances_depense`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `finances_echeancier`
--
ALTER TABLE `finances_echeancier`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT pour la table `finances_genres`
--
ALTER TABLE `finances_genres`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `finances_matrimoniales`
--
ALTER TABLE `finances_matrimoniales`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `finances_statuts`
--
ALTER TABLE `finances_statuts`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT pour la table `finances_transactionepargne`
--
ALTER TABLE `finances_transactionepargne`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `finances_transactionpret`
--
ALTER TABLE `finances_transactionpret`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `finances_typeprets`
--
ALTER TABLE `finances_typeprets`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `accounts_utilisateurs_groups`
--
ALTER TABLE `accounts_utilisateurs_groups`
  ADD CONSTRAINT `accounts_utilisateur_utilisateurs_id_ad936235_fk_accounts_` FOREIGN KEY (`utilisateurs_id`) REFERENCES `accounts_utilisateurs` (`id`),
  ADD CONSTRAINT `accounts_utilisateurs_groups_group_id_87ba4522_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `accounts_utilisateurs_user_permissions`
--
ALTER TABLE `accounts_utilisateurs_user_permissions`
  ADD CONSTRAINT `accounts_utilisateur_permission_id_52450dcb_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `accounts_utilisateur_utilisateurs_id_0e8e7b86_fk_accounts_` FOREIGN KEY (`utilisateurs_id`) REFERENCES `accounts_utilisateurs` (`id`);

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
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_utilisateurs_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_utilisateurs` (`id`);

--
-- Contraintes pour la table `finances_actionnaire`
--
ALTER TABLE `finances_actionnaire`
  ADD CONSTRAINT `finances_actionnaire_user_id_706290a4_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_utilisateurs` (`id`);

--
-- Contraintes pour la table `finances_agent`
--
ALTER TABLE `finances_agent`
  ADD CONSTRAINT `finances_agent_user_id_3204ac07_fk_accounts_utilisateurs_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_utilisateurs` (`id`);

--
-- Contraintes pour la table `finances_clients`
--
ALTER TABLE `finances_clients`
  ADD CONSTRAINT `finances_clients_matrimoniale_id_ed505b55_fk_finances_` FOREIGN KEY (`matrimoniale_id`) REFERENCES `finances_matrimoniales` (`id`),
  ADD CONSTRAINT `finances_clients_sexe_id_b22a5896_fk_finances_genres_id` FOREIGN KEY (`sexe_id`) REFERENCES `finances_genres` (`id`),
  ADD CONSTRAINT `finances_clients_statut_id_13c78f8a_fk_finances_statuts_id` FOREIGN KEY (`statut_id`) REFERENCES `finances_statuts` (`id`);

--
-- Contraintes pour la table `finances_compteepargnes`
--
ALTER TABLE `finances_compteepargnes`
  ADD CONSTRAINT `finances_compteeparg_client_id_29ebde75_fk_finances_` FOREIGN KEY (`client_id`) REFERENCES `finances_clients` (`id`),
  ADD CONSTRAINT `finances_compteeparg_statut_id_3b006718_fk_finances_` FOREIGN KEY (`statut_id`) REFERENCES `finances_statuts` (`id`);

--
-- Contraintes pour la table `finances_compteprets`
--
ALTER TABLE `finances_compteprets`
  ADD CONSTRAINT `finances_compteprets_client_id_0af08e8e_fk_finances_clients_id` FOREIGN KEY (`client_id`) REFERENCES `finances_clients` (`id`),
  ADD CONSTRAINT `finances_compteprets_statut_id_9bfb8505_fk_finances_statuts_id` FOREIGN KEY (`statut_id`) REFERENCES `finances_statuts` (`id`),
  ADD CONSTRAINT `finances_compteprets_type_pret_id_0baebd7b_fk_finances_` FOREIGN KEY (`type_pret_id`) REFERENCES `finances_typeprets` (`id`);

--
-- Contraintes pour la table `finances_depense`
--
ALTER TABLE `finances_depense`
  ADD CONSTRAINT `finances_depense_agent_id_e7be01f6_fk_finances_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `finances_agent` (`id`);

--
-- Contraintes pour la table `finances_echeancier`
--
ALTER TABLE `finances_echeancier`
  ADD CONSTRAINT `finances_echeancier_compte_pret_id_42532909_fk_finances_` FOREIGN KEY (`compte_pret_id`) REFERENCES `finances_compteprets` (`id`);

--
-- Contraintes pour la table `finances_transactionepargne`
--
ALTER TABLE `finances_transactionepargne`
  ADD CONSTRAINT `finances_transaction_agent_id_4d0ed1bc_fk_finances_` FOREIGN KEY (`agent_id`) REFERENCES `finances_agent` (`id`),
  ADD CONSTRAINT `finances_transaction_compte_epargne_id_0b5eb1a4_fk_finances_` FOREIGN KEY (`compte_epargne_id`) REFERENCES `finances_compteepargnes` (`id`);

--
-- Contraintes pour la table `finances_transactionpret`
--
ALTER TABLE `finances_transactionpret`
  ADD CONSTRAINT `finances_transaction_compte_pret_id_a2f6cb77_fk_finances_` FOREIGN KEY (`compte_pret_id`) REFERENCES `finances_compteprets` (`id`),
  ADD CONSTRAINT `finances_transactionpret_agent_id_1f094ca2_fk_finances_agent_id` FOREIGN KEY (`agent_id`) REFERENCES `finances_agent` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
