from server.db.init_db import SessionLocal
from server.schemas.service import UpdateServiceQuantitySchema, UpdateServiceQuantityResponse, ListServicesResponse
from server.crud.service import get_services, update_service_quantity

def read_services() -> ListServicesResponse:
    """
    Fetch all services from the database.
    This function retrieves a list of services and returns them in a structured response.

    Returns:
        ListServiceResponse: A response object containing the status, message, and list of services.
    """
    with SessionLocal() as session:
        try:
            services = get_services(session)
            return {
                    "status": "success",
                    "message": "Services retrieved successfully.",
                    "data": services
                }
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

def modify_service_quantity(
    service_id: int,
    payload: UpdateServiceQuantitySchema,
) -> UpdateServiceQuantityResponse:
    """
    Update the quantity of a service in the database.
    This function modifies the quantity of a specified service and returns the updated service data.

    Args:
        service_id (int): The ID of the service to update.
        payload (UpdateServiceQuantitySchema): The new quantity value to set for the service.
            - quantity (int): The new quantity value (must be ≥ 0).

    Returns:
        UpdateServiceQuantityResponse: A response object containing the status, message, and updated service data
            - status: "success" or "error"
            - message: A descriptive message about the operation
            - data: The updated service object if successful, or None if the service was not found
    """
    with SessionLocal() as session:
        try:
            updated_service = update_service_quantity(session, service_id, payload.quantity)
            if not updated_service:
                return {"status": "error", "message": "Service not found"}
            return {
                    "status": "success",
                    "message": "Service quantity updated successfully.",
                    "data": updated_service
                }
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }