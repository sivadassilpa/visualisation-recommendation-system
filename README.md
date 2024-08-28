# Visualisation Recommendation System

This project is a Visualisation Recommendation System designed to help users generate personalized data visualizations based on their profiles and preferences. The system consists of a backend service powered by Python and Auto-Sklearn, and a frontend built with React.

## Getting Started

Follow the steps below to set up the project and run it locally.

### Prerequisites

- Python 3.x
- Node.js and npm
- PostgreSQL

### DB Setup

Before starting the application, you need to populate the database with the required tables and data.

1. **Connect to your PostgreSQL database:**

   ```bash
   psql -U <username> -d <database_name>

   ```

2. **Create the necessary tables and import data:**

   ```bash
   -- Create the users table and populate it
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username TEXT,
        password_hash TEXT
    );
    \COPY users FROM 'data/users.csv' CSV HEADER;

    -- Create the userprofile table and populate it
    CREATE TABLE userprofile (
        id SERIAL PRIMARY KEY,
        userid INT,
        familiarity TEXT,
        profession TEXT,
        interest TEXT,
        country TEXT,
        CONSTRAINT fk_user FOREIGN KEY(userid) REFERENCES users(id)
    );
    \COPY userprofile FROM 'data/userprofile.csv' CSV HEADER;

    -- Create the rules table and populate it
    CREATE TABLE rules (
        id SERIAL PRIMARY KEY,
        rule_name TEXT,
        description TEXT,
        condition TEXT,
        information_type TEXT,
        action TEXT
    );
    \COPY rules FROM 'data/rules.csv' CSV HEADER;

    -- Create the feedback table and populate it
    CREATE TABLE feedback (
        id SERIAL PRIMARY KEY,
        ruleid INT,
        userprofileid INT,
        dataprofileid INT,
        preferred BOOL
    );
    \COPY feedback FROM 'data/feedback.csv' CSV HEADER;

    -- Create the data_contexts table and populate it
    CREATE TABLE data_contexts (
        id SERIAL PRIMARY KEY,
        userid INT,
        filename TEXT,
        objective TEXT,
        patternsinterest TEXT,
        groupcomparison TEXT,
        colorpreferences TEXT,
        usecase TEXT,
        createdat TIMESTAMP,
        CONSTRAINT fk_user FOREIGN KEY(userid) REFERENCES users(id)
    );
    \COPY data_contexts FROM 'data/data_contexts.csv' CSV HEADER;

   ```

3. **Start the backend server:**

   ```bash
   cd ..
   python app.py

   ```

### Backend Setup

1. **Clone the repository and navigate to the `backend/` directory:**

   ```bash
   git clone <repository-url>
   cd visualisation-recommendation-system/backend
   ```

2. **Install the required Python packages:**

   ```bash
   pip install auto-sklearn

   ```

3. **Start the backend server:**

   ```bash
   cd ..
   python app.py

   ```

### Backend Setup

1. **Navigate to the frontend/ directory:**

   ```bash
   cd .\frontend\

   ```

2. **Install dependencies:**

   ```bash
   npm install

   ```

3. **Start the frontend server:**

   ```bash
   npm start

   ```

### Running the Application

Once the backend, frontend, and database are set up, you can access the application by navigating to http://localhost:3000 in your web browser.

### Troubleshooting

1. Port Conflicts: Ensure no other services are running on the ports used by the backend (usually 5000) and frontend (usually 3000).
2. Database Connection Issues: Double-check your PostgreSQL credentials and ensure the database is running.
