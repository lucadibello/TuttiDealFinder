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
  id int PRIMARY KEY AUTO_INCREMENT,
  title VARCHAR(50) NOT NULL,
  price FLOAT,
  location_city VARCHAR(50) NOT NULL,
  location_cap int(4) NOT NULL,
  upload_date date NOT NULL,
  url TEXT NOT NULL
);

#TABELLA CHE TIENE IN MEMORIA QUALE OFFERTA È STATA TROVATA CON QUALE TRACKER
CREATE TABLE found(
  tracker_id INT NOT NULL,
  deal_id INT NOT NULL,
  PRIMARY KEY (tracker_id,deal_id),
  FOREIGN KEY (tracker_id) REFERENCES tracker(tracker_id),
  FOREIGN KEY (deal_id) REFERENCES deal(id)
);