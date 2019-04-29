-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Apr 29, 2019 at 12:38 AM
-- Server version: 5.7.25
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `animalshelter`
--

-- --------------------------------------------------------

--
-- Table structure for table `Admin`
--

CREATE TABLE `Admin` (
  `AdminID` char(10) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Admin`
--

INSERT INTO `Admin` (`AdminID`, `Username`) VALUES
('1', 'deviprasad1');

-- --------------------------------------------------------

--
-- Table structure for table `ADOPTION`
--

CREATE TABLE `ADOPTION` (
  `Adoption_id` varchar(10) NOT NULL,
  `Adoption_fee` int(11) NOT NULL,
  `Payment_method` varchar(30) DEFAULT NULL,
  `User_id` varchar(10) DEFAULT NULL,
  `Animal_id` varchar(10) DEFAULT NULL,
  `adoption_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ADOPTION`
--

INSERT INTO `ADOPTION` (`Adoption_id`, `Adoption_fee`, `Payment_method`, `User_id`, `Animal_id`, `adoption_date`) VALUES
('2a1d19', 210, 'VISA', '1', '33e90c', '2019-04-29');

-- --------------------------------------------------------

--
-- Table structure for table `Adoption_fee`
--

CREATE TABLE `Adoption_fee` (
  `Animal_id` char(10) DEFAULT NULL,
  `Adoption_fee` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Adoption_fee`
--

INSERT INTO `Adoption_fee` (`Animal_id`, `Adoption_fee`) VALUES
('1', '200'),
('33e90c', '210');

-- --------------------------------------------------------

--
-- Table structure for table `ANIMAL`
--

CREATE TABLE `ANIMAL` (
  `Animal_id` char(10) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Age` int(11) NOT NULL,
  `Type` varchar(50) NOT NULL,
  `Color` varchar(50) DEFAULT NULL,
  `Availability` varchar(10) NOT NULL,
  `Size` varchar(10) DEFAULT NULL,
  `Description` varchar(100) DEFAULT NULL,
  `Ported_date` date DEFAULT NULL,
  `Breed_id` varchar(30) DEFAULT NULL,
  `image` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ANIMAL`
--

INSERT INTO `ANIMAL` (`Animal_id`, `Name`, `Age`, `Type`, `Color`, `Availability`, `Size`, `Description`, `Ported_date`, `Breed_id`, `image`) VALUES
('1', 'Freddy', 20, 'Awesome', 'White', 'Yes', '20', 'Great Awesome', '2019-04-10', '1', 'dog-2.jpg'),
('33e90c', 'Maddy1', 3, 'Dog', 'White', 'NO', '20', 'Awesome Dog', '2019-04-27', '2', '02.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `BREED`
--

CREATE TABLE `BREED` (
  `Breed_id` varchar(10) NOT NULL,
  `Breed` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `BREED`
--

INSERT INTO `BREED` (`Breed_id`, `Breed`) VALUES
('1', 'alpline'),
('2', 'german shepherd');

-- --------------------------------------------------------

--
-- Table structure for table `DONATIONS`
--

CREATE TABLE `DONATIONS` (
  `User_id` char(10) DEFAULT NULL,
  `Animal_id` varchar(50) DEFAULT NULL,
  `DonationID` char(10) NOT NULL,
  `Amaount` varchar(10) NOT NULL,
  `donation_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `DONATIONS`
--

INSERT INTO `DONATIONS` (`User_id`, `Animal_id`, `DonationID`, `Amaount`, `donation_date`) VALUES
('1', '33e90c', '100', '1100', '2019-04-26'),
('2', '33e90c', '101', '300', '2019-04-27'),
('1', '33e90c', '75b950', '20', '2019-04-28');

-- --------------------------------------------------------

--
-- Table structure for table `INQUIRIES`
--

CREATE TABLE `INQUIRIES` (
  `User_id` char(10) DEFAULT NULL,
  `Animal_id` char(10) DEFAULT NULL,
  `Response` varchar(1000) NOT NULL,
  `Inquire_id` char(10) NOT NULL,
  `Message` varchar(1000) NOT NULL,
  `Assign_Admin_ID` char(10) DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `INQUIRIES`
--

INSERT INTO `INQUIRIES` (`User_id`, `Animal_id`, `Response`, `Inquire_id`, `Message`, `Assign_Admin_ID`, `date`) VALUES
('1', '33e90c', 'Hey, thanks for contacting', '1', 'Can you tell me more?', '1', '2019-04-28'),
('1', '33e90c', 'Hey, yes you can come', 'f6fdaf', 'Hey can I come to visit', '1', '2019-04-28');

-- --------------------------------------------------------

--
-- Table structure for table `Profile`
--

CREATE TABLE `Profile` (
  `profile_id` char(10) NOT NULL,
  `First_name` varchar(50) DEFAULT NULL,
  `Last_name` varchar(50) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Password` varchar(20) DEFAULT NULL,
  `Mobile_number` varchar(10) DEFAULT NULL,
  `DateCreated` date DEFAULT NULL,
  `IsActive` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Profile`
--

INSERT INTO `Profile` (`profile_id`, `First_name`, `Last_name`, `Username`, `Email`, `Password`, `Mobile_number`, `DateCreated`, `IsActive`) VALUES
('1', 'Devi Prasad', 'Tripathy', 'deviprasad1', 'tripathy.devi7@gmail.com', '06811@mummy', '6822569902', '2019-04-27', 1),
('2', 'Nick', 'Miller', 'nickmiller', 'nick@gmail.com', '06811@mummt', '6822569903', '2019-04-27', 1),
('23f86d', 'Diptin', 'Dahal', 'diptin', 'diptin@gmail.com', '06811@mummy', '6828458954', '2019-04-29', 1);

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `User_id` char(10) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`User_id`, `Username`) VALUES
(NULL, NULL),
(NULL, NULL),
('1', 'deviprasad1'),
('2', 'nickmiller'),
('23f86d', 'diptin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Admin`
--
ALTER TABLE `Admin`
  ADD KEY `Username` (`Username`),
  ADD KEY `AdminID` (`AdminID`);

--
-- Indexes for table `ADOPTION`
--
ALTER TABLE `ADOPTION`
  ADD PRIMARY KEY (`Adoption_id`),
  ADD KEY `Adoption_ibfk_1` (`User_id`),
  ADD KEY `Adoption_ibfk_2` (`Animal_id`);

--
-- Indexes for table `Adoption_fee`
--
ALTER TABLE `Adoption_fee`
  ADD KEY `Adoption_frfe_1` (`Animal_id`);

--
-- Indexes for table `ANIMAL`
--
ALTER TABLE `ANIMAL`
  ADD PRIMARY KEY (`Animal_id`),
  ADD KEY `Breed_id` (`Breed_id`);

--
-- Indexes for table `BREED`
--
ALTER TABLE `BREED`
  ADD PRIMARY KEY (`Breed_id`);

--
-- Indexes for table `DONATIONS`
--
ALTER TABLE `DONATIONS`
  ADD PRIMARY KEY (`DonationID`),
  ADD KEY `User_id` (`User_id`),
  ADD KEY `Animal_id` (`Animal_id`);

--
-- Indexes for table `INQUIRIES`
--
ALTER TABLE `INQUIRIES`
  ADD PRIMARY KEY (`Inquire_id`),
  ADD KEY `User_id` (`User_id`),
  ADD KEY `Animal_id` (`Animal_id`),
  ADD KEY `Assign_Admin_ID` (`Assign_Admin_ID`);

--
-- Indexes for table `Profile`
--
ALTER TABLE `Profile`
  ADD PRIMARY KEY (`profile_id`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD KEY `User_id` (`User_id`),
  ADD KEY `Username` (`Username`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Admin`
--
ALTER TABLE `Admin`
  ADD CONSTRAINT `Admin_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `Profile` (`Username`) ON DELETE SET NULL,
  ADD CONSTRAINT `Admin_ibfk_2` FOREIGN KEY (`AdminID`) REFERENCES `Profile` (`profile_id`) ON DELETE SET NULL;

--
-- Constraints for table `ADOPTION`
--
ALTER TABLE `ADOPTION`
  ADD CONSTRAINT `Adoption_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `User` (`User_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `Adoption_ibfk_2` FOREIGN KEY (`Animal_id`) REFERENCES `ANIMAL` (`Animal_id`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints for table `Adoption_fee`
--
ALTER TABLE `Adoption_fee`
  ADD CONSTRAINT `Adoption_frfe_1` FOREIGN KEY (`Animal_id`) REFERENCES `ANIMAL` (`Animal_id`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints for table `ANIMAL`
--
ALTER TABLE `ANIMAL`
  ADD CONSTRAINT `ANIMAL_ibfk_1` FOREIGN KEY (`Breed_id`) REFERENCES `BREED` (`Breed_id`) ON DELETE SET NULL;

--
-- Constraints for table `DONATIONS`
--
ALTER TABLE `DONATIONS`
  ADD CONSTRAINT `DONATIONS_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `User` (`User_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `DONATIONS_ibfk_2` FOREIGN KEY (`Animal_id`) REFERENCES `ANIMAL` (`Animal_id`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints for table `INQUIRIES`
--
ALTER TABLE `INQUIRIES`
  ADD CONSTRAINT `INQUIRIES_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `User` (`User_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `INQUIRIES_ibfk_2` FOREIGN KEY (`Animal_id`) REFERENCES `ANIMAL` (`Animal_id`) ON DELETE SET NULL ON UPDATE SET NULL,
  ADD CONSTRAINT `INQUIRIES_ibfk_3` FOREIGN KEY (`Assign_Admin_ID`) REFERENCES `Admin` (`AdminID`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints for table `User`
--
ALTER TABLE `User`
  ADD CONSTRAINT `User_ibfk_1` FOREIGN KEY (`User_id`) REFERENCES `Profile` (`profile_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `User_ibfk_2` FOREIGN KEY (`Username`) REFERENCES `Profile` (`Username`) ON DELETE SET NULL;
