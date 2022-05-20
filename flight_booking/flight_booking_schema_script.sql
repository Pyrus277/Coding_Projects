-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema FlightBooking
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema FlightBooking
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `FlightBooking` DEFAULT CHARACTER SET utf8 ;
USE `FlightBooking` ;

-- -----------------------------------------------------
-- Table `FlightBooking`.`passengers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FlightBooking`.`passengers` (
  `passenger_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`passenger_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FlightBooking`.`airlines`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FlightBooking`.`airlines` (
  `airline_id` INT NOT NULL AUTO_INCREMENT,
  `airline_name` INT NOT NULL,
  PRIMARY KEY (`airline_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FlightBooking`.`airports`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FlightBooking`.`airports` (
  `airport_id` VARCHAR(50) NOT NULL,
  `iata_code` VARCHAR(50) NOT NULL,
  `airport_name` VARCHAR(50) NOT NULL,
  `city` VARCHAR(50) NOT NULL,
  `state` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`airport_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FlightBooking`.`flights`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FlightBooking`.`flights` (
  `flight_id` INT NOT NULL AUTO_INCREMENT,
  `number` VARCHAR(50) NOT NULL,
  `departure_date_time` DATETIME NOT NULL,
  `arrival_date_time` VARCHAR(50) NOT NULL,
  `duration_minutes` SMALLINT NOT NULL,
  `distance_miles` SMALLINT NOT NULL,
  `arrival_airport_id` VARCHAR(50) NOT NULL,
  `departure_airport_id` VARCHAR(50) NOT NULL,
  `airline_id` INT NOT NULL,
  PRIMARY KEY (`flight_id`),
  INDEX `fk_flights_airlines1_idx` (`airline_id` ASC) VISIBLE,
  INDEX `fk_flights_airports1_idx` (`departure_airport_id` ASC) VISIBLE,
  INDEX `fk_flights_airports2_idx` (`arrival_airport_id` ASC) VISIBLE,
  CONSTRAINT `fk_flights_airlines`
    FOREIGN KEY (`airline_id`)
    REFERENCES `FlightBooking`.`airlines` (`airline_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_flights_airports1`
    FOREIGN KEY (`departure_airport_id`)
    REFERENCES `FlightBooking`.`airports` (`airport_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_flights_airports2`
    FOREIGN KEY (`arrival_airport_id`)
    REFERENCES `FlightBooking`.`airports` (`airport_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FlightBooking`.`flight_classes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FlightBooking`.`flight_classes` (
  `class_id` TINYINT NOT NULL AUTO_INCREMENT,
  `class_title` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`class_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FlightBooking`.`tickets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FlightBooking`.`tickets` (
  `ticket_id` INT NOT NULL AUTO_INCREMENT,
  `ticket_number` VARCHAR(50) NOT NULL,
  `price` DECIMAL(5,2) NOT NULL,
  `confirmation_number` VARCHAR(50) NOT NULL,
  `passenger_id` INT NOT NULL,
  `flight_id` INT NOT NULL,
  `class_id` TINYINT NOT NULL,
  INDEX `fk_tickets_passengers_idx` (`passenger_id` ASC) VISIBLE,
  PRIMARY KEY (`ticket_id`),
  INDEX `fk_tickets_flights1_idx` (`flight_id` ASC) VISIBLE,
  INDEX `fk_tickets_flight_classes1_idx` (`class_id` ASC) VISIBLE,
  CONSTRAINT `fk_tickets_passengers`
    FOREIGN KEY (`passenger_id`)
    REFERENCES `FlightBooking`.`passengers` (`passenger_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tickets_flights`
    FOREIGN KEY (`flight_id`)
    REFERENCES `FlightBooking`.`flights` (`flight_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tickets_flight_classes`
    FOREIGN KEY (`class_id`)
    REFERENCES `FlightBooking`.`flight_classes` (`class_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
