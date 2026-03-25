# jumia_page_scraper
It is a scraper designed with playwright and python to scrape products
# Jumia Product Scraper 🛒

This project is a Python web scraper that extracts product data from Jumia's mobile phones category.

It uses browser automation to handle dynamic content and retrieve real-time product information.

## Features

- Extracts product names
- Extracts product prices
- Handles dynamic website loading
- Saves data into a CSV file

## Technologies Used

- Python
- Playwright (for browser automation)
- CSV (for data storage)

## Project Structure

jumia_phone_scraper/

scraper.py → main scraping script  
requirements.txt → project dependencies  
data/products.csv → scraped data output  

## How It Works

1. Opens Jumia mobile phones page  
2. Waits for products to load  
3. Extracts product details  
4. Saves results into a CSV file  

## How to Run

1 Install dependencies


## Example Output

| Name | Price |
|------|------|
| Samsung Galaxy A14 | KSh 18,999 |
| Redmi Note 12 | KSh 22,499 |

## Learning Purpose

This project was built to practice:

- Web scraping on real-world websites
- Handling dynamic content
- Browser automation
- Data extraction and storage

## Disclaimer

This project is for educational purposes only.

