Flask URL Shortener API
A URL Shortener REST API built using Python, Flask, Flask-SQLAlchemy, and SQLite. The application generates short codes for long URLs, redirects users to the original URLs, and tracks the number of clicks.

Features
Shorten long URLs using unique short codes.
Redirect short URLs to their original destinations.
Track click counts for each URL.
Retrieve all stored URLs and their details.
Store URL information in an SQLite database.
Automatically record URL creation timestamps.
Technologies Used
Python
Flask
Flask-SQLAlchemy
SQLite
shortuuid
Project Structure
text
flask-url-shortener/
├── app.py
├── test.py
├── requirements.txt
├── .gitignore
└── README.md
The SQLite database is created locally when the application runs.
Installation and Setup
1. Clone the Repository
bash
git clone https://github.com/ujwal-kashyap/flask-url-shortener.git
cd flask-url-shortener
2. Create a Virtual Environment
bash
python -m venv .venv
Activate the virtual environment on Windows PowerShell:
powershell
.venv\Scripts\Activate.ps1
3. Install Dependencies
bash
pip install -r requirements.txt
4. Run the Application
bash
python app.py
The API will run locally at:
http://127.0.0.1:3434
API Endpoints
Method	Endpoint	Description
POST	/shorten	Create a short URL
GET	/<short_code>	Redirect to the original URL
GET	/urls	Retrieve all stored URLs
API Usage
1. Shorten a URL
Request
http
POST http://127.0.0.1:3434/shorten
Content-Type: application/json

Request Body

json
{
  "url": "https://www.example.com"
}


Example Response

json
{
  "message": "url recived",
  "original_url": "https://www.example.com",
  "short_code": "a1B2c3"
}


The short code shown above is an example. The application generates a code dynamically.

2. Redirect to the Original URL

Open the following URL in your browser, replacing the example code with the generated short code:

http://127.0.0.1:3434/a1B2c3

The application redirects you to the original URL and increments its click count.

3. Retrieve All URLs

Request

http
GET http://127.0.0.1:3434/urls


This endpoint returns all stored URLs, including their IDs, short codes, creation timestamps, and click counts.

Database

The application uses SQLite and SQLAlchemy to store:

Original URLs
Short codes
Creation timestamps
Click counts
Future Improvements
URL validation and improved error handling
Handling short-code collisions
Custom short URLs
URL expiration
Automated unit tests
Deployment to a cloud hosting platform
Author

Ujwal Kashyap

GitHub: ujwal-kashyap

License

No license has been specified for this project yet.
