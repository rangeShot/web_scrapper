from typing import Optional, List, Dict
from config import TARGET_WEBSITE_BASE_URL
from helper import utils, network_util
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(level=logging.INFO)


class ProductScraper:
    def __init__(self, page_count: int, target_website_base_url: str = TARGET_WEBSITE_BASE_URL, proxy_config: Optional[dict] = None):
        """
        Initialize the ProductScraper with the target website URL.
        """
        self.target_website_base_url = target_website_base_url
        self.page_count = page_count
        self.product_data: List[Dict[str, str]] = []
        self.proxy_config = proxy_config

    def _get_product_detail(self, product_soup: BeautifulSoup, folder: str) -> Dict[str, str]:
        """
        Extracts product details from a BeautifulSoup object.
        """
        try:
            product_price = float(product_soup.find(
                'span', class_='woocommerce-Price-amount amount').text.strip().replace('₹', '').replace(',', ''))
            product_title = product_soup.find('img')['title'].strip()
            product_image_url = product_soup.find('img')['data-lazy-src']
            product_image_local_url = utils.save_img(
                product_title, folder, product_image_url)
            
            return {
                "product_title": product_title,
                "product_price": product_price,
                "product_image_url": product_image_url,
                "product_image_local_url": product_image_local_url
            }
        except Exception as e:
            # logging.error(f"Error extracting product details: {e}")
            return {}

    def _get_page_details(self, page_number: int, folder: str) -> None:
        """
        Fetches and processes details from a specific page.
        """
        url = f"{self.target_website_base_url}/page/{page_number}"
        response = network_util.make_request(url, self.proxy_config)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', class_='product-inner clearfix')
            for product in products:
                product_detail = self._get_product_detail(product, folder)
                if product_detail:
                    self.product_data.append(product_detail)
        else:
            logging.error(f"Error: Failed to get page {page_number}")

    def _get_summary(self) -> str:
        summary = f"Summary: \n" + \
            f"Target Website: {self.target_website_base_url}\n" + \
            f"Total Pages Scraped: {self.page_count}\n" + \
            f"Total Products Scraped: {len(self.product_data)}\n"
        return summary

    def start(self) -> None:
        """
        Starts the scraping process for a given number of pages.
        """
        logging.info("Started scraping...")
        folder_name = 'result/' + utils.get_date_string()
        img_folder = folder_name + '/img'
        utils.ensure_folder_exists(img_folder)
        for page_number in range(1, self.page_count + 1):
            self._get_page_details(page_number, img_folder)
        utils.save_data_to_file(json.dumps(
            self.product_data), folder_name, "product_details.json")
        utils.save_data_to_file(self._get_summary(),
                                folder_name, "summary.txt")
