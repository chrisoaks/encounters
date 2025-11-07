import json
from typing import Any
from uuid import UUID

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


class SecretUUID:
    __slots__ = ("_value",)

    def __init__(self, value: UUID):
        self._value = value

    def get_secret_value(self) -> UUID:
        return self._value

    def __repr__(self) -> str:
        return "SecretUUID('**********')"

    def __str__(self) -> str:
        return "**********"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SecretUUID):
            return self._value == other._value
        if isinstance(other, UUID):
            return self._value == other
        return False

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        def validate(value: Any) -> "SecretUUID":
            if isinstance(value, SecretUUID):
                return value
            if isinstance(value, UUID):
                return cls(value)
            # For strings, convert to UUID first
            if isinstance(value, str):
                return cls(UUID(value))
            raise ValueError(f"Cannot convert {type(value)} to SecretUUID")

        # for JSON / python dumps, expose the underlying UUID as a string,
        # same idea as SecretStr exposing the underlying str
        def serialize(value: "SecretUUID") -> str:
            return str(value.get_secret_value())

        return core_schema.with_info_plain_validator_function(
            lambda value, _: validate(value),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                when_used="json",
            ),
        )
