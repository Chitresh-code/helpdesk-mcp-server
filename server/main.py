from mcp.server.fastmcp import FastMCP
from server.db.init_db import init_db
from fastapi.responses import JSONResponse
import uvicorn
import argparse

from server.tools.service import (
    read_services, modify_service_quantity
)
from server.tools.service_request import (
    read_service_requests, create_new_service_request, modify_service_request_status
)
from server.schemas.service import UpdateServiceQuantityResponse, ListServicesResponse
from server.schemas.service_request import (
    ListServiceRequestsResponse, CreateServiceRequestResponse, 
    UpdateServiceRequestStatusResponse
)

mcp = FastMCP(
    name="IT-HelpDesk", 
    enable_sessions=True, 
    stateless_http=False,
    enable_streamable_http=True,
)

# Add OpenAPI route
@mcp.custom_route(path="/openapi.json", methods=["GET"], name="openapi_schema")
def openapi_schema():
    return JSONResponse(mcp.openapi_schema())

mcp.add_tool(
    fn=read_services,
    name="read_services",
    description="""
Fetch all services from the database.
This function retrieves a list of services and returns them in a structured response.

Returns:
    ListServiceResponse: A response object containing the status, message, and list of services.
        - status: "success" or "error"
        - message: A descriptive message about the operation
        - data: A list of service objects if successful, or an error object if there was an error
""",
    structured_output=ListServicesResponse, 
)

mcp.add_tool(
    fn=modify_service_quantity,
    name="modify_service_quantity",
    description="""
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
""",
    structured_output=UpdateServiceQuantityResponse,
)

mcp.add_tool(
    fn=read_service_requests,
    name="read_service_requests",
    description="""Fetch all service requests from the database.
This function retrieves a list of service requests and returns them in a structured response.

Returns:
    ListServiceRequestsResponse: A response object containing the status, message, and list of service requests.
        - status: "success" or "error"
        - message: A descriptive message about the operation
        - data: A list of service request objects, or an empty list if no requests are found
""",
    structured_output=ListServiceRequestsResponse,
)

mcp.add_tool(
    fn=create_new_service_request,
    name="create_service_request",
    description="""Create a new service request in the database.
This function creates a new service request and returns the created request data.

Args:
    payload (ServiceRequestCreateSchema): The data for the new service request.
        - service_id (int): The ID of the service for which the request is made.
        - description (str): A description of the service request.
Returns:
    CreateServiceRequestResponse: A response object containing the status, message, and created service request data
        - status: "success" or "error"
        - message: A descriptive message about the operation
        - data: The created service request object if successful, or None if the creation failed
""",
    structured_output=CreateServiceRequestResponse,
)

mcp.add_tool(
    fn=modify_service_request_status,
    name="update_service_request_status",
    description="""Update the status of a service request in the database.
This function modifies the status of a specified service request and returns the updated request data.
Args:
    request_id (int): The ID of the service request to update.
    payload (UpdateServiceRequestStatusSchema): The new status value to set for the service request.
        - status (str): The new status value (e.g., "open", "in_progress", "closed").
Returns:
    UpdateServiceRequestStatusResponse: A response object containing the status, message, and updated service request data
        - status: "success" or "error"
        - message: A descriptive message about the operation
        - data: The updated service request object if successful, or None if the request was not found
""",
    structured_output=UpdateServiceRequestStatusResponse,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    args = parser.parse_args()

    # Initialize the database (sync version)
    init_db()

    # Start the server
    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=args.port)