"""
An Enum containing all XPath expressions to target
"""

from enum import Enum


class XPath(Enum):
	PRODUCT_ADD_BTN = '//p[text()="Agregar"]'
	FOOTER = '//div[@class="vtex-store-footer-2-x-footerLayout"]'
	PRODUCT_GALLERY_ITEMS = '//div[@id="gallery-layout-container"]/div'
	PRODUCT_NAME = './/h3[@class="vtex-product-summary-2-x-productNameContainer mv0 vtex-product-summary-2-x-nameWrapper overflow-hidden c-on-base f5"]'
	PRODUCT_PRICE = './/div[@id="items-price"]'