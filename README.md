# Memefy

Memefy is a web application designed to manage and share memes efficiently. This project utilizes FastAPI for the backend, PostgreSQL as the database, and integrates with Nextcloud for storage.

## Features

- **Meme Management**: Create, read, update, and delete memes.
- **Nextcloud Integration**: Seamlessly store and manage meme files on Nextcloud.
- **API Documentation**: Interactive API documentation provided by Swagger UI.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/memefy.git
    cd memefy
    ```

2. **Create a `.env` file** in the project root and fill in the following variables:

    ```plaintext
    APP__APP_TITLE=Your App Title
    APP__DESCRIPTION=Your App Description

    DB__DB_HOST=your-db-host
    DB__DB_PORT=your-db-port
    DB__DB_NAME=your-db-name
    DB__DB_USER=your-db-user
    DB__DB_PASS=your-db-password

    SERVICE_NAME=memefy

    # URLs
    HOST_IP=http://your-ip-address

    # Nextcloud database environment variables
    NEXTCLOUD_ADMIN_USER=your-nextcloud-admin-user
    NEXTCLOUD_ADMIN_PASSWORD=your-nextcloud-admin-password
    NEXT_CLOUD_PREFIX=remote.php/dav/files
    NEXT_CLOUD_HOST=http://your-ip-address:8082

    NEXTCLOUD_DB_ROOT_PASSWORD=your-nextcloud-db-root-password
    NEXTCLOUD_DB_PASSWORD=your-nextcloud-db-password
    ```

3. **Modify `docker-compose.yml`**:
    Replace `your-ip-address` with your actual IP address in the `NEXTCLOUD_TRUSTED_DOMAINS` section.
    ```yaml
    environment:
      - NEXTCLOUD_TRUSTED_DOMAINS=localhost your-ip-address
    ```

4. **Build and run the project**:
    ```bash
    docker-compose up --build
    ```

### Usage

- Access the application at `http://localhost:8000/api/meme/docs`.

## Environment Variables

- **APP__APP_TITLE**: Title of your application.
- **APP__DESCRIPTION**: Description of your application.
- **DB__DB_HOST**: Database host address.
- **DB__DB_PORT**: Database port.
- **DB__DB_NAME**: Database name.
- **DB__DB_USER**: Database user.
- **DB__DB_PASS**: Database password.
- **SERVICE_NAME**: Name of the service.
- **HOST_IP**: IP address where the app is hosted.
- **NEXTCLOUD_ADMIN_USER**: Nextcloud admin username.
- **NEXTCLOUD_ADMIN_PASSWORD**: Nextcloud admin password.
- **NEXT_CLOUD_PREFIX**: Nextcloud DAV files prefix.
- **NEXT_CLOUD_HOST**: Nextcloud host address.
- **NEXTCLOUD_DB_ROOT_PASSWORD**: Nextcloud database root password.
- **NEXTCLOUD_DB_PASSWORD**: Nextcloud database password.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

