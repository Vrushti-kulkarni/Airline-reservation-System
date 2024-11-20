import streamlit as st
import pymysql

# Database connection
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="MySQL@21331",
        database="airport_reservation",
        cursorclass=pymysql.cursors.DictCursor
    )

# Add a new user
def add_user(passport_id, email, dob, contact_number, name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            INSERT INTO User (passport_id, email, dob, contact_number, name)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (passport_id, email, dob, contact_number, name))
        connection.commit()
    finally:
        connection.close()

# Verify user credentials
def verify_user(passport_id, name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM User WHERE passport_id = %s AND name = %s
            """
            cursor.execute(query, (passport_id, name))
            result = cursor.fetchone()
            return result is not None
    finally:
        connection.close()

# Search for flights
def search_flights(from_destn, to_destn, departure_date):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT * FROM BookingFlight
            WHERE from_destn = %s AND to_destn = %s AND departure_date = %s
            """
            cursor.execute(query, (from_destn, to_destn, departure_date))
            flights = cursor.fetchall()
            return flights
    finally:
        connection.close()

# Generate ticket and store booking info in BookingAirline
def generate_ticket(flight_id, passport_id, trip_type, flight_class, num_passengers, from_destn, to_destn, departure_date, arrival_date):
    connection = get_db_connection()
    try:
        # Insert the booking into BookingAirline
        with connection.cursor() as cursor:
            query = """
            INSERT INTO BookingAirline (class, trip_type, from_destn, to_destn, departure_date, arrival_date, number_of_passengers)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (flight_class, trip_type, from_destn, to_destn, departure_date, arrival_date, num_passengers))
        connection.commit()

        # Get the booking_id of the newly inserted booking
        booking_id = cursor.lastrowid

        # Insert the user-booking association into UserBookings
        with connection.cursor() as cursor:
            query = """
            INSERT INTO UserBookings (user_id, booking_id)
            VALUES (%s, %s)
            """
            cursor.execute(query, (passport_id, booking_id))
        connection.commit()
    finally:
        connection.close()

# Fetch and display user's tickets
def fetch_user_tickets(passport_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT ba.* FROM BookingAirline ba
            JOIN UserBookings ub ON ba.booking_id = ub.booking_id
            WHERE ub.user_id = %s
            """
            cursor.execute(query, (passport_id,))
            tickets = cursor.fetchall()
            return tickets
    finally:
        connection.close()

# Streamlit App
st.title("Airline Booking System")

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Add User", "Search Flights", "My Tickets", "Reservation"])

# If "Reserve" is clicked for a flight, show "Reservation" section
if 'selected_flight' in st.session_state:
    menu = "Reservation"  # Automatically switch to "Reservation" after flight selection

if menu == "Home":
    st.subheader("Welcome to the Airline Booking System!")
    st.write("Use the sidebar to navigate through the system.")

elif menu == "Add User":
    st.subheader("Add a New User")
    passport_id = st.text_input("Passport ID")
    email = st.text_input("Email")
    dob = st.date_input("Date of Birth")
    contact_number = st.text_input("Contact Number")
    name = st.text_input("Name")
    
    if st.button("Add User"):
        add_user(passport_id, email, dob, contact_number, name)
        st.success("User added successfully!")

elif menu == "Search Flights":
    st.subheader("Search Flights")
    
    # Check if user is logged in using session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # User login
    if not st.session_state.logged_in:
        passport_id = st.text_input("Passport ID")
        name = st.text_input("Name")
    
        if st.button("Login"):
            if verify_user(passport_id, name):
                st.success("Login successful!")
                st.session_state.logged_in = True  # Set user as logged in
                st.session_state.passport_id = passport_id  # Store passport_id in session
            else:
                st.error("Invalid credentials. Please create an account first.")
    else:
        # Search flight details
        from_destn = st.text_input("From (Destination)")
        to_destn = st.text_input("To (Destination)")
        departure_date = st.date_input("Departure Date")

        if st.button("Search"):
            flights = search_flights(from_destn, to_destn, departure_date)
            if flights:
                st.write("Available Flights:")
                for flight in flights:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"**Flight ID:** {flight['flight_id']}")
                        st.markdown(f"**Airline:** {flight['airline_name']}")
                        st.markdown(f"**Departure:** {flight['depart_time']}")
                        st.markdown(f"**Arrival:** {flight['arrival_time']}")
                        st.markdown(f"**Price:** ${flight['price']}")
                        st.markdown(f"**Luggage Included:** {'Yes' if flight['luggage'] else 'No'}")
                        st.markdown(f"**Meals Included:** {'Yes' if flight['meals'] else 'No'}")
                    with col2:
                        st.markdown(f"**From:** {flight['from_destn']}")
                        st.markdown(f"**To:** {flight['to_destn']}")
                    with col3:
                        if st.button(f"Reserve {flight['flight_id']}"):
                            st.session_state.selected_flight = flight  # Store selected flight details
                            st.session_state.trip_details = {} 
                            # Set the menu to "Reservation"
                            st.session_state.menu = "Reservation"
                            st.experimental_rerun()  # Refresh to show booking form

elif menu == "Reservation":
  # Reservation page shown after clicking "Reserve"
  if 'selected_flight' in st.session_state:
    st.write("RUNNING.")
    selected_flight = st.session_state.selected_flight
    st.subheader(f"Reserve Your Flight: {selected_flight['airline_name']} ({selected_flight['flight_id']})")

    # Additional info for reservation
    trip_type = st.radio("Trip Type", ["One-way", "Round-trip"])
    flight_class = st.selectbox("Class", ["Economy", "Business", "First"])
    num_passengers = st.number_input("Number of Passengers", min_value=1, value=1)

    # Get arrival date (for round-trip, assume same return date)
    if trip_type == "Round-trip":
      arrival_date = st.date_input("Return Date")
    else:
      arrival_date = selected_flight['departure_date']  # Use flight's departure date for one-way

    # Confirm reservation
    if st.button("Confirm Reservation"):
      generate_ticket(
          selected_flight['flight_id'],
          st.session_state.passport_id,  # Assume passport_id is stored in session
          trip_type,
          flight_class,
          num_passengers,
          selected_flight['from_destn'],
          selected_flight['to_destn'],
          selected_flight['departure_date'],
          arrival_date
      )
      st.success("Ticket generated and reserved successfully!")
      # Clear session state after successful reservation
      st.session_state.selected_flight = None
      st.session_state.trip_details = None  


elif menu == "My Tickets":
    st.subheader("My Tickets")
    if 'passport_id' in st.session_state:
        tickets = fetch_user_tickets(st.session_state.passport_id)
        if tickets:
            for ticket in tickets:
                st.write(f"Flight: {ticket['from_destn']} to {ticket['to_destn']}")
                st.write(f"Class: {ticket['class']}")
                st.write(f"Departure: {ticket['departure_date']}")
                st.write(f"Arrival: {ticket['arrival_date']}")
                st.write(f"Passengers: {ticket['number_of_passengers']}")
        else:
            st.write("You have no tickets.")
    else:
        st.write("Please log in first.")
