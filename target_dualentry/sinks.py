"""Dualentry target sink class, which handles writing streams."""

from __future__ import annotations

from __future__ import annotations



from target_dualentry.client import DualentrySink

class VendorsSink(DualentrySink):
    """Drip target sink class."""
    name = "Vendors"
    
    @property
    def endpoint(self) -> str:
        return f"/vendors"
    
    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record
    
    def upsert_record(self, record: dict, context: dict):
        if "id" in record:
            # Use PUT for updates when record has an ID
            record_id = record["id"]
            response = self.request_api("PUT", endpoint=f"{self.endpoint}/{record_id}", request_data=record)
            id = response.json().get("id")
        else:
            # Use POST for creates when record doesn't have an ID
            response = self.request_api("POST", request_data=record)
            id = response.json().get("id")
        return str(id) if id is not None else id, response.ok, dict()

class BillsSink(DualentrySink):
    """Drip target sink class."""
    name = "Bills"
    relation_fields = [
        {"field": "vendor_id", "objectName": "Vendors"}
    ]
    
    
    @property
    def endpoint(self) -> str:
        return f"/bills"
    
    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record

    def upsert_record(self, record: dict, context: dict):
        if "id" in record:
            # Use PUT for updates when record has an ID
            record_id = record["id"]
            response = self.request_api("PUT", endpoint=f"{self.endpoint}/{record_id}", request_data=record)
            id = response.json().get("internal_id")
        else:
            # Use POST for creates when record doesn't have an ID
            response = self.request_api("POST", request_data=record)
            id = response.json().get("internal_id")
        return str(id) if id is not None else id, response.ok, dict()
