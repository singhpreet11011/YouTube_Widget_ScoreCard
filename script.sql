-- Create a database for the Scorecard Widget
CREATE DATABASE ScorecardWidget;

-- Use the newly created database
USE ScorecardWidget;

-- Create the Teams table
CREATE TABLE Teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
);

-- Create the Matches table
CREATE TABLE Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    team1_id INT,
    team2_id INT,
    match_date DATETIME NOT NULL,
    status ENUM('scheduled', 'in_progress', 'completed'),
    FOREIGN KEY (team1_id) REFERENCES Teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES Teams(team_id)
);

-- Create the Scores table
CREATE TABLE Scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    team1_score INT,
    team2_score INT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
);

-- Create the Score Updates table
CREATE TABLE Score_Updates (
    update_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT,
    score1 INT,
    score2 INT,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES Matches(match_id)
);

-- Insert dummy data into Teams table
INSERT INTO Teams (team_name) VALUES
('Team A'),
('Team B'),
('Team C'),
('Team D');

-- Insert dummy data into Matches table
INSERT INTO Matches (team1_id, team2_id, match_date, status) VALUES
(1, 2, '2024-10-05 14:00:00', 'scheduled'),
(3, 4, '2024-10-06 16:00:00', 'scheduled'),
(1, 3, '2024-10-07 18:00:00', 'in_progress');

-- Insert dummy data into Scores table
INSERT INTO Scores (match_id, team1_score, team2_score) VALUES
(1, 0, 0),
(2, 0, 0),
(3, 1, 2);

-- Insert dummy data into Score Updates table
INSERT INTO Score_Updates (match_id, score1, score2) VALUES
(1, 0, 0),
(1, 1, 0),
(3, 1, 1),
(3, 1, 2);
