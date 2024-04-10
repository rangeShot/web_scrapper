from config import DEFAULT_SCRAPE_PAGE_COUNT


class UserInputHandler:
    VALID_YES = ("true", "yes", "y", "1")
    VALID_NO = ("false", "no", "n", "0")

    def __init__(self, max_attempts=2):
        self.max_attempts = max_attempts

    def _capture_user_input(self, data_type, prompt, default_value=None):
        for _ in range(self.max_attempts):
            try:
                user_input = input(prompt)

                if data_type == int:
                    return int(user_input)
                elif data_type == bool:
                    if user_input.lower() in self.VALID_YES:
                        return True
                    elif user_input.lower() in self.VALID_NO:
                        return False
                elif data_type == str:
                    return user_input
                else:
                    raise TypeError(f"Unsupported data type: {data_type}")
            except (ValueError, TypeError) as e:
                print(f"WTH... I'm expecting a {data_type}. Try again: ")
        else:
            if default_value is not None:
                print(
                    f"Let it be... I'll manage with default value: {default_value}")
                return default_value
            else:
                raise ValueError(
                    "Input limit reached. No default value provided.")

    def get_user_inputs(self):
        page_count_msg = "Enter Number Of Pages To Be Scraped: "
        proxy_needed_msg = "Do you want to set up proxy server(Y/N): "
        http_proxy_server_msg = "Enter Url Of HTTP Proxy server: "
        https_proxy_server_msg = "Enter Url Of HTTPS Proxy server: "
        proxies = None

        total_pages = self._capture_user_input(
            int, page_count_msg, DEFAULT_SCRAPE_PAGE_COUNT)
        is_proxy_server_needed = self._capture_user_input(
            bool, proxy_needed_msg, False)

        if is_proxy_server_needed:
            http_proxy_server = self._capture_user_input(
                str, http_proxy_server_msg)
            https_proxy_server = self._capture_user_input(
                str, https_proxy_server_msg)
            proxies = {
                'http': http_proxy_server,
                'https': https_proxy_server
            }

        return total_pages, proxies
