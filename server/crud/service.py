from sqlmodel import Session, select
from server.models.service import Service

def get_services(session: Session):
    """Fetch all services from the database."""
    try:
        stmt = select(Service)
        result = session.execute(stmt).scalars()
        services = result.all()
        return services
    except Exception as e:
        print(f"Error fetching services: {e}")
        session.rollback()
        return []

def create_service(session: Session, service_data: dict):
    """Create a new service in the database."""
    try:
        service = Service(**service_data)
        session.add(service)
        session.commit()
        session.refresh(service)
        return service
    except Exception as e:
        print(f"Error creating service: {e}")
        session.rollback()
        return None

def update_service_quantity(session: Session, service_id: int, quantity: int):
    """Update the quantity of a service."""
    try:
        service = session.get(Service, service_id)
        if service:
            service.quantity = quantity
            session.add(service)
            session.commit()
            session.refresh(service)
            return service
        else:
            print(f"Service with id {service_id} not found.")
            session.rollback()
            return None
    except Exception as e:
        print(f"Error updating service quantity: {e}")
        session.rollback()
        return None