SELECT * FROM Books;
SELECT * FROM Members;
SELECT * FROM BorrowedBooks;
SELECT * FROM ReservedBooks;
SELECT * FROM Authors;

SELECT b.accessionNo, title, GROUP_CONCAT(a.name SEPARATOR ',') AS Authors, ISBN, publisher, publicationYr
FROM Books b JOIN BorrowedBooks b2 ON b.accessionNo = b2.borrowedBookID 
JOIN Authors a ON b.accessionNo = a.accessionNo 
WHERE b2.returnedDate IS NULL GROUP BY b.accessionNo;

SELECT b.accessionNo, title, GROUP_CONCAT(a.name SEPARATOR ',') AS Authors, ISBN, publisher, publicationYr
FROM Books b JOIN Authors a ON b.accessionNo = a.accessionNo 
WHERE publisher REGEXP "([[:blank:][:punct:]]|^)joanne([[:blank:][:punct:]]|$)" GROUP BY b.accessionNo;

DELETE FROM BorrowedBooks WHERE borrowedUserID = "A1010J";

SELECT * FROM Books WHERE isBorrowed = TRUE;
DELETE FROM ReservedBooks WHERE reservedUserID = "A1000";

UPDATE Books SET isBorrowed = FALSE WHERE accessionNo IN ("A06");
INSERT INTO ReservedBooks VALUES("A06", "A1010J", '2022-3-9');

SELECT fineAmt FROM Members WHERE membershipID = "A26";
UPDATE Members SET fineAmt = 20 WHERE membershipID = "A26";
SELECT TIMESTAMPDIFF(DAY, dueDate, STR_TO_DATE("28/2/2022", '%d/%m/%Y')) FROM BorrowedBooks WHERE borrowedBookID = "A100" AND returnedDate IS NULL