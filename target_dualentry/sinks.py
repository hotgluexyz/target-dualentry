"""Dualentry target sink class, which handles writing streams."""

from __future__ import annotations

from datetime import datetime

from hotglue_models_accounting.accounting import JournalEntry

from target_dualentry.client import DualentrySink

class VendorsSink(DualentrySink):
    """Drip target sink class."""
    name = "Vendors"
    
    @property
    def endpoint(self) -> str:
        return "/vendors"
    
    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record
    
    def upsert_record(self, record: dict, context: dict):
        state = dict()
        
        if "id" in record:
            # Use PUT for updates when record has an ID
            record_id = record["id"]
            response = self.request_api("PUT", endpoint=f"{self.endpoint}/{record_id}", request_data=record)
            id = response.json().get("id")
            state["is_updated"] = True
        else:
            # Use POST for creates when record doesn't have an ID
            response = self.request_api("POST", request_data=record)
            id = response.json().get("id")
        return str(id) if id is not None else id, response.ok, state

class BillsSink(DualentrySink):
    """Drip target sink class."""
    name = "Bills"
    relation_fields = [
        {"field": "vendor_id", "objectName": "Vendors"}
    ]
    
    
    @property
    def endpoint(self) -> str:
        return "/bills"
    
    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record

    def upsert_record(self, record: dict, context: dict):
        
        state = dict()
        
        if "id" in record:
            # Use PUT for updates when record has an ID
            record_id = record["id"]
            response = self.request_api("PUT", endpoint=f"{self.endpoint}/{record_id}", request_data=record)
            id = response.json().get("number")
            state["is_updated"] = True
        else:
            # Use POST for creates when record doesn't have an ID
            response = self.request_api("POST", request_data=record)
            id = response.json().get("number")
        return str(id) if id is not None else id, response.ok, state


class JournalEntriesSink(DualentrySink):
    """Dualentry JournalEntries sink class."""

    name = "JournalEntries"
    unified_schema = JournalEntry
    auto_validate_unified_schema = True

    @property
    def endpoint(self) -> str:
        return "/journal-entries"

    def preprocess_record(self, record: dict, context: dict) -> dict:
        payload = {}

        if record.get("transactionDate"):
            date_val = record["transactionDate"]
            date_str = date_val.strftime("%Y-%m-%d") if isinstance(date_val, datetime) else str(date_val)[:10]
            payload["date"] = date_str
            payload["transaction_date"] = date_str

        if record.get("currency"):
            payload["currency_iso_4217_code"] = record["currency"]

        if record.get("exchangeRate") is not None:
            payload["exchange_rate"] = record["exchangeRate"]

        if record.get("isDraft") is not None:
            payload["record_status"] = "draft" if record["isDraft"] else "posted"

        if record.get("id"):
            payload["id"] = record["id"]

        if record.get("subsidiaryId"):
            payload["company_id"] = int(record["subsidiaryId"])

        if record.get("description"):
            payload["memo"] = record["description"]

        payload["items"] = self._map_line_items(record.get("lineItems") or [])

        return payload

    def _map_line_items(self, line_items: list) -> list:
        items = []
        for i, line in enumerate(line_items):
            item = {
                "account_number": int(line["accountNumber"]) if line.get("accountNumber") else None,
                "debit": line.get("debitAmount") or 0,
                "credit": line.get("creditAmount") or 0,
                "memo": line.get("description") or "",
                "position": i + 1,
            }
            if line.get("customerId"):
                item["customer_id"] = int(line["customerId"])
            if line.get("vendorId"):
                item["vendor_id"] = int(line["vendorId"])
            items.append(item)
        return items

    def upsert_record(self, record: dict, context: dict):
        state = dict()

        if "id" in record:
            record_id = record.pop("id")
            response = self.request_api("PUT", endpoint=f"{self.endpoint}/{record_id}", request_data=record)
            id = response.json().get("number")
            state["is_updated"] = True
        else:
            response = self.request_api("POST", request_data=record)
            id = response.json().get("number")

        return str(id) if id is not None else id, response.ok, state
