# Sports Scraper

**Sports Scraper** is a full-stack web application for scraping and serving sports data through a Python API with a modern frontend interface. The project is fully containerized using Docker, making it easy to run locally or deploy consistently across environments.

## Features

-  Scrapes sports-related data from configured sources (currently Betr)
- Python backend API responsible for scraping and data processing  
- Frontend interface for interacting with scraped data  
- Docker & Docker Compose support for simple setup  

## Prerequisites

Before running the project, ensure you have the following installed:

- **Docker** 
- **Git**  

> You do **not** need Python or Node installed locally if using Docker.

## Running with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/matthewlu2/sports_scraper.git
cd sports_scraper
```

### 2. Build and Start the Application

```bash
docker compose up --build
```

### 3. Access the Application

Once running, access the app in your browser:

- **Frontend:** http://localhost:3000  
- **Backend API:** http://localhost:5001

### 4. Stop the Application

```bash
docker compose down
```