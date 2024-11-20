CREATE DATABASE airport_reservation;
USE airport_reservation;

CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    passport_id VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    contact_number VARCHAR(15),
    name VARCHAR(100) NOT NULL
);

CREATE TABLE BookingAirline (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    class VARCHAR(20),
    trip_type ENUM('one-way', 'round-trip'),
    from_destn VARCHAR(50),
    to_destn VARCHAR(50),
    departure_date DATE,
    arrival_date DATE,
    number_of_passengers INT
);

CREATE TABLE Reserve (
    passport_id VARCHAR(20),
    booking_id INT,
    FOREIGN KEY (passport_id) REFERENCES User(passport_id),
    FOREIGN KEY (booking_id) REFERENCES BookingAirline(booking_id),
    PRIMARY KEY (passport_id, booking_id)
);

CREATE TABLE Ticket (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    price DECIMAL(10, 2),
    seat_number VARCHAR(10),
    booking_date DATE,
    booking_id INT,
    FOREIGN KEY (booking_id) REFERENCES BookingAirline(booking_id)
);

CREATE TABLE Generates (
    booking_id INT,
    reservation_id INT,
    time TIME,
    date DATE,
    PRIMARY KEY (booking_id, reservation_id),
    FOREIGN KEY (booking_id) REFERENCES BookingAirline(booking_id),
    FOREIGN KEY (reservation_id) REFERENCES Ticket(reservation_id)
);

CREATE TABLE PaymentGateway (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    mode_of_payment ENUM('credit', 'debit', 'paypal', 'netbanking')
);

CREATE TABLE Pay (
    reservation_id INT,
    payment_id INT,
    PRIMARY KEY (reservation_id, payment_id),
    FOREIGN KEY (reservation_id) REFERENCES Ticket(reservation_id),
    FOREIGN KEY (payment_id) REFERENCES PaymentGateway(payment_id)
);

CREATE TABLE BookingFlight (
    flight_id INT PRIMARY KEY AUTO_INCREMENT,
    depart_time TIME,
    arrival_time TIME,
    luggage BOOLEAN,
    meals BOOLEAN,
    airline_name VARCHAR(50),
    price DECIMAL(10, 2),
    from_destn VARCHAR(50),
    to_destn VARCHAR(50),
    departure_date DATE
);

-- Insert dummy flight data into the BookingFlight table
INSERT INTO BookingFlight (depart_time, arrival_time, luggage, meals, airline_name, price, from_destn, to_destn, departure_date)
VALUES
    ("08:00:00", "10:00:00", TRUE, TRUE, "Air India", 5000.00, "New York", "London", "2024-12-01"),
    ("12:00:00", "14:00:00", TRUE, FALSE, "Indigo", 3000.00, "New York", "London", "2024-12-01"),
    ("16:00:00", "18:00:00", FALSE, TRUE, "SpiceJet", 4500.00, "New York", "Delhi", "2024-12-02"),
    ("20:00:00", "22:00:00", TRUE, TRUE, "Vistara", 6000.00, "London", "Paris", "2024-12-01"),
    ("10:00:00", "12:00:00", TRUE, FALSE, "Lufthansa", 7000.00, "Delhi", "Mumbai", "2024-12-01");


CREATE TABLE Search (
    booking_id INT,
    flight_id INT,
    PRIMARY KEY (booking_id, flight_id),
    FOREIGN KEY (booking_id) REFERENCES BookingAirline(booking_id),
    FOREIGN KEY (flight_id) REFERENCES BookingFlight(flight_id)
);

CREATE TABLE Airport (
    airport_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    location VARCHAR(100)
);

SHOW TABLES;
SELECT * FROM User;
SELECT * FROM BookingFlight;
SELECT * FROM BookingAirline;
DESCRIBE BookingAirline;
ALTER TABLE BookingAirline ADD passport_id INT;
CREATE TABLE UserBookings (
    user_id VARCHAR(50),
    booking_id INT,
    FOREIGN KEY (user_id) REFERENCES User(passport_id),
    FOREIGN KEY (booking_id) REFERENCES BookingAirline(booking_id)
);


