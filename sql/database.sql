CREATE DATABASE tuttidealfinder;
use tuttidealfinder;

#TABELLA CHE TIENE IN MEMORIA QUALI UTENTI UTILIZZANO IL BOT
CREATE TABLE user(
  chat_id INT PRIMARY KEY,
  notify_flag BIT DEFAULT 1 NOT NULL
);

#TABELLA CHE TIENE IN MEMORIA QUALI SONO I TRACKER PRESENTI
CREATE TABLE tracker(
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  query_url TEXT NOT NULL,
  name VARCHAR(50) NOT NULL
);

#TABELLA CHE TIENE IN MEMORIA TUTTE LE OFFERTE TROVATE
CREATE TABLE deal(
  id int AUTO_INCREMENT,
  user_id int NOT NULL,
  title VARCHAR(50) NOT NULL,
  price varchar(20) NOT NULL,
  location_city VARCHAR(50) NOT NULL,
  location_cap int(4) NOT NULL,
  upload_date VARCHAR(50) NOT NULL,
  url TEXT NOT NULL,
<<<<<<< HEAD
  PRIMARY KEY (id,user_id)
=======
  PRIMARY KEY (id,tracker_id),
  FOREIGN KEY (tracker_id) REFERENCES tracker(tracker_id)
  ON DELETE CASCADE
>>>>>>> 9356d9cd85718b52effa301f9ec0666cf9f0eb28
);