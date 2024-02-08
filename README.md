# Top Cryptocurrency Price List Service

## Overview

This project is a prototype for a price list service that provides up-to-date information on the top cryptocurrencies, including their prices in USD. It exposes an HTTP endpoint that clients can query to retrieve this information. The service fetches data from external sources, merges it, and provides the results in either JSON or CSV format.

## How It Works

The project consists of multiple services, each responsible for a specific aspect of functionality:

- **Pricing Service**: Retrieves current pricing information for cryptocurrencies from CoinMarketCap.
- **Ranking Service**: Retrieves the latest ranking information for cryptocurrencies from CryptoCompare.
- **Data Collection Service**: Periodically fetches data from the Pricing and Ranking services, merges it, and inserts it into a PostgreSQL database.
- **HTTP API Service**: Exposes an HTTP endpoint for clients to query the database and retrieve the latest cryptocurrency price list.

### Architecture

The project follows a service-oriented architecture, with separate services for different tasks. These services communicate with each other to provide the required functionality. The architecture includes:

- **Pricing Service**: Fetches pricing data from CoinMarketCap.
- **Ranking Service**: Fetches ranking data from CryptoCompare.
- **Data Collection Service**: Periodically fetches data from the Pricing and Ranking services, merges it, and stores it in a PostgreSQL database.
- **HTTP API Service**: Exposes an HTTP endpoint for clients to query the database and retrieve the latest cryptocurrency price list.

### Technologies Used

- **Python**: Programming language used for implementing the services.
- **FastAPI**: Web framework used for building the HTTP API service.
- **Celery**: Distributed task queue used for asynchronous processing in the Data Collection Service.
- **PostgreSQL**: Relational database used for storing merged cryptocurrency data.
- **Docker**: Containerization platform used for packaging the services into containers.
- **Redis**: In-memory data store used as a message broker for Celery.
- **CoinMarketCap API**: External API used for fetching cryptocurrency pricing data.
- **CryptoCompare API**: External API used for fetching cryptocurrency ranking data.

### Running the Project

1. Clone the project repository.
2. Create  a `.env` file in the root directory of the project. You can use the provided `.env.example` file as a template.

    ```bash
    cp .env.example .env
    ```
3. Add API Keys: Open the `.env` file and provide values for the following environment variables:

    - `COINMARKETCAP_API_KEY`: Your API key for CoinMarketCap.
    - `CRYPTOCOMPARE_API_KEY`: Your API key for CryptoCompare.
4. Build Docker Containers.

    ```bash
    docker-compose build
    ```
5. Run Services in the Background: Once the containers are built, start the services in the background using the following command:

    ```bash
    docker-compose up -d
    ```
6. Verify Services: After the services are started, verify that they are running without errors by checking the logs:

    ```bash
    docker-compose logs
    ```

7. Access the HTTP API service at `http://localhost:8003` to retrieve cryptocurrency price lists. 


## API Usage

The HTTP API service provides a single endpoint `/crypto-price-and-rank/` that clients can query to retrieve cryptocurrency price lists. It accepts the following query parameters:

- **limit**: Number of top cryptocurrencies to return.
- **datetime**: Optional parameter indicating the timestamp of the returned information (default is latest time).
- **format**: Output format (JSON or CSV, default is JSON).

### Example API Request

To retrieve the top 10 cryptocurrencies in JSON format, you can make the following HTTP GET request:

```http
GET http://localhost:8003/crypto-price-and-rank/?limit=10&format=json
```



