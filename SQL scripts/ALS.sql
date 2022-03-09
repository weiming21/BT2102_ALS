DROP TABLE IF EXISTS `Members`;
    
CREATE TABLE `Members` (
	`membershipID` VARCHAR(25) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    `faculty` VARCHAR(25) NOT NULL,
    `phoneNo` INT NOT NULL,
    `email` VARCHAR(50),
    `fineAmt` INT DEFAULT 0,
    `paymentDate` DATE DEFAULT NULL,
    PRIMARY KEY (`membershipID`));
    
DROP TABLE IF EXISTS `Books`;

CREATE TABLE `Books` (
	`accessionNo` VARCHAR(10) NOT NULL,
	`ISBN` VARCHAR(13) NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `publisher` VARCHAR(50) NOT NULL,
    `publicationYr` INT NOT NULL,
    `isBorrowed` BOOL DEFAULT FALSE,
	`isReserved` BOOL DEFAULT FALSE,
    PRIMARY KEY (`accessionNo`));
    
DROP TABLE IF EXISTS `Authors`; 

CREATE TABLE `Authors`(
	`accessionNo` VARCHAR(10) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    FOREIGN KEY (`accessionNo`) REFERENCES `Books` (`accessionNo`) ON DELETE CASCADE
    ON UPDATE CASCADE);
    
DROP TABLE IF EXISTS `BorrowedBooks`;

CREATE TABLE `BorrowedBooks`(
  `borrowedBookID` VARCHAR(10) NOT NULL,
  `borrowedUserID` VARCHAR(25) NOT NULL,
  `borrowedDate` DATE NOT NULL,
  `dueDate` DATE NOT NULL,
  `returnedDate` DATE DEFAULT NULL,
  PRIMARY KEY (`borrowedBookID`, `borrowedUserID`, `borrowedDate`),
  FOREIGN KEY (`borrowedUserID`) REFERENCES `Members`(`membershipID`) ON DELETE CASCADE 
  ON UPDATE CASCADE,
  FOREIGN KEY (`borrowedBookID`) REFERENCES `Books` (`accessionNo`) ON DELETE CASCADE
  ON UPDATE CASCADE);

DROP TABLE IF EXISTS `ReservedBooks`;
  
CREATE TABLE `ReservedBooks`(
  `reservedBookID` VARCHAR(10) NOT NULL,
  `reservedUserID` VARCHAR(25) NOT NULL,
  `reservedDate` DATE NOT NULL,
  PRIMARY KEY (`reservedBookID`, `reservedUserID`),
  FOREIGN KEY (`reservedBookID`) REFERENCES `Books` (`accessionNo`) ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (`reservedUserID`) REFERENCES `Members` (`membershipID`) ON DELETE CASCADE
  ON UPDATE CASCADE);
    
