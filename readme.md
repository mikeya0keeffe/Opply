# Opply README

## Overview

This project is a FastAPI application for managing customers, products, and orders. The backend is implemented using asynchronous APIs with PostgreSQL as the database. I have implemented an extra customers get api for ease of access to customer details.

## Prerequisites

1. **Docker**: Install Docker by following the instructions on the [Docker Hub website](https://www.docker.com/get-started).
2. **Docker Compose**: Docker Compose is included with Docker Desktop.

## Installation

1. **Clone the repository**:
    ```
    git clone git@github.com:mikeya0keeffe/Opply.git
    cd Opply
    ```

2. **Set up environment variables**:
    Create a `.env` file in the root directory and add the following environment variables:
    ```
    # APP INFO
    APP_PORT=8000
    APP_HOST=0.0.0.0

    # DB CREDENTIALS
    APP_POSTGRES_USER=appuser
    APP_POSTGRES_PASSWORD=dbpassword
    APP_POSTGRES_VOLUME=db
    APP_POSTGRES_DB=store
    POSTGRES_PASSWORD=dbadminpassword
    POSTGRES_MASTER=postgres
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    POSTGRES_TABLE=customers
    POSTGRES_VOLUME=db

    DATABASE_URL=postgresql+asyncpg://appuser:dbpassword@db:5432/store

    # AUTH
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ```

## Usage

### Build and start the Docker containers:

1. **Build and run the application**:
    ```
    docker-compose up --build
    ```

2. **Stop the application**:
    ```
    docker-compose down
    ```

### Database Management

I recommend using [DBeaver](https://dbeaver.io/) to manage your PostgreSQL database. DBeaver is a free and open-source universal database tool.

### Access the API Documentation

Once the application is running, navigate to the following URL to access the Swagger UI for the FastAPI application:

```
http://localhost:8000/docs
```

Here you can explore the API endpoints and test them out. To log in, use one of the predefined users (e.g., `alice`, `bob`, etc.).

### Predefined Users
You can use the following predefined users to log in:

- **Username**: alice, **Password**: alicepass
- **Username**: bob, **Password**: bobpass
- **Username**: carol, **Password**: carolpass
- **Username**: david, **Password**: davidpass
- **Username**: john, **Password**: johnpass
- **Username**: eve, **Password**: evepass

## Directory Structure

The project is organized as follows:

```
server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── customer_controller.py
│   │   ├── order_controller.py
│   │   ├── product_controller.py
│   ├── services/
│   │   ├── base_service.py
│   │   ├── auth_service.py
│   │   ├── customer_service.py
│   │   ├── order_service.py
│   │   ├── product_service.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── customer_repository.py
│   │   ├── order_repository.py
│   │   ├── product_repository.py
│   ├── dependencies/
│   │   ├── auth.py
│   ├── connect.py
│   ├── init_db.py
├── Dockerfile
├── docker-compose.yml
```

### Justification for Structure

- **Controllers**: Handle the HTTP requests and responses.
- **Services**: Contain business logic.
- **Repositories**: Handle database interactions.
- **Dependencies**: Handle shared dependencies like authentication.

### Asynchronous APIs

Using asynchronous APIs improves the performance and scalability of the application by allowing it to handle more concurrent requests.

### Database Choice

PostgreSQL is used due to its robustness, scalability, and support for advanced features like JSONB, full-text search, and more.

## Deployment on AWS

1. **Create an ECR repository**:
    ```
    aws ecr create-repository --repository-name opply-task
    ```

2. **Build the Docker image**:
    ```
    docker build -t opply-task .
    ```

3. **Tag the Docker image**:
    ```
    docker tag opply-task:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/opply-task:latest
    ```

4. **Push the Docker image to ECR**:
    ```
    docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/opply-task:latest
    ```

5. **Deploy RDS Instance**
    a. Open the RDS console and create a new PostgreSQL instance.
    b. Configure the instance with the desired settings.
    c. Update the `.env` file with the RDS endpoint and credentials.
    d. Deploy the db using the db/init.sh script 

5. **Create an ECS cluster and task definition**:
    Follow the steps below to create a cluster, task definition, and service on AWS ECS. Ensure you set up autoscaling and an HTTPS certificate using AWS Certificate Manager and Route 53.

    #### Create an ECS Cluster:
    - Go to the [AWS Management Console](https://aws.amazon.com/console/).
    - Navigate to **ECS**, click on **Clusters**, then **Create Cluster**.
    - Select the cluster template (EC2 or Fargate), configure settings, and click **Create**.

    #### Create a Task Definition:
    - In the ECS console, click on **Task Definitions**, then **Create new Task Definition**.
    - Input the variables from the .env file
    - Choose launch type (EC2 or Fargate), add a container with your Docker image, and click **Create**.

    #### Create a Service:
    - In the ECS console, select your cluster, click **Create** in the Services tab.
    - Configure service settings, select the task definition, and click **Create Service**.

    #### Set Up Autoscaling:
    - Enable autoscaling during service creation.
    - Set minimum, desired, and maximum number of tasks.

    #### Set Up an HTTPS Certificate:
    - Go to [AWS Certificate Manager (ACM) console](https://console.aws.amazon.com/acm/home).
    - Request a public certificate for your domain.

    #### Configure Route 53:
    - Go to [Route 53 console](https://console.aws.amazon.com/route53/).
    - Create a hosted zone if needed and create an A record pointing to your load balancer.

    #### Attach the HTTPS Certificate to the Load Balancer:
    - Go to [Elastic Load Balancing console](https://console.aws.amazon.com/ec2/v2/home#LoadBalancers:).
    - Select your load balancer, go to **Listeners**, click **View/edit rules** for the HTTPS listener.
    - Add a new rule to forward traffic to your ECS service and select the ACM certificate.

    Your ECS cluster with autoscaling and an HTTPS certificate should now be set up and running.

## Next Steps if there were more time

- **Testing**: Write unit and integration tests.
- **Error Handling**: Write classes for common errors and improve API responses.
- **Authorization**: Add permission levels to protect apis like "customers".
- **Logging**: Implement logging.
