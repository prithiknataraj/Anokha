# Project ANOKHA

## Overview

Anokha is a comprehensive dashboard application designed to track and display progress indicators for different years within each division. The project leverages MongoDB for database management and Flask for the backend, with implemented login and signup functionalities.

## Features

- **Dashboard:** Visual representation of progress indicators for various years and divisions.
- **User Authentication:** Secure login and signup functionalities.
- **Data Management:** Efficient handling of data using MongoDB.
- **Responsive Design:** Optimized for various screen sizes.

## Project Structure

```
Anokha/
│
├── .git/               # Git repository files
├── app.py              # Main application file
├── carbon.csv          # CSV file for carbon data
├── hydro.csv           # CSV file for hydro data
├── main.csv            # Main CSV file
├── op1.csv             # Operational CSV 1
├── OP2.csv             # Operational CSV 2
├── OP3.csv             # Operational CSV 3
├── static/             # Static files (CSS, JavaScript, images)
└── templates/          # HTML templates
```

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- MongoDB
- PythonAnywhere account (if deploying on PythonAnywhere)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Anokha.git
   cd Anokha
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your MongoDB connection in `app.py`:

   ```python
   from pymongo import MongoClient

   client = MongoClient('your_mongodb_connection_string')
   db = client.your_database_name
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Access the application in your web browser at `http://localhost:5000`.

### Deployment

To deploy Anokha on PythonAnywhere, follow these steps:

1. Upload the project files to your PythonAnywhere account.
2. Configure a new web app using the Flask framework.
3. Set up the WSGI file to point to `app.py`.
4. Ensure that the MongoDB connection string is correctly configured for remote access.
5. Reload the web app to apply the changes.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the existing style guidelines and includes appropriate tests.

## Acknowledgements

- The team YUKTHI
- Open-source libraries and tools

## Contact

For any inquiries or feedback, please contact prithik0926@gmail.com.
