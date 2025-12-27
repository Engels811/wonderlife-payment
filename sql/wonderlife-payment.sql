-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Erstellungszeit: 27. Dez 2025 um 02:04
-- Server-Version: 10.11.15-MariaDB-deb11
-- PHP-Version: 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `wonderlife_payments`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `bundle_items`
--

CREATE TABLE `bundle_items` (
  `bundle_id` int(11) NOT NULL,
  `product_name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `cancellations`
--

CREATE TABLE `cancellations` (
  `id` int(11) NOT NULL,
  `subscription_id` int(11) NOT NULL,
  `cancelled_at` datetime DEFAULT NULL,
  `cancelled_by` enum('user','admin','system') DEFAULT 'user',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `payments`
--

CREATE TABLE `payments` (
  `id` int(11) NOT NULL,
  `discord_id` bigint(20) NOT NULL,
  `provider` enum('stripe','tebex','paypal','paysafecard') NOT NULL,
  `product` varchar(150) NOT NULL,
  `amount` int(11) NOT NULL COMMENT 'Betrag in Cents',
  `status` enum('paid','pending','failed','refunded') DEFAULT 'paid',
  `external_id` varchar(100) DEFAULT NULL COMMENT 'Stripe Event ID / Tebex Payment ID',
  `invoice_number` varchar(50) DEFAULT NULL,
  `invoice_pdf` varchar(255) DEFAULT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_email` varchar(150) DEFAULT NULL,
  `customer_address` text DEFAULT NULL,
  `company_name` varchar(150) DEFAULT NULL,
  `vat_id` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `payment_retries`
--

CREATE TABLE `payment_retries` (
  `id` int(11) NOT NULL,
  `subscription_id` int(11) NOT NULL,
  `provider` varchar(20) DEFAULT NULL,
  `attempt` int(11) DEFAULT 0,
  `last_error` text DEFAULT NULL,
  `next_try` datetime DEFAULT NULL,
  `active` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `product_bundles`
--

CREATE TABLE `product_bundles` (
  `id` int(11) NOT NULL,
  `bundle_name` varchar(100) NOT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `subscriptions`
--

CREATE TABLE `subscriptions` (
  `id` int(11) NOT NULL,
  `discord_id` bigint(20) NOT NULL,
  `product` varchar(150) NOT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `active` tinyint(1) DEFAULT 1,
  `auto_renew` tinyint(1) DEFAULT 0,
  `payment_provider` varchar(20) DEFAULT NULL,
  `price_cents` int(11) DEFAULT NULL,
  `billing_interval_days` int(11) DEFAULT NULL,
  `last_renewed` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `vat_rates`
--

CREATE TABLE `vat_rates` (
  `country_code` char(2) NOT NULL,
  `vat_rate` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `vat_rates`
--

INSERT INTO `vat_rates` (`country_code`, `vat_rate`) VALUES
('AT', 20.00),
('DE', 19.00),
('ES', 21.00),
('FR', 20.00),
('IT', 22.00),
('NL', 21.00);

-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `v_payments_clean`
-- (Siehe unten für die tatsächliche Ansicht)
--
CREATE TABLE `v_payments_clean` (
`id` int(11)
,`discord_id` bigint(20)
,`provider` enum('stripe','tebex','paypal','paysafecard')
,`product` varchar(150)
,`amount` int(11)
,`status` enum('paid','pending','failed','refunded')
,`created_at` datetime
);

-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `v_revenue_by_provider`
-- (Siehe unten für die tatsächliche Ansicht)
--
CREATE TABLE `v_revenue_by_provider` (
`provider` enum('stripe','tebex','paypal','paysafecard')
,`payments` bigint(21)
,`revenue` decimal(32,0)
);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `bundle_items`
--
ALTER TABLE `bundle_items`
  ADD PRIMARY KEY (`bundle_id`,`product_name`);

--
-- Indizes für die Tabelle `cancellations`
--
ALTER TABLE `cancellations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_cancel_sub` (`subscription_id`);

--
-- Indizes für die Tabelle `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `external_id` (`external_id`),
  ADD KEY `idx_discord` (`discord_id`),
  ADD KEY `idx_provider` (`provider`),
  ADD KEY `idx_status` (`status`),
  ADD KEY `idx_created` (`created_at`);

--
-- Indizes für die Tabelle `payment_retries`
--
ALTER TABLE `payment_retries`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_retry_active` (`active`),
  ADD KEY `idx_retry_next` (`next_try`);

--
-- Indizes für die Tabelle `product_bundles`
--
ALTER TABLE `product_bundles`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `subscriptions`
--
ALTER TABLE `subscriptions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_sub_discord` (`discord_id`),
  ADD KEY `idx_sub_active` (`active`),
  ADD KEY `idx_sub_end` (`end_date`);

--
-- Indizes für die Tabelle `vat_rates`
--
ALTER TABLE `vat_rates`
  ADD PRIMARY KEY (`country_code`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `cancellations`
--
ALTER TABLE `cancellations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `payment_retries`
--
ALTER TABLE `payment_retries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `product_bundles`
--
ALTER TABLE `product_bundles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `subscriptions`
--
ALTER TABLE `subscriptions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- --------------------------------------------------------

--
-- Struktur des Views `v_payments_clean`
--
DROP TABLE IF EXISTS `v_payments_clean`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_payments_clean`  AS SELECT `payments`.`id` AS `id`, `payments`.`discord_id` AS `discord_id`, `payments`.`provider` AS `provider`, `payments`.`product` AS `product`, `payments`.`amount` AS `amount`, `payments`.`status` AS `status`, `payments`.`created_at` AS `created_at` FROM `payments` WHERE `payments`.`status` = 'paid' ;

-- --------------------------------------------------------

--
-- Struktur des Views `v_revenue_by_provider`
--
DROP TABLE IF EXISTS `v_revenue_by_provider`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_revenue_by_provider`  AS SELECT `payments`.`provider` AS `provider`, count(0) AS `payments`, sum(`payments`.`amount`) AS `revenue` FROM `payments` WHERE `payments`.`status` = 'paid' GROUP BY `payments`.`provider` ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
