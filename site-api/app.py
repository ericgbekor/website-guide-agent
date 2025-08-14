# app.py

from fastapi import APIRouter
from service.website import WebsiteService
from config.logging import get_logger


logger = get_logger()
website_service = WebsiteService()

router = APIRouter(
    prefix="/website",
    responses={404: {"description": "Not found"}},
)

    
@router.get("/services", tags=["website"])
async def get_service_details():
    """
    Retrieves details of the website service.
    
    Returns:
        dict: A dictionary containing service details.
    """
    try:
        logger.info("GET /website/services endpoint called")
        service_details = website_service.getServiceDetails()
        logger.info("Successfully retrieved service details")
        return service_details
    except Exception as error:
        logger.error(f"Error while retrieving service details: {error}")
        return {"error": f"Error while retrieving service details. Error -> {error}"}   
    
@router.get("/navigation/{section}", tags=["website"])
async def get_navigation_section(section: str):
    """
    Retrieves the navigation section details.

    Args:
        section (str): The specific section to retrieve.

    Returns:
        dict: A dictionary containing the navigation section details.
    """
    try:
        logger.info(f"GET /website/navigation/{section} endpoint called")
        section_details = website_service.getWebsitePageUrl(section)
        logger.info(f"Successfully retrieved navigation section details for: {section}")
        return section_details
    except Exception as error:
        logger.error(f"Error while retrieving navigation section '{section}': {error}")
        return {"error": f"Error while retrieving navigation section. Error -> {error}"}
