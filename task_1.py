"""
1. Genera un script en Python que obtenga y de formato a las siguientes
propiedades de un archivo JSON:
- allergens
- sku
- vegan
- kosher
- organic
- vegetarian
- gluten_free
- lactose_free
- package_quantity
- Unit_size
- net_weight
"""

import pandas as pd
import requests
import json
import re
import task_1_query_config as query_config
from logger_config import logger as l


def get_nested_dict(
    nested_data_loc: dict, target_key: str, target_key_value: str
) -> dict:
    """
    Safely get a deeply nested dictionary from a dictionary querying by a key and its value
    Parameters:
        nested_data_loc: dict -> The deeply nested dictionary to be queried
        target_key: str -> The name of the key to be queried
        target_key_value: str -> The value of the key to be queried
    Returns:
        result: dict -> The deeply nested dictionary
    """
    result = {}
    for dictionary in nested_data_loc:
        if dictionary[target_key] == target_key_value:
            result = dictionary
    return result


def numeric_cast(str_value: str):
    """
    Casts an incorrectly typed number string into its correct type by regex matching
    Parameters:
        str_value: str -> The incorrectly typed number string to be corrected
    Returns:
        current_value: Any -> The deeply nested value which can be: int, bool, str, None, list or dict
    """
    casted_value = str_value
    try:
        if re.match(r"^-?\d+$", casted_value):  # Integer pattern
            casted_value = int(casted_value)
        elif re.match(r"^-?\d*(\.|\,)\d+$", casted_value):  # Float pattern
            casted_value = float(casted_value)
    except (TypeError, ValueError) as ex:
        # Leaves the value as a string if not any of the above types
        l.error(f"Error casting string value: {casted_value} {ex}")
    finally:
        return casted_value


def get_nested_value(dictionary: dict, key_path: list):
    """
    Safely get a deeply nested value from a dictionary using a key path list and correct its type for numeric values
    Parameters:
        dictionary: dict -> The dictionary to be queried
        key_path: list -> A list of keys needed to be traversed to get the value searched for
    Returns:
        current_value: Any -> The deeply nested value which can be: int, bool, str, None, list or dict
    """
    current_value = dictionary  # will store current nested level

    for key in key_path:
        try:
            current_value = current_value[key]
            if isinstance(current_value, str):
                current_value = numeric_cast(current_value)
        except (KeyError, TypeError, IndexError):
            return None
    return current_value


def request_data(url: str) -> dict:
    """
    Requests a website to get a JSON file
    Parameters:
        url: str -> The URL to be requested to get the raw JSON data
    Returns:
        raw_data_dict: dict -> A JSON response converted into a Python dict
    """
    response = requests.get(url)
    raw_data_dict = response.json()
    return raw_data_dict


def main() -> str:
    l.info("Running task_1...")
    l.info(f"Requesting data from {query_config.url}")
    
    # Get the data object with target info
    data = request_data(query_config.url)
    nested_data = get_nested_value(data, query_config.object_path)
    clean_data = get_nested_dict(
        nested_data, query_config.target_key, query_config.target_key_value
    )
    clean_data = json.loads(
        get_nested_value(clean_data, query_config.target_nested_json_string)
    )

    # Extract target info and create CSV
    csv_data_matrix = []
    column = []
    l.info("Obtaining values from data")
    for key_path in query_config.columns_metadata.values():
        column.append(get_nested_value(clean_data, key_path))
    csv_data_matrix.append(column)
    
    df = pd.DataFrame(
        csv_data_matrix, columns=list(query_config.columns_metadata.keys())
    )
    l.info("CSV output generated")
    l.info("task_1 completed")
    return df.to_csv(index=False)


if __name__ == "__main__":
    main()
