import os
import requests


class HTMLProductScraper:
    def __init__(self, product_div):
        self.product_div = product_div
        self.images_folder = "images"

    def get_product_name(self):
        try:
            # Find the div with class "mf-product-content"
            product_content_div = self.product_div.find('div', class_='mf-product-content')

            # Within this div, find the h2 tag with class "woo-loop-product__title"
            short_description_div = product_content_div.find('div', class_='woocommerce-product-details__short-description')

            # Within this h2 tag, find the <a> tag
            p_tag_data = short_description_div.find('p')

            # Extract the text content from the <a> tag
            return p_tag_data.get_text()
        except Exception:
            print("Unable to extract name for a product")

    def get_product_price(self):
        try:
            # Find the span with class "price"
            price_span = self.product_div.find('span', class_='price')

            # Within this span, find the span with class "woocommerce-Price-amount amount"
            amount_span = price_span.find('span', class_='woocommerce-Price-amount amount')

            # Within this span, find the <bdi> tag
            bdi_tag = amount_span.find('bdi')

            # Extract the text content from the <bdi> tag and return number
            return float(bdi_tag.contents[-1].get_text(strip=True))
        except Exception:
            print(f"Unable to get price for product {self.get_product_name()}")

    def get_product_image_path(self):
        try:
            image_div_tag = self.product_div.find('div', class_='mf-product-thumbnail')

            image_tag = image_div_tag.find('img')

            # Extracting the URL from data-lazy-src attribute
            image_url = image_tag.get('data-lazy-src')

            downloaded_image_path = self.download_image(image_url)

            return downloaded_image_path
        except Exception:
            print(f"Unable to get image for product {self.get_product_name()}")

    def download_image(self, image_url):
        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                filename = os.path.join(self.images_folder, image_url.split('/')[-1])
                with open(filename, 'wb') as f:
                    f.write(response.content)
                return filename
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")
