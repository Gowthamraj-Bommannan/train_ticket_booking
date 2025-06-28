# ---------- USER MESSAGES ----------
class UserMessage:
    USER_NOT_FOUND = "User not found."
    USER_ALREADY_EXISTS = "User already exists."
    INVALID_CREDENTIALS = "Invalid username or password."
    USER_REGISTERED_SUCCESSFULLY = "User registered successfully."

# ---------- FIELD VALIDATION ----------
class FieldValidationMessage:
    USERNAME_REQUIRED = "Username is required."
    USERNAME_TOO_SHORT = "Username must be at least 3 characters long."
    EMAIL_REQUIRED = "Email is required."
    EMAIL_INVALID = "Invalid email format."
    MOBILE_REQUIRED = "Mobile number is required."
    MOBILE_INVALID = "Mobile number must be 10 digits and start with 6 to 9."
    PASSWORD_REQUIRED = "Password is required."
    PASSWORD_TOO_SHORT = "Password must be at least 8 characters long."
    PASSWORD_TOO_LONG = "Password must not exceed 16 characters."
    PASSWORD_LONG_OR_SHORT = 'Password must be 8 to 16 characters long.'
    FIRST_NAME_REQUIRED = "First name is required."

# ---------- UNIQUE FIELD CONFLICTS ----------
class AlreadyExistsMessage:
    EMAIL_ALREADY_EXISTS = "Email already exists."
    USERNAME_ALREADY_EXISTS = "Username already exists."
    MOBILE_ALREADY_EXISTS = "Mobile number already exists."

class GeneralMessage:
    INVALID_INPUT = "Invalid input."
    QUERY_MISSING = 'Search query parameter is required.'

# ---------STATION CONSTANTS-----------
class StationMessage:
    STATION_NOT_FOUND = "Station not found."
    STATION_ALREADY_EXISTS = "Station with this name or code already exists."
    STATION_CODE_REQUIRED = "Station code is required."
    STATION_NAME_REQUIRED = "Station name is required."
    STATION_NAME_TOO_SHORT = "Station name must be at least 3 characters."
    STATION_CODE_TOO_SHORT = "Station code must be at least 2 characters."
    STATION_SEARCH_QUERY_REQUIRED = "Search query for station is required."
    STATION_DELETED_SUCCESSFULLY = "Station deleted successfully."
    STATION_UPDATED = "Station Updated Successfully."

# ------------TRAIN CONSTANTS-------------
class TrainMessage:
    TRAIN_NOT_FOUND = "Train not found."
    TRAIN_ALREADY_EXISTS = "Train with this number or name already exists."
    TRAIN_NUMBER_REQUIRED = "Train number is required."
    TRAIN_NAME_REQUIRED = "Train name is required."
    TRAIN_NAME_TOO_SHORT = "Train name must be at least 3 characters long."
    TRAIN_NAME_INVALID = "Train name should contains alphabets only."
    TRAIN_NUMBER_INVALID = "Train number must be numeric."
    TRAIN_COMPARTMENT_COUNT_INVALID = "Compartment count must be a positive integer."
    TRAIN_SEAT_COUNT_INVALID = "Seats per compartment must be a positive integer."

# ----------- TRAIN STATION CONSTANTS ------------
class TrainStationMessage:
    TRAIN_STATION_NOT_FOUND = "Train station mapping not found."
    TRAIN_STATION_ALREADY_EXISTS = "This train already has this station in its route."
    TRAIN_STATION_ARRIVAL_REQUIRED = "Arrival time is required for train station."
    TRAIN_STATION_DEPARTURE_REQUIRED = "Departure time is required for train station."
    TRAIN_STATION_STOP_NUMBER_REQUIRED = "Stop number must be a positive integer."
    TRAIN_STATION_INVALID_STOP_NUMBER = "Invalid number of stops. Must be >= 1."
    TRAIN_STATION_DUPLICATE_STOP = "Duplicate stop number for this train."
    TRAIN_STATION_DEPARTURE_MUST_GREATER = "Departure time must be greater than Arrival time."



