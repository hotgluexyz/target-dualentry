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

class BillsSink(DualentrySink):
    """Drip target sink class."""
    name = "Bills"
    
    @property
    def endpoint(self) -> str:
        return f"/bills"
    
    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record

    def upsert_record(self, record: dict, context: dict):
        response = self.request_api("POST", request_data=record) # returns 204 no content
        id = record.get("number")
        return id, response.ok, dict()