# Job Application Submission API

## Description

This is a RESTful API built with Flask to handle job application submissions for software developer candidates. It allows candidates to submit their applications with personal information, additional fields, and file attachments.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install Flask Flask-MySQLdb python-dotenv
    ```
2.  **Set up MySQL database:**
    -   Create a MySQL database named `job_applications`.
    -   Create the `applications` and `attachments` tables using the provided `database.sql` file.
    -   Update the `.env` file with your MySQL credentials:
        ```
        MYSQL_HOST=localhost
        MYSQL_USER=your_mysql_user
        MYSQL_PASSWORD=your_mysql_password
        MYSQL_DB=job_applications
        ```
3.  **Run the application:**
    ```bash
    python app.py
    ```

## API Endpoint

### POST /apply

This endpoint accepts POST requests with the following:

-   **Form data:**
    -   `full_name` (required): Full name of the applicant.
    -   `email` (required): Email address of the applicant.
    -   `phone_number` (required): Phone number of the applicant.
    -   Any additional fields as needed (e.g., `linkedin`, `portfolio`).
-   **File attachments:**
    -   Any number of PDF files with any name.

**Example using curl:**

```bash
curl -X POST -F "full_name=John Doe" -F "email=john.doe@example.com" -F "phone_number=1234567890" -F "linkedin=linkedin.com/in/johndoe" -F "cv=@cv.pdf" -F "cover_letter=@cover_letter.pdf" http://127.0.0.1:5000/apply
```

**Response:**

-   **Success (201 Created):**
    ```json
    {
        "message": "Application submitted successfully",
        "application_token": "unique_application_token"
    }
    ```
-   **Error (400 Bad Request):**
    ```json
    {
        "error": "Error message"
    }
    ```
-   **Error (500 Internal Server Error):**
    ```json
    {
        "error": "Database error: error_message"
    }
