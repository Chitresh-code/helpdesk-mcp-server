from server.schemas.service_request import (
    ListServiceRequestsResponse, ServiceRequestCreateSchema,
    CreateServiceRequestResponse, UpdateServiceRequestStatusSchema, UpdateServiceRequestStatusResponse
)
from server.crud.service_request import (
    get_service_requests, create_service_request, update_service_request_status
)
from server.models.service_request import ServiceRequest
from server.db.init_db import SessionLocal

def read_service_requests() -> ListServiceRequestsResponse:
    """
    Fetch all service requests from the database.
    This function retrieves a list of service requests and returns them in a structured response.

    Returns:
        ListServiceRequestsResponse: A response object containing the status, message, and list of service requests.
            - status: "success" or "error"
            - message: A descriptive message about the operation
            - data: A list of service request objects, or an empty list if no requests are found    
    """
    with SessionLocal() as session:
        try:
            service_requests = get_service_requests(session)
            return {
                    "status": "success",
                    "message": "Service requests retrieved successfully.",
                    "data": service_requests
                }
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

def create_new_service_request(
    request: ServiceRequestCreateSchema
) -> CreateServiceRequestResponse:
    """
    Create a new service request in the database.
    This function takes a service request schema, creates a new service request object,
    and attempts to save it to the database.

    Args:
        request (ServiceRequestCreateSchema): The service request data to create.
            - service_id (int): The ID of the service being requested.
            - requester_name (str): The name of the person making the request.
            - status (str): The initial status of the service request (default is "pending").

    Returns:
        CreateServiceRequestResponse: A response object containing the status, message, and created service request data.
            - status: "success" or "error"
            - message: A descriptive message about the operation
            - data: The created service request object if successful, or None if an error occurred
    """
    with SessionLocal() as session:
        try:
            new_request = ServiceRequest(**request.model_dump())
            created = create_service_request(session, new_request)
            return {
                    "status": "success",
                    "message": "Service request created successfully.",
                    "data": created
                }
        except Exception as e:
            return {
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

def modify_service_request_status(
    request_id: int,
    payload: UpdateServiceRequestStatusSchema,
) -> UpdateServiceRequestStatusResponse:
    """
    Update the status of a service request in the database.
    This function modifies the status of a specified service request and returns the updated service request data.

    Args:
        request_id (int): The ID of the service request to update.
        payload (UpdateServiceRequestStatusSchema): The new status value to set for the service request.
            - status (str): The new status value (e.g., "pending", "in_progress", "completed").

    Returns:
        UpdateServiceRequestStatusResponse: A response object containing the status, message, and updated service request data
            - status: "success" or "error"
            - message: A descriptive message about the operation
            - data: The updated service request object if successful, or None if the service request was not found
    """
    with SessionLocal() as session:
        try:
            updated = update_service_request_status(session, request_id, payload.status)
            if updated:
                return {
                        "status": "success",
                        "message": "Service request status updated successfully.",
                        "data": updated
                    }
            else:
                return {
                    "error": {
                        "code": -1,
                        "message": "Service request not found"
                    }
                }
        except Exception as e:
            return {
               "error": {
                    "code": -1,
                    "message": str(e)
                }
            }