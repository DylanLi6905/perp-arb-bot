import logging

logger = logging.getLogger(__name__)

def sort_nested_dict(nested_dict: dict):
    """Sorts a nested dictionary by net rate in descending order."""
    try:
        sorted_keys = sorted(nested_dict.keys(), key=lambda k: nested_dict[k]['net_rate'], reverse=True)
        return sorted_keys
    except Exception as e:
        logger.error(f"Failed to sort nested dictionary: {e}")
        return None

def parse_opportunity_objects_from_response(response: dict) -> list:
    """Parses funding rate opportunities from the GMX API response."""
    try:
        opportunities = []
        for position_type in response.keys(): 
            for symbol, details in response[position_type].items():
                funding_rate = details['net_rate_per_hour'] * 8
                if position_type == 'long':
                    funding_rate *= -1
                funding_rate /= 100
                opportunity = {
                    "exchange": "GMX",
                    "symbol": symbol,
                    "skew_usd": details["open_interest_imbalance"],
                    "funding_rate": funding_rate,
                }
                opportunities.append(opportunity)
        return opportunities
    except Exception as e:
        logger.error(f"Failed to parse opportunity objects: {e}")
        return None

def filter_market_data(data: list, symbols: list) -> list:
    """Filters market data for specific token symbols."""
    try:
        return [market_data for market_data in data if market_data["symbol"] in symbols]
    except Exception as e:
        logger.error(f"Failed to filter market data: {e}")
        return None
