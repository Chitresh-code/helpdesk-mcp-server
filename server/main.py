from mcp.server.fastmcp import FastMCP
from sqlmodel import Session
from server.db.init_db import SessionLocal, init_db
from server.schemas.service import (
    ListServicesResponse, UpdateServiceQuantitySchema, UpdateServiceQuantityResponse
)
from server.crud.service import get_services, update_service_quantity
from server.schemas.service_request import (
    ListServiceRequestsResponse, ServiceRequestCreateSchema,
    CreateServiceRequestResponse, UpdateServiceRequestStatusSchema, UpdateServiceRequestStatusResponse
)
from server.crud.service_request import get_service_requests, create_service_request, update_service_request_status
from server.models.service_request import ServiceRequest
from fastapi.responses import JSONResponse
import uvicorn
import argparse

mcp = FastMCP(
    name="IT-HelpDesk", 
    enable_sessions=True, 
    stateless_http=False,
    enable_streamable_http=True,
)

# Expose FastAPI app
app = mcp.streamable_http_app

# Add OpenAPI route
@app.get("/openapi.json")
def openapi_schema():
    return JSONResponse(mcp.openapi_schema())

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

@mcp.tool()
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    args = parser.parse_args()

    # Initialize the database (sync version)
    init_db()

    # Start the server
    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=args.port)