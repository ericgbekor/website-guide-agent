"""Tools module for the web navigation service agent."""

import logging
import requests
from .config import Config

configs = Config()

logger = logging.getLogger(__name__)


def get_website_services() -> dict:
    """Retrieves the available services for the website.

    Args:
        None

    Returns:
        A dictionary containing the available services for the website. Example:
        {'services': [{'id': '1', 'name': 'Web Hosting', 'description': 'Reliable web hosting services'}, 
                       {'id': '2', 'name': 'Domain Registration', 'description': 'Register your domain with us'}]}

    """

    try:
        url = f"{configs.WEBSITE_API_URL}/website/services"
        logger.info("Making request to: %s", url)
        response = requests.get(
            url,
            timeout=30,  # 30 second timeout
            headers={'User-Agent': 'website-agent-service/0.1.0'}
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        return {"services": response.json()}
    except requests.exceptions.Timeout:
        logger.error("Timeout while fetching website services")
        return {"status": "error", "message": "Service request timed out"}
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching website services: %s", e)
        return {"status": "error", "message": "Failed to retrieve services"}
    except Exception as e:
        logger.error("Unexpected error fetching website services: %s", e)
        return {"status": "error", "message": "Failed to retrieve services"}

def get_website_navigation(section: str) -> dict:
    """Retrieves the navigation links for a specific website section.

    Args:
        section: The website section to retrieve navigation links for.

    Returns:
        A dictionary containing the navigation links for the specified section. Example:
        {'status': 'success', 'navigation': 'https://example.com/navigation/section'}

    """

    try:
        url = f"{configs.WEBSITE_API_URL}/website/navigation/{section}"
        logger.info("Making request to: %s", url)
        response = requests.get(
            url,
            timeout=30,  # 30 second timeout
            headers={'User-Agent': 'website-agent-service/0.1.0'}
        )
        response.raise_for_status()  # Raise exception for HTTP errors

        response_data = response.json()
        return {
            "status": "success",
            "navigation": response_data.get("url")  
        }
    except requests.exceptions.Timeout:
        logger.error("Timeout while fetching website navigation for section: %s", section)
        return {"status": "error", "message": "Navigation request timed out"}
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching website navigation for section %s: %s", section, e)
        return {"status": "error", "message": "Failed to retrieve navigation links"}
    except Exception as e:
        logger.error("Unexpected error fetching website navigation for section %s: %s", section, e)
        return {"status": "error", "message": "Failed to retrieve navigation links"}