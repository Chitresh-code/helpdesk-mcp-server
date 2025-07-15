from sqlmodel import Session, select
from server.models.service_request import ServiceRequest

def get_service_requests(session: Session):
    """Fetch all service requests from the database."""
    try:
        stmt = select(ServiceRequest)
        result = session.execute(stmt).scalars()
        service_requests = result.all()
        return service_requests
    except Exception as e:
        print(f"Error fetching service requests: {e}")
        session.rollback()
        return []

def create_service_request(session: Session, service_request: ServiceRequest):
    """Create a new service request."""
    try:
        session.add(service_request)
        session.commit()
        session.refresh(service_request)
        return service_request
    except Exception as e:
        print(f"Error creating service request: {e}")
        session.rollback()
        return None

def update_service_request_status(session: Session, request_id: int, status: str):
    """Update the status of a service request."""
    try:
        service_request = session.get(ServiceRequest, request_id)
        if service_request:
            service_request.status = status
            session.add(service_request)
            session.commit()
            session.refresh(service_request)
            return service_request
        else:
            print(f"ServiceRequest with id {request_id} not found.")
            session.rollback()
            return None
    except Exception as e:
        print(f"Error updating service request status: {e}")
        session.rollback()
        return None