import json
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class SecretJson:
    __slots__ = ("_value",)

    def __init__(self, value: Any):
        self._value = value

    def get_secret_value(self) -> Any:
        return self._value

    def __repr__(self):
        return "SecretJson('**********')"

    def __str__(self):
        return "**********"

    def __eq__(self, other):
        if isinstance(other, SecretJson):
            return self._value == other._value
        return False

    def json(self) -> str:
        return json.dumps(self._value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        # validator: any JSON → SecretJson
        def validate(value: Any) -> "SecretJson":
            if isinstance(value, SecretJson):
                return value
            return cls(value)

        # serializer: SecretJson → underlying JSON value
        def serialize(value: "SecretJson") -> Any:
            return value.get_secret_value()

        return core_schema.no_info_after_validator_function(
            validate,
            core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                when_used="json",
            ),
        )
