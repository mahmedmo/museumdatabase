-- MUSEUM database creation
DROP DATABASE IF EXISTS MUSEUM;
CREATE DATABASE MUSEUM; 
USE MUSEUM;

-- Create INFORMATION_SCHEMA table
CREATE TABLE INFORMATION_SCHEMA (
    Table_name VARCHAR(100) PRIMARY KEY,
    Description TEXT,
    Tables_referenced TEXT,
    Referenced_by TEXT
);

-- Insert data into INFORMATION_SCHEMA
INSERT INTO INFORMATION_SCHEMA (Table_name, Description, Tables_referenced, Referenced_by)
VALUES
    ('ARTIST', 'Table to hold the name, date born and died, country of origin, epoch, main style, and description of an artist.', 'None', 'ART_OBJECT'),
    ('ART_OBJECT', "Table to hold the ID number, artist's name, year created, title, description, place of origin, and epoch of an art piece. References an ARTIST's Name as Artist_name.", 'ARTIST', 'PAINTING, SCULPTURE_STATUE, OTHER, PERMANENT_COLLECTION, BORROWED_COLLECTION, EXHIBITION_HAS'),
    ('PAINTING', "Table to hold the ID number, paint type, material drawn on, and style of a painting. References ART_OBJECT's Id_no as Art_id.", 'ART_OBJECT', 'None'),
    ('SCULPTURE_STATUE', "Table to hold the ID number, material made of, height, ,weight, and style of a sculpture or statue. References ART_OBJECT's Id_no as Art_id.", 'ART_OBJECT', 'None'),
    ('OTHER', "Table to hold the ID number, art piece type, and style of an art piece that isn't a painting, sculpture, or statue. References ART_OBJECT's Id_no as Art_id.", 'ART_OBJECT', 'None'),
    ('COLLECTION', "Table to hold the name, type, description, address, phone, and contact person of an art collection.", 'None', 'BORROWED_COLLECTION'),
    ('PERMANENT_COLLECTION', "Table to hold the ID number, date acquired, current status ('on display', 'on loan', or 'stored'), and cost of an art piece that belongs to this museum. References ART_OBJECT's Id_no as Art_id.", 'ART_OBJECT', 'None'),
    ('BORROWED_COLLECTION', "Table to hold the ID number, name of the collection it belongs to, date borrowed, and date returned of an art piece that is being borrowed and doesn't belong to this museum. References ART_OBJECT's Id_no as Art_id. References COLLECTION's Name as Collection_name.", 'ART_OBJECT, COLLECTION', 'None'), 
    ('EXHIBITION', "Table to hold the name, start date, and end date of an exhibition.", 'None', 'EXHIBITION_HAS'),
    ('EXHIBITION_HAS', "Table to hold an exhibition's name and the corresponding art piece's ID that the exhibition displays. References EXHIBITION's Name as Exhibition_name. References ART_OBJECT's Id_no as Art_id.", 'EXHIBITION, ART_OBJECT', 'None');


-- Create ARTIST table
CREATE TABLE ARTIST (
    Name VARCHAR(100) PRIMARY KEY,
    Date_born VARCHAR(100),
    Date_died VARCHAR(100),
    Country_of_origin VARCHAR(100),
    Epoch VARCHAR(100),
    Main_style VARCHAR(100),
    Description TEXT
);

-- Create ART_OBJECT table
CREATE TABLE ART_OBJECT (
    Id_no INT PRIMARY KEY AUTO_INCREMENT,
    Artist_name VARCHAR(100),
    Year INT,
    Title VARCHAR(255),
    Description TEXT,
    Origin VARCHAR(100),
    Epoch VARCHAR(100),
    FOREIGN KEY (Artist_name) REFERENCES ARTIST(Name)
);

-- Create PAINTING table
CREATE TABLE PAINTING (
    Art_id INT PRIMARY KEY,
    Paint_type VARCHAR(100),
    Drawn_on VARCHAR(100),
    Style VARCHAR(100),
    FOREIGN KEY (Art_id) REFERENCES ART_OBJECT(Id_no)
);

-- Create SCULPTURE_STATUE table
CREATE TABLE SCULPTURE_STATUE (
    Art_id INT PRIMARY KEY,
    Material VARCHAR(100),
    Height DECIMAL(8, 2),
    Weight DECIMAL(8, 2),
    Style VARCHAR(100),
    FOREIGN KEY (Art_id) REFERENCES ART_OBJECT(Id_no)
);

-- Create OTHER table
CREATE TABLE OTHER (
    Art_id INT PRIMARY KEY,
	Type varchar(100),
    Style varchar(100),
    FOREIGN KEY (Art_id) REFERENCES ART_OBJECT(Id_no)
);

-- Create COLLECTION table
CREATE TABLE COLLECTION (
    Name VARCHAR(100) PRIMARY KEY,
    Type VARCHAR(100),
    Description TEXT,
    Address VARCHAR(255),
    Phone VARCHAR(20),
    Contact_person VARCHAR(100)
);

-- Create PERMANENT_COLLECTION table
CREATE TABLE PERMANENT_COLLECTION (
	Art_id INT PRIMARY KEY,
    Date_acquired VARCHAR(100),
    Status ENUM('on display', 'on loan', 'stored'),
    Cost DECIMAL(10, 2),
    FOREIGN KEY (Art_id) REFERENCES ART_OBJECT(Id_no)
);

-- Create BORROWED_COLLECTION table
CREATE TABLE BORROWED_COLLECTION (
    Art_id INT PRIMARY KEY,
    Collection_name VARCHAR(100),
    Date_borrowed VARCHAR(100),
    Date_returned VARCHAR(100),
    FOREIGN KEY (Art_id) REFERENCES ART_OBJECT(Id_no),
    FOREIGN KEY (Collection_name) REFERENCES COLLECTION(Name)
);

-- Create EXHIBITION table
CREATE TABLE EXHIBITION (
    Name VARCHAR(100) PRIMARY KEY,
    Start_date VARCHAR(100),
    End_date VARCHAR(100)
);

-- Create EXHIBITION_HAS table
CREATE TABLE EXHIBITION_HAS (
    Exhibition_name VARCHAR(100),
    Art_id INT,
    FOREIGN KEY (Exhibition_name) REFERENCES EXHIBITION(Name),
    FOREIGN KEY (Art_id) REFERENCES ART_OBJECT(Id_no)
);

-- Insert data into ARTIST table
INSERT INTO ARTIST (Name, Date_born, Date_died, Country_of_origin, Epoch, Main_style, Description)
VALUES 
    ('Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown'),
    ('Hans Holbein the Younger', '1497', '1543', 'Germany', 'Holocene', 'Northern Renaissance', 'German-Swiss painter and printmaker'),
    ('Robert Peake the Elder', '1551', '1619', 'Britain', 'Holocene', 'Elizabethan', 'English painter'),
    ('Pablo Picasso', '1881', '1973', 'Spain', 'Holocene', 'Cubism', 'Spanish painter, sculptor, printmaker, ceramicist, and theatre designer'),
    ('Cornelius Norbertus Gijsbrechts', '1625', '1677', 'Flanders', 'Holocene', 'Baroque', 'Flemish painter'),
    ('Juan Gris', '1887', '1927', 'Spain', 'Holocene', 'Cubism', 'Spanish painter'),
    ('Leonardo da Vinci', '1452', '1519', 'Italy', 'Holocene', 'High Renaissance', 'An Italian painter, draughtsman, engineer, scientist, theorist, sculptor, and architect.'),
    ('Vincent van Gogh', '1853', '1890', 'Netherlands', 'Holocene', 'Impressionism', 'A Dutch painter who is among the most famous and influential figures in the history of Western art.');

-- Insert data into ART_OBJECT table
INSERT INTO ART_OBJECT (Artist_name, Year, Title, Description, Origin, Epoch)
VALUES 
    ('Hans Holbein the Younger', 1533, 'Portrait of a Man in Royal Livery', 'The man in this portrait wears English royal livery, a uniform consisting of a red cap and coat embroidered with Henry VIII’s initials (HR), which identifies him as an artisan or attendant in the royal household.', 'Britain', 'Holocene'),
    ('Robert Peake the Elder', 1603, 'Henry Frederick (1594–1612), Prince of Wales, with Sir John Harington (1592–1614), in the Hunting Field', "This royal hunting portrait was modeled after an earlier type established by Netherlandish and German artists.", 'Britain', 'Holocene'),
    ('Unknown', 1544, 'Field Armor of King Henry VIII of England', 'This impressive armor was made for Henry VIII (reigned 1509–47) toward the end of his life, when he was overweight and crippled with gout.', 'Italy', 'Holocene'),
    ('Hans Holbein the Younger', 1527, 'Armor Garniture, Probably of King Henry VIII of England', 'This is the earliest dated armor from the royal workshops at Greenwich, which were established in 1515 by Henry VIII (reigned 1509–47) to produce armors for himself and his court.', 'Greenwich', 'Holocene'),
    ('Unknown', 1580, 'Jerkin', "This doublet is a rare example of sixteenth-century male clothing, very little of which has survived.", 'Europe', 'Holocene'),
    ('Unknown', 1600, 'Pair of gloves', "The weeping eye. green parrot, and shimmering pansies adorning this pair of gloves indicate they were originally intended as a love token.", 'Britain', 'Holocene'),
    ('Pablo Picasso', 1912, 'Still Life with Chair Caning', "Picasso made the first Cubist collage by pasting a piece of oilcloth (a waterproof fabric used for tablecloths) onto an oval canvas depicting café fare and a newspaper.", 'Spain', 'Holocene'),
    ('Cornelius Norbertus Gijsbrechts', 1665, 'The Attributes of the Painter', "A studio wall displaying the tools of the artist’s trade was the ultimate self-reflexive subject of trompe l’oeil, a means of representing representation.", 'Flanders', 'Holocene'),
    ('Juan Gris', 1913, 'Violin and Engraving', "A picture-within-a-picture attached to a board or wall was a favorite motif of trompe l’oeil artists.", 'Spain', 'Holocene'),
    ('Pablo Picasso', 1914, 'Still Life', 'Still Life may appear to be casually concocted from scrap materials but is rife with playful allusions to favorite motifs of trompe l’oeil painters: a table that thrusts forward, a precariously balanced knife, a cut-crystal glass half full of wine, and the leftovers of a meal.', 'Spain', 'Holocene'),
    ('Pablo Picasso', 1914, 'Glass and Die', 'While Picasso never sculpted in the esteemed material of marble, he copied its veining in paintings, papiers collés, and this deliberately rough-hewn construction.', 'Spain', 'Holocene'),
    ('Pablo Picasso', 1914, 'The Absinthe Glass', 'In an age when sculpture usually meant allegorical figures and portrait busts, Picasso’s life-size rendering of a glass of alcohol was shocking for its banality.', 'Spain', 'Holocene'),
    ('Unknown', 1867, 'Face Jug', "Face jugs were made by African American slaves and freedmen working in potteries in the Edgefield District of South Carolina, an area of significant stoneware production in the nineteenth century.", 'USA', 'Holocene'),
    ('Unknown', 1846, 'Pitcher', "A pitcher.", 'USA', 'Holocene'),
    ('Unknown', 2021, 'Large Jug', 'A large jug with a handle.', 'USA', 'Holocene'),
    ('Unknown', 1500, 'Bowl', 'A bowl with an indented pattern all around it.', 'USA', 'Holocene'),
    ('Unknown', 1840, 'Reconstructed Jug', 'A reconstructed jug with missing pieces.', 'USA', 'Holocene'),
    ('Unknown', 1858, 'Storage Jar', 'A jar for storage.', 'USA', 'Holocene'),
    ('Leonardo da Vinci', 1503, 'Mona Lisa', "The Mona Lisa or Monna Lisa is a half-length portrait painting by Italian artist Leonardo da Vinci.", 'Italy', 'Holocene'),
    ('Leonardo da Vinci', 1483, 'The Virgin of the Rocks (Paris)', "The Virgin of the Rocks is the name of two paintings by the Italian Renaissance artist Leonardo da Vinci, of the same subject, with a composition which is identical except for several significant details.", 'Italy', 'Holocene'),
    ('Leonardo da Vinci', 1513, 'Saint John the Baptist', 'Saint John the Baptist is a High Renaissance oil painting on walnut wood by Leonardo da Vinci.', 'Italy', 'Holocene'),
    ('Vincent van Gogh', 1889, 'The Starry Night', "The Starry Night is an oil-on-canvas painting by the Dutch painter Vincent van Gogh.", 'France', 'Holocene'),
    ('Vincent van Gogh', 1889, 'Van Gogh self-portrait', "Dutch painter Vincent van Gogh painted this self-portrait, which may have been his last self-portait.", 'France', 'Holocene'),
    ('Unknown', -1323, 'Mask of Tutankhamun', 'A gold funerary mask of the 18th-dynasty ancient Egyptian pharaoh Tutankhamun (King Tut).', 'Egypt', 'Holocene');

-- Insert data into PAINTING table
INSERT INTO PAINTING (Art_id, Paint_type, Drawn_on, Style)
VALUES 
    (1, 'Oil, gold', 'Parchment', 'Northern Renaissance'),
    (2, 'Oil', 'Canvas', 'Elizabethan'),
    (7, 'Oil, printed oilcloth', 'Canvas', 'Cubist'),
    (8, 'Oil', 'Canvas', 'Baroque'),
    (9, 'Oil, sand', 'Canvas', 'Cubist'),
    (19, 'Oil', 'Poplar', 'High Renaissance'),
    (20, 'Oil', 'Panel', 'High Renaissance'),
    (21, 'Oil', 'Walnut wood', 'High Renaissance'),
    (22, 'Oil', 'Canvas', 'Post-Impressionalism'),
    (23, 'Oil', 'Canvas', 'Post-Impressionalism');

-- Insert data into SCULPTURE_STATUE table
INSERT INTO SCULPTURE_STATUE (Art_id, Material, Height, Weight, Style)
VALUES 
    (3, 'Steel, gold, textile, leather', 1.842, 22.91, 'Italian'),
    (4, 'Steel, gold, leather, copper alloys', 1.854, 28.45, 'British'),
    (10, 'Wood, fabric', 0.254, 4.1, 'Cubist'),
    (11, 'Wood', 0.235, 3.8, 'Cubist'),
    (12, 'Bronze, tin absinthe', 0.225, 10.2, 'Cubist');

-- Insert data into OTHER table
INSERT INTO OTHER (Art_id, Type, Style)
VALUES 
    (5, 'Costume', 'Western European'),
    (6, 'Textiles', 'British'),
    (13, 'Pottery', 'American'),
    (14, 'Pottery', 'American'),
    (15, 'Pottery', 'American'),
    (16, 'Pottery', 'First Nations'),
    (17, 'Pottery', 'American'),
    (18, 'Pottery', 'American'),
    (24, 'Funerary Mask', 'Egyptian');

-- Insert data into COLLECTION table
INSERT INTO COLLECTION (Name, Type, Description, Address, Phone, Contact_person)
VALUES 
    ('The Met', 'Museum', 'The Metropolitan Museum of Art presents over 5,000 years of art from around the world for everyone to experience and enjoy.', '1000 5th Ave, New York, NY 10028, USA', '212-535-7710', 'Met Person'),
    ('Louvre Museum', 'Museum', "Louvre Museum is the world's most-visited art museum, with a collection that spans work from ancient civilizations to the mid-19th century.", '75001 Paris, France', '+33 1 40 20 53 17', 'Louvre Person');

-- Insert data into PERMANENT_COLLECTION table
INSERT INTO PERMANENT_COLLECTION (Art_id, Date_acquired, Status, Cost)
VALUES 
    (22, '2000-01-01', 'on display', 1000000.00),
    (23, '2009-09-09', 'on loan', 7150000.00),
    (24, '1981-09-23', 'stored', 9999999.99);

-- Insert data into BORROWED_COLLECTION table
INSERT INTO BORROWED_COLLECTION (Art_id, Collection_name, Date_borrowed, Date_returned)
VALUES 
    (1, 'The Met', '2022-01-01', '2023-02-02'),
    (2, 'The Met', '2022-01-01', '2023-02-02'),
    (3, 'The Met', '2022-01-01', '2023-02-02'),
    (4, 'The Met', '2022-01-01', '2023-02-02'),
    (5, 'The Met', '2022-01-01', '2023-02-02'),
    (6, 'The Met', '2022-01-01', '2023-02-02'),
    (7, 'The Met', '2022-01-01', '2023-02-02'),
    (8, 'The Met', '2022-01-01', '2023-02-02'),
    (9, 'The Met', '2022-01-01', '2023-02-02'),
    (10, 'The Met', '2022-01-01', '2023-02-02'),
    (11, 'The Met', '2022-01-01', '2023-02-02'),
    (12, 'The Met', '2022-01-01', '2023-02-02'),
    (13, 'The Met', '2022-01-01', '2023-02-02'),
    (14, 'The Met', '2022-01-01', '2023-02-02'),
    (15, 'The Met', '2022-01-01', '2023-02-02'),
    (16, 'The Met', '2022-01-01', '2023-02-02'),
    (17, 'The Met', '2022-01-01', '2023-02-02'),
    (18, 'The Met', '2022-01-01', '2023-02-02'),
    (19, 'Louvre Museum', '2023-03-04', '2023-06-07'),
    (20, 'Louvre Museum', '2023-03-04', '2023-06-07'),
    (21, 'Louvre Museum', '2023-03-04', '2023-06-07');

-- Insert data into EXHIBITION table
INSERT INTO EXHIBITION (Name, Start_date, End_date)
VALUES 
    ("The Tudors", '2022-10-10', '2023-01-08'),
    ("Cubism and the Trompe l'Oeil Tradition", '2022-10-20', '2023-01-22'),
    ("Hear Me Now", '2022-09-09', '2023-02-05'),
    ("Louvre Exhibition", '2023-04-04', '2024-05-05'),
    ("Local Exhibition", '2023-01-01', '2024-01-01');

-- Insert data into EXHIBITION_HAS table
INSERT INTO EXHIBITION_HAS (Exhibition_name, Art_id)
VALUES 
    ("The Tudors", 1),
    ("The Tudors", 2),
    ("The Tudors", 3),
    ("The Tudors", 4),
    ("The Tudors", 5),
    ("The Tudors", 6),
    ("Cubism and the Trompe l'Oeil Tradition", 7),
    ("Cubism and the Trompe l'Oeil Tradition", 8),
    ("Cubism and the Trompe l'Oeil Tradition", 9),
    ("Cubism and the Trompe l'Oeil Tradition", 10),
    ("Cubism and the Trompe l'Oeil Tradition", 11),
    ("Cubism and the Trompe l'Oeil Tradition", 12),
    ("Hear Me Now", 13),
    ("Hear Me Now", 14),
    ("Hear Me Now", 15),
    ("Hear Me Now", 16),
    ("Hear Me Now", 17),
    ("Hear Me Now", 18),
    ("Louvre Exhibition", 19),
    ("Louvre Exhibition", 20),
    ("Louvre Exhibition", 21),
    ("Local Exhibition", 22),
    ("Local Exhibition", 23),
    ("Local Exhibition", 24);

-- ROLE creation 
DROP ROLE IF EXISTS db_admin@localhost, data_access@localhost, read_access@localhost, blocked@localhost;
CREATE ROLE db_admin@localhost, data_access@localhost, read_access@localhost,blocked@localhost;
GRANT ALL PRIVILEGES ON *.* TO db_admin@localhost WITH GRANT OPTION;
GRANT SELECT, INSERT, UPDATE, DELETE ON MUSEUM.* TO data_access@localhost;
GRANT Select ON MUSEUM.* TO read_access@localhost;

-- Default USER creation
DROP USER IF EXISTS administrator@localhost;
DROP USER IF EXISTS data_entry@localhost;
DROP USER IF EXISTS guest@localhost;
CREATE USER administrator@localhost IDENTIFIED WITH mysql_native_password BY 'password';
CREATE USER data_entry@localhost IDENTIFIED WITH mysql_native_password BY 'password';
CREATE USER guest@localhost;
GRANT db_admin@localhost TO administrator@localhost;
GRANT data_access@localhost TO data_entry@localhost;
GRANT read_access@localhost TO guest@localhost;
SET DEFAULT ROLE ALL TO administrator@localhost;
SET DEFAULT ROLE ALL TO data_entry@localhost;
SET DEFAULT ROLE ALL TO guest@localhost;

-- ENDOFFILE


