# FastAPI Dental Stall Scraper

This repository contains a FastAPI application for scraping dental products from a website, storing them in a database, and serving the scraped data via API endpoints.

## Features

- **Scraping Endpoint**: Allows scraping dental products from the specified website.
- **Scraped Data Endpoint**: Retrieves scraped dental product data from the database.
- **Image Endpoint**: Serves product images stored in the repository.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sriharsharevadi/web_scraper.git
    ```

2. Navigate to the project directory:

    ```bash
    cd web_scraper
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the FastAPI server**:

    ```bash
    uvicorn main:app --reload
    ```

2. **Access the API**:

    - Scraping Endpoint: `http://localhost:8000/scrape`
    - Scraped Data Endpoint: `http://localhost:8000/scraped_data`
    - Image Endpoint: `http://localhost:8000/images/{image_name}`

    