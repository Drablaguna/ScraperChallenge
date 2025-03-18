"""
2. Genera una API en python con un servicio que tenga la capacidad de recibir
una URL como parámetro de entrada (POST) y extraer los primeros 15
productos. Incluye un Dockerfile
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from logger_config import logger as l
from task_2_xpaths import XPath
import re


def browser_init(url: str, expected_loaded_object_xpath: XPath | str) -> webdriver:
    """
    Creates a webdriver object, requests an URL and waits until a specific element is located in the page
    Parameters:
        url: str -> The URL to request
        expected_loaded_object_xpath: XPath | str -> The XPath or str expression targeting an specific element for the driver to wait
    Returns:
        browser: webdriver -> The browser webdriver object with an open and loaded URL
    """
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--user-data-dir=/tmp/user-data")
    opts.add_argument("--no-sandbox")
    opts.add_argument("user-agent=Mozilla/5.0")
    browser = webdriver.Chrome(options=opts)
    l.info(f"Requesting page: {url}")
    browser.get(url)
    browser.maximize_window()
    WebDriverWait(browser, 120).until(
        ec.visibility_of_any_elements_located((By.XPATH, expected_loaded_object_xpath))
    )
    l.info("Page loaded")
    return browser


def find_object(web_browser: webdriver, xpath: XPath | str):
    """
    Wrapper for find_element() Selenium method
    Parameters:
        web_browser: webdriver -> The webdriver object to be queried upon
        xpath: XPath | str -> The XPath or str expression targeting an specific element to find
    """
    return web_browser.find_element(By.XPATH, xpath)


def find_multiple_objects(web_browser: webdriver, xpath: XPath | str) -> list:
    """
    Wrapper for find_elements() Selenium method
    Parameters:
        web_browser: webdriver -> The webdriver object to be queried upon
        xpath: XPath | str -> The XPath or str expression targeting an array of element to find
    """
    return web_browser.find_elements(By.XPATH, xpath)


def hover_on_element(
    web_browser: webdriver, xpath: XPath | str, timeout: int = 20
) -> None:
    """
    Finds an element and hovers over it
    Parameters:
        web_browser: webdriver -> The webdriver object to be manipulated
        xpath: XPath | str -> The XPath or str expression targeting an specific element to hover
        timeout: int -> The timeout value for finding the element
    """
    try:
        WebDriverWait(web_browser, timeout).until(
            ec.element_to_be_clickable((By.XPATH, xpath)),
            f"WebElement with XPath: {xpath} not found, hover was not executed",
        )
        element = web_browser.find_element(By.XPATH, xpath)
        hover = ActionChains(web_browser).move_to_element(element)
        hover.perform()
    except TimeoutException:
        l.error(
            f"Time to timeout exceeded, WebElement with XPath: {xpath} not found, hover was not executed"
        )


def get_lowest_discount_price(product_component_str:str, default_price:str) -> str:
    """
    From a webelement casted to string, use regex to match all discount prices and return the lowest value
    Parameters:
        product_component_str: str -> The webelement casted to string to be queried upon
        default_price: str -> The normal/default price tag of the webelement
    """
    promo_price_list = re.findall(r"Paga\n\$ *-?\d*\.\d+", product_component_str)
    if not promo_price_list:
        return default_price  # No promo prices, return default price
    else:
        promo_price_list = [
            float(price_str.split("$")[1].strip()) for price_str in promo_price_list
        ]
        return f"$ {'{:.3f}'.format(min(promo_price_list))}"


def main(url="") -> dict:
    l.info("Running task_2...")
    l.info(f"Creating browser...")

    # Initialize Selenium driver and wait for the page to be fully loaded
    BROWSER = browser_init(url, XPath.PRODUCT_ADD_BTN.value)
    l.info(f"Browser created {BROWSER}")
    BROWSER.implicitly_wait(4)  # Wait for a few seconds for the page to load
    BROWSER.execute_script("document.body.style.zoom=0.1;")  # Zoom to 10% so all products are visible and selectable
    hover_on_element(BROWSER, "//body")
    WebDriverWait(BROWSER, 20).until(
        ec.visibility_of_element_located((By.XPATH, XPath.FOOTER.value)),
        "Footer not found",
    )
    BROWSER.implicitly_wait(4)
    l.info("Querying products...")

    # Get all products
    found_products = find_multiple_objects(BROWSER, XPath.PRODUCT_GALLERY_ITEMS.value)
    l.info(
        f"Found {len(found_products)} products, obtaining details from all {len(found_products)} products..."
    )

    # From all products, begin extracting their data
    result = {}
    result["url"] = url
    result["products"] = []
    item = {}
    for product in found_products:
        item = {}
        item["name"] = find_object(product, XPath.PRODUCT_NAME.value).text.strip()
        item_price = find_object(product, XPath.PRODUCT_PRICE.value).text.strip()
        item["price"] = item_price
        item["promo_price"] = get_lowest_discount_price(product.text, item_price)
        result.get("products").append(item)

    l.info("Scrape complete")
    BROWSER.quit()
    l.info("Browser closed")
    l.info("task_2 completed")
    return result


if __name__ == "__main__":
    print(main("https://www.tiendasjumbo.co/supermercado/despensa/enlatados-y-conservas"))
