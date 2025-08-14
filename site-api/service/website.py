import json
import os
from config.logging import get_logger

class WebsiteService:
    def __init__(self) -> None:
        self.logger = get_logger()
        self.logger.info("Initializing WebsiteService")
        webdata = self.getWebsiteData()
        self.navigation_data = webdata.get("navigation", {})
        self.services_data = webdata.get("services", {})
        self.logger.info(f"Loaded {len(self.navigation_data)} navigation items and {len(self.services_data)} services")
        
    def getWebsiteData(self)-> dict:
        """
        Retrieves website data from a predefined source.
        
        Returns:
            dict: A dictionary containing website data.
        """
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.logger.debug(f"Loading website data from directory: {current_dir}")

            # Load website navigation data
            navigation_path = os.path.join(current_dir, 'data', 'website-navigation.json')
            with open(navigation_path, 'r') as f:
                navigation_data = json.load(f)
            self.logger.debug(f"Loaded navigation data from {navigation_path}")

            # Load website services data
            services_path = os.path.join(current_dir, 'data', 'website-services.json')
            with open(services_path, 'r') as f:
                services_data = json.load(f)
            self.logger.debug(f"Loaded services data from {services_path}")

            return {
                "navigation": navigation_data.get("navigation", []),
                "services": services_data.get("services", [])
            }
        except Exception as e:
            self.logger.error(f"Error loading website data: {e}")
            raise

    def getServiceDetails(self):
        self.logger.info("Retrieving service details")
        return self.services_data
    

    def getWebsitePageUrl(self, section) -> dict:
        """
        Constructs a URL for a specific section on the website.

        Args:
            section (str): The specific section to access.

        Returns:
            str: The full URL to the specified section.
        """
        self.logger.info(f"Retrieving URL for section: {section}")
        self.logger.debug(f"Navigation Data: {self.navigation_data}")

        # Find object in JSON array navigation where section field equals section
        web_path = [item for item in self.navigation_data if item["section"].lower() == section.lower()]
        path_url = web_path[0].get("url", "") if len(web_path) > 0 else ""
        
        if path_url:
            self.logger.info(f"Found URL for section '{section}': {path_url}")
            return {"url": f"http://fictionsolutions.com{path_url}"}
        else:
            self.logger.warning(f"No URL found for section '{section}'")

        return {"url": ""}
