# Reservation Application

This application allows you to create reservations using PyQt5 and MariaDB.

## Getting Started

These instructions will guide you through running the project on your computer.

### Prerequisites

To run this application, you need the following:

- Docker and Docker Compose installed.

### Installation

You can run the application by following these steps:

1. Clone this project:

git clone "project-repo-url"



2. Navigate to the project directory:

cd "project-directory"



3. Start MariaDB and application containers using Docker Compose:

docker-compose up -d



4. Find the IP address of the MariaDB container:

docker ps



Get the ID of the MariaDB container and determine its IP address with the following command:

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "mariadb-container-id"



5. Open the .env file and edit the following line:

DB_HOST=mariadb-container-ip



6. Start the application:

./reservation.sh



7. The application should now be running.

## Usage

When you start the application, the reservation screen will open. You can make reservations by entering your name, panel ID, and your preferred hours. If you don't enter the hour information, it will be considered a reservation for the whole day.

## Webhook Settings

To communicate with a webhook, you need to modify the relevant link within the application.

## Contributing

If you would like to contribute to this project, please fork it and send pull requests. Your contributions are welcome!

