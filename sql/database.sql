CREATE DATABASE tuttidealfinder;
use tuttidealfinder;

#TABELLA CHE TIENE IN MEMORIA QUALI UTENTI UTILIZZANO IL BOT
CREATE TABLE user(
  chat_id INT PRIMARY KEY,
  notify_flag BIT DEFAULT 1 NOT NULL
);

#TABELLA CHE TIENE IN MEMORIA QUALI SONO I TRACKER PRESENTI
CREATE TABLE tracker(
  tracker_id INT PRIMARY KEY AUTO_INCREMENT,
  query_url TEXT NOT NULL,
  name VARCHAR(50) NOT NULL
);

#TABELLA PONTE CHE PERMETTE DI CAPIRE QUALE UTENTE POSSIEDE QUALI TRACKER
CREATE TABLE tracking_list(
  user_id int NOT NULL,
  tracker_id int NOT NULL,
  PRIMARY KEY (user_id,tracker_id),
  FOREIGN KEY (user_id) REFERENCES user(chat_id),
  FOREIGN KEY (tracker_id) REFERENCES tracker(tracker_id)
);

#TABELLA CHE TIENE IN MEMORIA TUTTE LE OFFERTE TROVATE
CREATE TABLE deal(
  id int AUTO_INCREMENT,
  tracker_id int NOT NULL,
  title VARCHAR(50) NOT NULL,
  price varchar(20) NOT NULL,
  location_city VARCHAR(50) NOT NULL,
  location_cap int(4) NOT NULL,
  upload_date VARCHAR(50) NOT NULL,
  url TEXT NOT NULL,
  PRIMARY KEY (id,tracker_id),
  FOREIGN KEY (tracker_id) REFERENCES tracker(tracker_id)
  ON DELETE CASCADE
);