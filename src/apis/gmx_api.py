import os
import sys
import logging
from dotenv import load_dotenv
import requests
import contextlib
import io

# ------------------------------------------------------------------------------
# Optional: Monkey-patch requests.get for a longer timeout (if desired)
# ------------------------------------------------------------------------------
original_get = requests.get
def patched_get(*args, **kwargs):
    kwargs.setdefault('timeout', 10)  # Wait up to 10 seconds if not specified
    return original_get(*args, **kwargs)
requests.get = patched_get

# ------------------------------------------------------------------------------
# Load Environment Variables and Configure Logging
# ------------------------------------------------------------------------------
load_dotenv()  # Loads the .env file (which should define PATH_TO_GMX_CONFIG_FILE)
PATH_TO_GMX_CONFIG_FILE = os.getenv("PATH_TO_GMX_CONFIG_FILE")
if not PATH_TO_GMX_CONFIG_FILE:
    print("Error: PATH_TO_GMX_CONFIG_FILE not set in your .env file.")
    sys.exit(1)

logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
# Reduce verbosity for the GMX SDK if needed.
logging.getLogger("gmx_python_sdk").setLevel(logging.CRITICAL)

# ------------------------------------------------------------------------------
# Suppress unwanted prints during import of problematic SDK modules
# ------------------------------------------------------------------------------
with contextlib.redirect_stdout(io.StringIO()):
    from gmx_python_sdk.scripts.v2.gmx_utils import ConfigManager
    from gmx_python_sdk.scripts.v2.get.get_funding_apr import GetFundingFee

# ------------------------------------------------------------------------------
# Create the GMX Configuration Object
# ------------------------------------------------------------------------------
def get_config_object() -> ConfigManager:
    config_object = ConfigManager(chain="arbitrum")
    try:
        config_object.set_config(PATH_TO_GMX_CONFIG_FILE)
    except Exception as e:
        logger.error(f"Error setting GMX config: {e}")
        sys.exit(1)
    return config_object

config = get_config_object()

# ------------------------------------------------------------------------------
# Instantiate the Funding Fee Getter
# ------------------------------------------------------------------------------
funding_fee_getter = GetFundingFee(config)

# ------------------------------------------------------------------------------
# Token Symbol Mapping (Optional)
# ------------------------------------------------------------------------------
# In this example, we remove any filtering for a single token.
# However, if needed, you can include a mapping (e.g., "BTC" -> "WBTC").
TOKEN_SYMBOL_MAPPING = {
    "BTC": "WBTC",  # This mapping is still used for querying purposes.
    # Add more mappings here if necessary.
}

# ------------------------------------------------------------------------------
# Function to Get All Funding Rates
# ------------------------------------------------------------------------------
def get_all_funding_rates(query_symbol: str = None):
    """
    Fetches funding rate data from the GMX SDK.
    
    If query_symbol is provided (e.g. "WBTC"), that is passed to the SDK's get_data() method.
    The SDK returns a dictionary with keys "long", "short", and "parameter".
    
    This function returns the entire dictionary.
    """
    # If a query symbol is not provided, you can choose one.
    # In many cases, using "WBTC" returns data for all tokens.
    symbol_to_query = query_symbol if query_symbol else "WBTC"
    try:
        data = funding_fee_getter.get_data(symbol_to_query)
        return data
    except Exception as e:
        logger.error(f"Error fetching funding data for query symbol {symbol_to_query}: {e}", exc_info=True)
        return None

# ------------------------------------------------------------------------------
# Main Execution: Print All Funding Rates
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Query using "WBTC" (or change if needed) so that the returned dictionary
    # includes all tokens.
    funding_data = get_all_funding_rates("WBTC")
    
    if funding_data is None:
        print("Failed to retrieve funding rate data.")
        sys.exit(1)
    
    # Check that the returned dictionary has the expected keys.
    if not ("long" in funding_data and "short" in funding_data):
        print("The funding data does not have the expected structure.")
        sys.exit(1)
    
    print("\nGMX v2 Funding Rates (% per hour)")
    # We assume that the keys in the "long" and "short" sub-dictionaries are the token symbols.
    # We'll iterate over the tokens in the "long" section.
    for token, long_rate in funding_data["long"].items():
        short_rate = funding_data["short"].get(token)
        print(f"\n{token}")
        if long_rate is not None:
            print(f"  Long funding rate: {long_rate:.4f}%")
        else:
            print("  No long funding rate available.")
        if short_rate is not None:
            print(f"  Short funding rate: {short_rate:.4f}%")
        else:
            print("  No short funding rate available.")
