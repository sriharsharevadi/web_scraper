import os
import constants
from helpers import fetch_page_content_with_retry


class HTMLProductScraper:
    def __init__(self, product_div):
        self.product_div = product_div

    def get_product_full_name(self):
        try:
            # Locate the product price box division
            product_price_box_div = self.product_div.find('div', class_=constants.PRODUCT_PRICE_BOX_DIV)

            # Locate the footer division within the price box
            footer_div = product_price_box_div.find('div', class_=constants.FOOTER_BUTTON_DIV)

            # Locate the add-to-cart division within the footer
            add_to_cart_div = footer_div.find('div', class_=constants.ADD_TO_CART_DIV)

            # Find the first anchor tag within the add-to-cart division
            a_tag = add_to_cart_div.find('a')

            # Return the value of the 'data-title' attribute from the anchor tag
            return a_tag.get('data-title')

        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Unable to extract name for a product: {e}")
            return None

    def get_product_title_name(self):
        try:
            # Locate the product details div
            product_price_box_div = self.product_div.find('div', class_=constants.PRODUCT_DETAILS_DIV)

            # Locate the footer div within the product details div
            footer_div = product_price_box_div.find('div', class_=constants.PRODUCT_CONTENT_DIV)

            # Locate the add-to-cart div within the footer div
            add_to_cart_div = footer_div.find('h2', class_=constants.PRODUCT_TITLE_H2)

            # Locate the anchor tag within the add-to-cart div
            a_tag = add_to_cart_div.find('a')

            # Return the text of the anchor tag (the product title)
            return a_tag.get_text()

        except Exception as e:
            # Print the exception for debugging purposes
            print(f"Unable to extract name for a product: {e}")
            return None

    def get_product_name(self):
        if constants.USE_PRODUCT_FULL_NAME:
            return self.get_product_full_name()
        return self.get_product_title_name()

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
        """
        Downloads an image from the provided URL and saves it to the local filesystem.

        Args:
            image_url (str): The URL of the image to be downloaded.

        Returns:
            str: The file path of the downloaded image if successful, None otherwise.
        """
        try:
            # Fetch the content of the image URL with retries
            response = fetch_page_content_with_retry(image_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Construct the file path using the image folder and the image name from the URL
                filename = os.path.join(constants.IMAGES_FOLDER, image_url.split('/')[-1])

                # Open the file in write-binary mode and write the image content
                with open(filename, 'wb') as f:
                    f.write(response.content)

                # Return the file path of the downloaded image
                return filename

        except Exception as e:
            # Print the exception message for debugging purposes
            print(f"Error downloading {image_url}: {e}")
            return None

