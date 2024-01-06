# Capstone Project - IBM Full Stack Software Developer 

## Description

This Capstone project, part of the IBM Full Stack Software Developer Specialization, showcases a dealership management application. It integrates dealership data storage with IBM Cloud Database and utilizes IBM Watson's Natural Language Understanding for review sentiment analysis. The project features Django for backend operations, JavaScript with HTML and CSS for the frontend, and API connections to IBM Cloud. The application is containerized using Docker and deployed through Kubernetes.

## Running the Application with Docker

To run the application using Docker:

1. **Build the Docker Image**:
   - In the project's root directory (where the Dockerfile is located), build the Docker image:
     ```
     docker build -t ibm-capstone-project .
     ```

2. **Run the Docker Container**:
   - Start the container, mapping the container's port 8000 to the host's port 8000:
     ```
     docker run -p 8000:8000 ibm-capstone-project
     ```

3. **Accessing the Application**:
   - Open `http://localhost:8000/djangoapp` in a web browser. Note the `/djangoapp` at the end of the URL.

## Project Breakdown

### Prework: IBM Cloud Setup and Watson NLU Service
1. Create an IBM cloud account.
2. Set up an instance of the Natural Language Understanding (NLU) service.

### Building and Deploying the Application
1. Develop static pages fulfilling user stories.
2. Deploy the application on IBM Cloud for live interaction.

### Implementing User Management
1. Utilize Django's authentication system for user management.
2. Set up continuous integration and continuous deployment (CI/CD) pipelines.

### Backend Services Development
1. Develop cloud functions for dealers and reviews management.
2. Create Django models and views for car models and makes.
3. Integrate dealerships, reviews, and car data using Django views.

### Dynamic Web Pages with Django Templates
1. Create a page listing all dealerships.
2. Develop a page to display reviews for a specific dealer.
3. Implement functionality for users to add reviews for dealerships.

### Containerization and Final Deployment
1. Prepare the application for deployment by adding necessary artifacts.
2. Deploy the application using Docker and Kubernetes.
