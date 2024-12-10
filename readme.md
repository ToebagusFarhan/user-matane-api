# <#>User Management API
This API provides functionalities to manage user data, including CRUD operations, file uploads for profile pictures, and personal data updates. It also integrates with a database and cloud storage.
## Notes
There are some user operation that are not used in the production, so please read them carefully since it won't be written in here.
## Dependencies
Ensure the following dependencies are installed (available in `requirements.txt`):
- Flask==3.1.0

- protobuf==5.28.3

- bcrypt==4.2.0

- pytz==2023.3.post1

- SQLAlchemy==2.0.36

- PyMySQL==1.1.1

- gunicorn==23.0.0

- python-dotenv

- google-cloud-storage==2.18.2

- google-auth==2.36.0

- google-cloud-secret-manager==2.21.1

## Environment Variables
Kindly check the .env-example

## Routes and Functionality
### Database Session Management
#### `get_session()`

-   **Description**: Context manager to manage database sessions.

### User Operations
#### `Login()`
 - **Description:**
Handle user login request.
    This function processes a login request by extracting the email and hashed password
    from the request JSON payload. It validates the presence of these fields, checks if
    the user exists in the database, and verifies the provided password hash against the
    stored hash using bcrypt.
 - **Returns:**
	- Response: A JSON response with the following possible outcomes:
		 -  `400`: If the email or password is not provided.
	     - `404`: If the user with the provided email does not exist.
	     - `401`: If the provided password is incorrect.
	     - `200`: If the login is successful, including user details (excluding sensitive data).
	     - `500`: If there is a database error.
	- Raises: 
		- SQLAlchemyError: If there is an error querying the database. 
#### `Regis()`
- **Description:**
Registers a new user in the database.
    This function handles the registration of a new user by receiving user data from a JSON request,
    hashing the provided password, and storing the user information in the database. It also performs
    basic validation to ensure that the username and email are provided.
- Returns:
	- Response: A JSON response indicating the success or failure of the user registration process.
		- On success: Returns a JSON response with status "success", a message, and the new user's ID and username.
	    - On failure: Returns a JSON response with status "fail" and an appropriate error message, along with an HTTP status code.

#### **`add_personal_data_by_uuid(user_uuid)`**
-   **Description:**  
    Adds personal data to a user profile. Receives user data via a JSON request and updates the user information in the database. Validates that the `user_uuid` is provided and ensures the user exists.
    
-   **Args:**
    
    -   `user_uuid` (string): UUID of the user to add personal data to.
-   **Returns:**
    
    -   **Response:** A JSON response indicating the success or failure of the user personal data addition process.
        -   **On success:**  
            Returns a JSON response with status `"success"`, a message, and the user's updated personal data.
        -   **On failure:**  
            Returns a JSON response with status `"fail"` and an appropriate error message.
            -   `404`: If the user with the provided `user_uuid` does not exist.
            -   `500`: If there is a database error.
            -   `401`: If the user is not allowed to access the endpoint.

----------

#### **`update_userProfile_by_uuid(user_uuid)`**

-   **Description:**  
    Updates the user profile image. Receives an image file in the request, uploads it to Cloud Storage, and generates a presigned URL for the uploaded image.
    
-   **Args:**
    
    -   `user_uuid` (string): UUID of the user to update their profile image.
-   **Returns:**
    
    -   **Response:** A JSON response indicating the success or failure of the image upload process.
        -   **On success:**  
            Returns a JSON response with status `"success"`, a message, and the presigned URL of the uploaded image.
        -   **On failure:**  
            Returns a JSON response with status `"fail"` and an appropriate error message.
            -   `400`: If no image file is found in the request.
            -   `401`: If the user is not allowed to access the endpoint.
            -   `404`: If the user with the provided `user_uuid` does not exist.
            -   `500`: If there is an error during the upload process or while generating the presigned URL.

#### **`delete_user_by_uuid(user_uuid)`**

-   **Description:**  
    Deletes a user from the database based on the provided `user_uuid`.
    
-   **Args:**
    
    -   `user_uuid` (string): UUID of the user to delete.
-   **Returns:**
    
    -   **Response:** A JSON response indicating the success or failure of the deletion process.
        -   **On success:**  
            Returns a JSON response with status `"success"` and a message indicating the user was deleted successfully.
        -   **On failure:**  
            Returns a JSON response with status `"fail"` and an appropriate error message.
            -   `401`: If the user is not allowed to access the endpoint.
            -   `404`: If the user with the provided `user_uuid` does not exist.
            -   `500`: If there is a database error.

## Another Notes
We are aware that this Documentation lacks a lot of things, and for that please just kindly ask us.