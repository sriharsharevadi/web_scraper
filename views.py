import os
from bs4 import BeautifulSoup
from fastapi import Query, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

import constants
from helpers import get_scraping_website_page_urls, fetch_page_content_with_retry
from html_product_scraper import HTMLProductScraper
from database import get_db
from models import ProductORM, Product
from authentication import authenticate

# Create an instance of APIRouter
router = APIRouter()


@router.get("/scrape")
def scrape_dental_stall(
    number_of_pages: int = Query(1, description="Number of pages to scrape", gt=0),
    proxy_url: str = None,
    db: Session = Depends(get_db),
    auth: bool = Depends(authenticate)
):
    # get all the page urls
    page_urls = get_scraping_website_page_urls(number_of_pages)
    product_divs = []
    products_updated = 0

    # get product divs from html
    for page_url in page_urls:
        response = fetch_page_content_with_retry(page_url, proxy_url=proxy_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_divs.extend(soup.find_all('div', class_=constants.PRODUCT_DIV))

    for product_div in product_divs:
        # use HTMLProductScraper class for extracting data
        product_scraper = HTMLProductScraper(product_div)
        product_title = product_scraper.get_product_name()
        if not product_title:
            continue
        product_price = product_scraper.get_product_price()
        path_to_image = product_scraper.get_product_image_path()

        # query for existing product
        product = db.query(ProductORM).filter(ProductORM.product_title == product_title).first()

        if product:
            # update price and image of the existing product
            product.product_price = product_price
            product.path_to_image = path_to_image
            db.commit()
        else:
            # create new product
            product = ProductORM(
                product_title=product_title,
                product_price=product_price,
                path_to_image=path_to_image
            )
            db.add(product)
            db.commit()
        products_updated += 1

    return {
        "message": f"{products_updated} products were scraped and updated in DB during the current session."
    }


@router.get("/scraped_data")
def get_scraped_data(
    request: Request,
    db: Session = Depends(get_db),
    auth: bool = Depends(authenticate)
):
    base_url = str(request.base_url)

    # query for existing products
    products = db.query(ProductORM).all()

    products_with_image_url = []
    for product in products:
        # Check if product_price is not None
        if product.product_price is not None:
            product_data = {
                "product_title": product.product_title,
                "product_price": product.product_price,
                "path_to_image": product.path_to_image,
                "image_url": f"{base_url}images/{product.path_to_image.split('/')[-1]}"
            }
            products_with_image_url.append(Product(**product_data))
    return products_with_image_url


@router.get("/images/{image_name}")
async def get_image(
    image_name: str,
    auth: bool = Depends(authenticate)
):
    image_path = os.path.join(constants.IMAGES_FOLDER, image_name)

    # Check if the file exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image as a response
    return FileResponse(image_path)
