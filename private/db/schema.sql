DROP TABLE IF EXISTS city_req;

CREATE TABLE city_req (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cidade VARCHAR(100),
    ip VARCHAR(50)
);

DROP TABLE IF EXISTS cities;

CREATE TABLE cities (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

INSERT INTO cities (name) VALUES ('Lisbon');
INSERT INTO cities (name) VALUES ('Madrid');
INSERT INTO cities (name) VALUES ('Paris');
INSERT INTO cities (name) VALUES ('Berlin');
INSERT INTO cities (name) VALUES ('Rome');
INSERT INTO cities (name) VALUES ('Vienna');
INSERT INTO cities (name) VALUES ('Prague');
INSERT INTO cities (name) VALUES ('Amsterdam');
INSERT INTO cities (name) VALUES ('Brussels');
INSERT INTO cities (name) VALUES ('Copenhagen');
INSERT INTO cities (name) VALUES ('Dublin');
INSERT INTO cities (name) VALUES ('Helsinki');
INSERT INTO cities (name) VALUES ('Oslo');
INSERT INTO cities (name) VALUES ('Stockholm');
INSERT INTO cities (name) VALUES ('Warsaw');
INSERT INTO cities (name) VALUES ('Budapest');
INSERT INTO cities (name) VALUES ('Athens');
INSERT INTO cities (name) VALUES ('Zurich');
INSERT INTO cities (name) VALUES ('Vienna');
INSERT INTO cities (name) VALUES ('Sofia');
INSERT INTO cities (name) VALUES ('Belgrade');
INSERT INTO cities (name) VALUES ('Bucharest');
INSERT INTO cities (name) VALUES ('Ljubljana');
INSERT INTO cities (name) VALUES ('Bratislava');
INSERT INTO cities (name) VALUES ('Tallinn');
INSERT INTO cities (name) VALUES ('Riga');
INSERT INTO cities (name) VALUES ('Vilnius');
INSERT INTO cities (name) VALUES ('Luxembourg');
INSERT INTO cities (name) VALUES ('Valletta');
INSERT INTO cities (name) VALUES ('Reykjavik');
INSERT INTO cities (name) VALUES ('Sarajevo');
INSERT INTO cities (name) VALUES ('Skopje');
INSERT INTO cities (name) VALUES ('Podgorica');
INSERT INTO cities (name) VALUES ('Tirana');
INSERT INTO cities (name) VALUES ('Andorra la Vella');
INSERT INTO cities (name) VALUES ('San Marino');
INSERT INTO cities (name) VALUES ('Monaco');
INSERT INTO cities (name) VALUES ('Vaduz');
INSERT INTO cities (name) VALUES ('Minsk');
INSERT INTO cities (name) VALUES ('Chisinau');
INSERT INTO cities (name) VALUES ('Yerevan');
INSERT INTO cities (name) VALUES ('Tbilisi');
INSERT INTO cities (name) VALUES ('Baku');
INSERT INTO cities (name) VALUES ('Astana');
INSERT INTO cities (name) VALUES ('Tashkent');
INSERT INTO cities (name) VALUES ('Ashgabat');
INSERT INTO cities (name) VALUES ('Dushanbe');
INSERT INTO cities (name) VALUES ('Bishkek');
INSERT INTO cities (name) VALUES ('Nicosia');
INSERT INTO cities (name) VALUES ('Ankara');
INSERT INTO cities (name) VALUES ('Jerusalem');
INSERT INTO cities (name) VALUES ('Beirut');
INSERT INTO cities (name) VALUES ('Damascus');
INSERT INTO cities (name) VALUES ('Amman');
INSERT INTO cities (name) VALUES ('Baghdad');
INSERT INTO cities (name) VALUES ('Tehran');
INSERT INTO cities (name) VALUES ('Kuwait City');
INSERT INTO cities (name) VALUES ('Riyadh');
INSERT INTO cities (name) VALUES ('Manama');
INSERT INTO cities (name) VALUES ('Doha');
INSERT INTO cities (name) VALUES ('Abu Dhabi');
INSERT INTO cities (name) VALUES ('Muscat');
INSERT INTO cities (name) VALUES ('Sanaa');
INSERT INTO cities (name) VALUES ('Kabul');
INSERT INTO cities (name) VALUES ('Islamabad');
INSERT INTO cities (name) VALUES ('New Delhi');
INSERT INTO cities (name) VALUES ('Kathmandu');
INSERT INTO cities (name) VALUES ('Thimphu');
INSERT INTO cities (name) VALUES ('Dhaka');
INSERT INTO cities (name) VALUES ('Colombo');
INSERT INTO cities (name) VALUES ('Male');
INSERT INTO cities (name) VALUES ('Beijing');
INSERT INTO cities (name) VALUES ('Tokyo');
INSERT INTO cities (name) VALUES ('Seoul');
INSERT INTO cities (name) VALUES ('Pyongyang');
INSERT INTO cities (name) VALUES ('Ulaanbaatar');
INSERT INTO cities (name) VALUES ('Hanoi');
INSERT INTO cities (name) VALUES ('Vientiane');
INSERT INTO cities (name) VALUES ('Bangkok');
INSERT INTO cities (name) VALUES ('Naypyidaw');
INSERT INTO cities (name) VALUES ('Phnom Penh');
INSERT INTO cities (name) VALUES ('Kuala Lumpur');
INSERT INTO cities (name) VALUES ('Singapore');
INSERT INTO cities (name) VALUES ('Jakarta');
INSERT INTO cities (name) VALUES ('Manila');
INSERT INTO cities (name) VALUES ('Bandar Seri Begawan');
INSERT INTO cities (name) VALUES ('Canberra');
INSERT INTO cities (name) VALUES ('Wellington');
INSERT INTO cities (name) VALUES ('Port Moresby');
INSERT INTO cities (name) VALUES ('Suva');
INSERT INTO cities (name) VALUES ('Honiara');
INSERT INTO cities (name) VALUES ('Port Vila');
INSERT INTO cities (name) VALUES ('Apia');
INSERT INTO cities (name) VALUES ('Nukuʻalofa');
INSERT INTO cities (name) VALUES ('Funafuti');
INSERT INTO cities (name) VALUES ('Palikir');
INSERT INTO cities (name) VALUES ('Majuro');
INSERT INTO cities (name) VALUES ('Yaren');