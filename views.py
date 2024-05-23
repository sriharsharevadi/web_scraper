from bs4 import BeautifulSoup
from fastapi import Query, Depends
from sqlalchemy.orm import Session

from helpers import get_scraping_website_page_urls, fetch_page_content_with_retry
from html_product_scraper import HTMLProductScraper
from database import get_db
from models import ProductORM

from fastapi import APIRouter

# Create an instance of APIRouter
router = APIRouter()


@router.get("/scrape")
def scrape_dental_stall(number_of_pages: int = Query(1, description="Page number", gt=0), db: Session = Depends(get_db)):
    page_urls = get_scraping_website_page_urls(number_of_pages)
    product_divs = []
    for page_url in page_urls:
        response = fetch_page_content_with_retry(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_divs.extend(soup.find_all('div', class_='product-inner clearfix'))

    for product_div in product_divs:
        product_scraper = HTMLProductScraper(product_div)
        product_title = product_scraper.get_product_name()
        if not product_title:
            continue
        product_price = product_scraper.get_product_price()
        path_to_image = product_scraper.get_product_image_path()
        product = db.query(ProductORM).filter(ProductORM.product_title == product_title).first()

        if product:
            product.product_price = product_price
            product.path_to_image = path_to_image
            db.commit()
        else:
            product = ProductORM(product_title=product_title, product_price=product_price, path_to_image=path_to_image)
            db.add(product)
            db.commit()

    return {"message": f"{len(product_divs)} products were scraped and updated in DB during the current session."}
