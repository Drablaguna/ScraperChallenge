"""Module containing only targets for extracting information from a web requested JSON"""

# URL to query
url = "https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json"

# Deeply nested object with target information to obtain
object_path = ["allVariants", 0, "attributesRaw"]

# Target key and value to find an specific object
target_key = "name"
target_key_value = "custom_attributes"

# Target nested JSON string (specific use cases)
target_nested_json_string = ["value", "es-CR"]

# Extensible dict to define data to be queried: the column name and a list with the path to its value
# Directly influences data available in final CSV file
columns_metadata = {
    "allergens": ["allergens", "value", 0, "name"],
    "sku": ["sku", "value"],
    "vegan": ["vegan", "value"],
    "kosher": ["kosher", "value"],
    "organic": ["organic", "value"],
    "vegetarian": ["vegetarian", "value"],
    "gluten_free": ["gluten_free", "value"],
    "lactose_free": ["lactose_free", "value"],
    "package_quantity": ["package_quantity", "value"],
    "unit_size": ["unit_size", "value"],
    "net_weight": ["net_weight", "value"],
}
