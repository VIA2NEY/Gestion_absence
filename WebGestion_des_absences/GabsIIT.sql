CREATE TABLE IF NOT EXISTS Utilisateurs (
  `ID_Utilisateur` INT PRIMARY KEY,
  `loginname` VARCHAR(255),
  `password` VARCHAR(255),
  `Type` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Departement (
  `Id_dep` INT,
  `specialiter` VARCHAR(255),
  `niveau` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Etudiant (
  `ID_Utilisateur` INT,
  `Id_departement` INT,
  `matricule` INT,
  `nom` VARCHAR(55),
  `prenom` VARCHAR(255),
  `email` VARCHAR(55),
  `Date_De_Nainssance` DATE,
  `contact` INT,
  `photo` LONGBLOB,

  PRIMARY KEY (`matricule`),
  KEY `FK_Inheritance_1` (`ID_Utilisateur`),
  KEY `FK_Incrit` (`Id_departement`)

);

CREATE TABLE IF NOT EXISTS  Admin (
  `ID_Utilisateur` INT,
  `nom` VARCHAR(255),
  `prenom` VARCHAR(255),

  KEY `FK_Inheritance_2` (`ID_Utilisateur`)
);

CREATE TABLE IF NOT EXISTS  Enseignants (
  `ID_Utilisateur` INT,
  `Nom` VARCHAR(255),
  `Prenom` VARCHAR(255),
  `Tel` INT,
  `email` VARCHAR(255),
  `Photo` LONGBLOB,
  
  KEY `FK_Inheritance_3` (`ID_Utilisateur`)
);

CREATE TABLE IF NOT EXISTS Presence (
  `ID_Presence` INT,
  `ID_Etudiant` INT,
  `ID_Cour` INT,
  `dateheure` DATETIME,
  `Statut` VARCHAR(255),

  PRIMARY KEY (`ID_Presence`),
  KEY `FK_Confirme` (`ID_Etudiant`),
  KEY `FK_Concerne` (`ID_Cour`)
);

CREATE TABLE IF NOT EXISTS Cour (
  `idCour` INT,
  `dateheure` DATETIME,
  `type` VARCHAR(255),
  `ID_Module` INT,

  PRIMARY KEY (`idCour`),
  KEY `FK_Appartenir` (`ID_Module`)
);

CREATE TABLE IF NOT EXISTS Module (
  `id` INT PRIMARY KEY,
  `NomModule` VARCHAR(255),
  `nombre_Heur_du_modulee` INT
);

CREATE TABLE IF NOT EXISTS CodeQR (
  `ID_CodeQR` INT,
  `ID_Cour` INT,
  `Code` VARCHAR(255),

  PRIMARY KEY (`ID_CodeQR`),
  KEY `FK_Represente` (`ID_Cour`)
);

-- Insertion de données

-- Table Utilisateurs
INSERT INTO Utilisateurs (ID_Utilisateur, loginname, password, Type)
VALUES
  (1, 'john_doe', '123456', 'étudiant'),
  (2, 'emma_smith', 'password123', 'étudiant'),
  (3, 'michael_johnson', 'pass123', 'étudiant'),
  (4, 'Dia', 'Jean Fabrice', 'admin'),
  (5, 'julle_allani', 'All123', 'enseignant');

-- Table Etudiant
INSERT INTO Etudiant (ID_Utilisateur, Id_departement, matricule, nom, prenom, email, Date_De_Nainssance, contact, photo)
VALUES
  (1, 1, 1001, 'Doe', 'John', 'john.doe@example.com', '2000-01-01', 0747474776, NULL),
  (2, 3, 1002, 'Smith', 'Emma', 'emma.smith@example.com', '1999-12-31', 0758961324, NULL);

-- Table Admin
INSERT INTO Admin (ID_Utilisateur, nom, prenom)
VALUES
  (4, 'Dia', 'Jean Fabrice');

-- Table Enseignants
INSERT INTO Enseignants (ID_Utilisateur, Nom, Prenom, Tel, email, Photo)
VALUES
  (5, 'Allani', 'Julle', 0908070605, 'john.doe@example.com', NULL);

-- Table Departement
INSERT INTO Departement (Id_dep, specialiter, niveau)
VALUES
  (1, 'Informatique', 'Licence 3'),
  (2, 'Génie civil', 'Master 1'),
  (3, 'Administration des affaires', 'Licence 2');

-- Table Presence
INSERT INTO Presence (ID_Presence, ID_Etudiant, ID_Cour, dateheure, Statut)
VALUES
  (1, 2, 1, '2023-06-01 10:00:00', 'Présent'),
  (2, 2, 2, '2023-06-02 14:00:00', 'Absent'),
  (3, 3, 3, '2023-06-03 09:00:00', 'Présent');

-- Table Cour
INSERT INTO Cour (idCour, dateheure, type, ID_Module)
VALUES
  (1, '2023-06-01 10:00:00', 'Cours magistral', 1),
  (2, '2023-06-02 14:00:00', 'Travaux pratiques', 2),
  (3, '2023-06-03 09:00:00', 'Séminaire', 3);

-- Table Module
INSERT INTO Module (id, NomModule, nombre_Heur_du_modulee)
VALUES
  (1, 'Programmation avancée', 60),
  (2, 'Gestion de projet', 45),
  (3, 'Comptabilité', 30);

-- Table CodeQR
INSERT INTO CodeQR (ID_CodeQR, ID_Cour, Code)
VALUES
  (1, 1, 'ABC123'),
  (2, 2, 'DEF456'),
  (3, 3, 'GHI789');


ALTER TABLE `Etudiant`
  ADD CONSTRAINT `FK_Inheritance_1` FOREIGN KEY (`ID_Utilisateur`) REFERENCES `Utilisateurs` (`ID_Utilisateur`),
  ADD CONSTRAINT `FK_Incrit` FOREIGN KEY (`Id_departement`) REFERENCES `Departement` (`Id_dep`);

ALTER TABLE `Admin`
  ADD CONSTRAINT `FK_Inheritance_2` FOREIGN KEY (`ID_Utilisateur`) REFERENCES `user` (`ID_Utilisateur`);

ALTER TABLE `Enseignants`
  ADD CONSTRAINT `FK_Inheritance_3` FOREIGN KEY (`ID_Utilisateur`) REFERENCES `user` (`ID_Utilisateur`);

ALTER TABLE `Cour`
  ADD CONSTRAINT `FK_Appartenir` FOREIGN KEY (`ID_Module`) REFERENCES `Module` (`id`);

ALTER TABLE `Presence`
  ADD CONSTRAINT `FK_Confirme` FOREIGN KEY (`ID_Etudiant`) REFERENCES `Etudiant` (`matricule`),
  ADD CONSTRAINT `FK_Concerne` FOREIGN KEY (`ID_Cour`) REFERENCES `Cour` (`idCour`);

ALTER TABLE `CodeQR`
  ADD CONSTRAINT `FK_Represente` FOREIGN KEY (`ID_Cour`) REFERENCES `Cour` (`idCour`);

