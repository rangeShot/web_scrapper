from product_scraper import ProductScraper
from helper.input import UserInputHandler


class ProductScraperApp:
    """
    A class to encapsulate the functionality of the product scraper application.
    """

    def __init__(self):
        """
        Initializes the ProductScraperApp with user inputs and sets up the scraper.
        """
        self.user_input_handler = UserInputHandler()
        self.page_count, self.proxy = self.user_input_handler.get_user_inputs()
        self.scraper = ProductScraper(self.page_count)

    def start(self):
        """
        Starts the product scraping process.
        """
        self.scraper.start()


if __name__ == "__main__":
    app = ProductScraperApp()
    app.start()
