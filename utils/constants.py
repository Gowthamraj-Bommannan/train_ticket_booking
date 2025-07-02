# ---------- USER MESSAGES ----------
class UserMessage:
    USER_NOT_FOUND = "User not found."
    USER_ALREADY_EXISTS = "User already exists."
    INVALID_CREDENTIALS = "Invalid username or password."
    USER_REGISTERED_SUCCESSFULLY = "User registered successfully."
    USER_ROLE_NOT_FOUND = "Role PASSENGER is not defined in the system."
    USER_INACTIVE = "User account is disabled."
    USERNAME_AND_PASSWORD_REQUIRED = "Both username and password are required."
    USER_LOGIN_SUCCESSFUL = "Login in successful."

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
    STATION_WITH_CODE_NOT_EXISTS = "Station with code '{station_code}' does not exist."
    STATION_WITH_ID_NOT_EXISTS = "Station with ID {station_id} does not exist or is inactive."

# ------------TRAIN CONSTANTS-------------
class TrainMessage:
    TRAIN_NOT_FOUND = "Train not found."
    TRAIN_ALREADY_EXISTS = "Train with this name already exists."
    TRAIN_NUMBER_REQUIRED = "Train number is required."
    TRAIN_NAME_REQUIRED = "Train name is required."
    TRAIN_NAME_TOO_SHORT = "Train name must be at least 3 characters long."
    TRAIN_NAME_INVALID = "Train name should contains alphabets only."
    TRAIN_NUMBER_INVALID = "Train number must be numeric."
    TRAIN_COMPARTMENT_COUNT_INVALID = "Compartment count must be a positive integer."
    TRAIN_SEAT_COUNT_INVALID = "Seats per compartment must be a positive integer."
    TRAIN_WITH_NUMBER_NOT_EXIST = "Train with number '{train_number}' does not exist."
    TRAIN_QUERY_MISSING = 'train_number query parameter is required.'

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
    TRAIN_ROUTE_ALREADY_DEFINED = "Train route already defined. Clear it before adding."
    TRAIN_STOP_ALREADY_EXISTS = "Stop station already exists for this train."
    ALL_FIELDS_ARE_REQUIRED = "All fields (train, station, arrival_time, departure_time, insert_after_station_code) are required."
    STATION_EXIST_IN_ROUTE = "This station is already in the route."
    TRAIN_STOP_ADDED = "Stop added successfully."
    TRAIN_STOP_DELETED = "Train stop removed successfully."
    TRAIN_STATION_NOT_FOUND_WITH_CODE = "Station with code '{station_code}' not found."
    TRAIN_ROUTE_DELETED = "All '{count}' stops for train '{train_number}' have been deleted."
    TRAIN_STOP_DELETED = 'Stop at station {station_code} deleted.'
    TRAIN_STOP_NOT_EXISTS = "Stop for train {train_number} at station {station_code} does not exist"
    TRAIN_NUMBER_STNCODE_REQUIRED = 'train_number and station_code are required in the URL.'
    STOP_UPDATED_SUCCESSFULLY = 'Stop updated successfully.'
    ROUTE_VALIDATION_REQUIREMENTS = 'train, station, arrival_time, and departure_time are required.'
    TRAIN_ROUTE_EXISTS = "Active stop for station already exists in this train's route."



