"""Dualentry target class."""

from __future__ import annotations

from hotglue_singer_sdk import typing as th
from hotglue_singer_sdk.target_sdk.target import TargetHotglue

from target_dualentry.sinks import (
    BillsSink,
    DualentrySink,
    VendorsSink,
)


class TargetDualentry(TargetHotglue):
    """Sample target for Dualentry."""

    def __init__(
        self,
        config=None,
        parse_env_config: bool = False,
        validate_config: bool = True,
        state: str = None
    ) -> None:
        self.config_file = config[0]
        super().__init__(config, parse_env_config, validate_config, state)

    name = "target-dualentry"

    SINK_TYPES = [VendorsSink, BillsSink]
    MAX_PARALLELISM = 1

    config_jsonschema = th.PropertiesList(
        th.Property("api_key", th.StringType, required=True),
    ).to_dict()

if __name__ == "__main__":
    TargetDualentry.cli()
