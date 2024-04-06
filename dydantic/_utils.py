"""The main function in this module is `create_model_from_schema`, which takes a JSON
schema as input and returns a dynamically created Pydantic model class. The function
supports various features such as nested objects, referenced definitions, custom
configurations, custom base classes, custom validators, and more.

Example usage:

    >>> from dydantic import create_model_from_schema
    >>> json_schema = {
    ...     "title": "Person",
    ...     "type": "object",
    ...     "properties": {
    ...         "name": {"type": "string"},
    ...         "age": {"type": "integer"},
    ...     },
    ...     "required": ["name"],
    ... }
    >>> Person = create_model_from_schema(json_schema)
    >>> person = Person(name="John", age=30)
    >>> person
    Person(name='John', age=30)

The module also includes helper functions such as `_json_schema_to_pydantic_field` and
`_json_schema_to_pydantic_type` that are used internally by `create_model_from_schema`
to convert JSON schema definitions to Pydantic fields and types.

Functions:
    - create_model_from_schema: Create a Pydantic model from a JSON schema.

Helper Functions:
    - _json_schema_to_pydantic_field: Convert a JSON schema field to a Pydantic field.
    - _json_schema_to_pydantic_type: Convert a JSON schema type to a Pydantic type.

For more detailed information and examples, refer to the docstring of the
`create_model_from_schema` function.
"""

from __future__ import annotations
import datetime
import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union

from typing_extensions import Annotated
import uuid
from pydantic.networks import (
    IPv4Address,
    IPv6Address,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
)
from pydantic import (
    AnyUrl,
    Field,
    HttpUrl,
    Json,
    PostgresDsn,
    SecretBytes,
    SecretStr,
    StrictBytes,
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    FileUrl,
    DirectoryPath,
    FilePath,
    NewPath,
    MongoDsn,
)
from pydantic import BaseModel, create_model as create_model_base, ConfigDict

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from pydantic.main import AnyClassMethod
    from pydantic import EmailStr
else:
    try:
        from pydantic import EmailStr
    except ImportError:
        logger.warning(
            "EmailStr requires email_validator package to be installed. Will use str instead."
        )
        EmailStr = str


def create_model_from_schema(
    json_schema: Dict[str, Any],
    *,
    root_schema: Optional[Dict[str, Any]] = None,
    __config__: ConfigDict | None = None,
    __base__: None = None,
    __module__: str = __name__,
    __validators__: dict[str, AnyClassMethod] | None = None,
    __cls_kwargs__: dict[str, Any] | None = None,
) -> Type[BaseModel]:
    model_name = json_schema.get("title", "DynamicModel")
    field_definitions = {
        name: _json_schema_to_pydantic_field(
            name, prop, json_schema.get("required", []), root_schema or json_schema
        )
        for name, prop in (json_schema.get("properties", {}) or {}).items()
    }
    return create_model_base(model_name, **field_definitions)


FORMAT_TYPE_MAP: Dict[str, Type[Any]] = {
    "base64": Annotated[bytes, Field(json_schema_extra={"format": "base64"})],
    "binary": StrictBytes,
    "date": datetime.datetime,
    "time": datetime.time,
    "date-time": datetime.datetime,
    "duration": datetime.timedelta,
    "directory-path": DirectoryPath,
    "email": EmailStr,
    "file-path": FilePath,
    "ipv4": IPv4Address,
    "ipv6": IPv6Address,
    "ipvanyaddress": IPvAnyAddress,
    "ipvanyinterface": IPvAnyInterface,
    "ipvanynetwork": IPvAnyNetwork,
    "json-string": Json,
    "multi-host-uri": Union[PostgresDsn, MongoDsn],
    "password": SecretStr,
    "path": NewPath,
    "uri": AnyUrl,
    "uuid": uuid.UUID,
    "uuid1": UUID1,
    "uuid3": UUID3,
    "uuid4": UUID4,
    "uuid5": UUID5,
}


def _json_schema_to_pydantic_field(
    name: str,
    json_schema: Dict[str, Any],
    required: List[str],
    root_schema: Dict[str, Any],
) -> Any:
    type_ = _json_schema_to_pydantic_type(json_schema, root_schema)
    description = json_schema.get("description")
    examples = json_schema.get("examples")
    is_required = name in required
    default = ... if is_required else None

    field_kwargs = {
        "description": description,
        "examples": examples,
        "default": default,
    }

    if isinstance(type_, type) and issubclass(type_, (int, float)):
        if "minimum" in json_schema:
            field_kwargs["ge"] = json_schema["minimum"]
        if "exclusiveMinimum" in json_schema:
            field_kwargs["gt"] = json_schema["exclusiveMinimum"]
        if "maximum" in json_schema:
            field_kwargs["le"] = json_schema["maximum"]
        if "exclusiveMaximum" in json_schema:
            field_kwargs["lt"] = json_schema["exclusiveMaximum"]
        if "multipleOf" in json_schema:
            field_kwargs["multiple_of"] = json_schema["multipleOf"]

    format_ = json_schema.get("format")
    if format_ in FORMAT_TYPE_MAP:
        pydantic_type = FORMAT_TYPE_MAP[format_]

        if format_ == "binary":
            field_kwargs["strict"] = True
        elif format_ == "password":
            if json_schema.get("writeOnly"):
                pydantic_type = SecretBytes
        elif format_ == "uri":
            allowed_schemes = json_schema.get("scheme")
            if allowed_schemes:
                if len(allowed_schemes) == 1 and allowed_schemes[0] == "http":
                    pydantic_type = HttpUrl
                elif len(allowed_schemes) == 1 and allowed_schemes[0] == "file":
                    pydantic_type = FileUrl
                else:
                    field_kwargs["allowed_schemes"] = allowed_schemes

        type_ = pydantic_type

    if isinstance(type_, type) and issubclass(type_, str):
        if "minLength" in json_schema:
            field_kwargs["min_length"] = json_schema["minLength"]
        if "maxLength" in json_schema:
            field_kwargs["max_length"] = json_schema["maxLength"]
    return (type_, Field(default, json_schema_extra=field_kwargs))


def _json_schema_to_pydantic_type(
    json_schema: Dict[str, Any], root_schema: Dict[str, Any]
) -> Any:
    ref = json_schema.get("$ref")
    if ref:
        ref_path = ref.split("/")
        if ref.startswith("#/$defs/"):
            ref_schema = root_schema["$defs"]
            start_idx = 2
        else:
            ref_schema = root_schema
            start_idx = 1
        for path in ref_path[start_idx:]:
            ref_schema = ref_schema[path]
        return _json_schema_to_pydantic_type(ref_schema, root_schema)

    any_of_schemas = json_schema.get("anyOf")
    if any_of_schemas:
        any_of_types = [
            _json_schema_to_pydantic_type(schema, root_schema)
            for schema in any_of_schemas
        ]
        return Union[tuple(any_of_types)]

    type_ = json_schema.get("type")

    if type_ == "string":
        return str
    elif type_ == "integer":
        return int
    elif type_ == "number":
        return float
    elif type_ == "boolean":
        return bool
    elif type_ == "array":
        items_schema = json_schema.get("items")
        if items_schema:
            item_type = _json_schema_to_pydantic_type(items_schema, root_schema)
            return List[item_type]  # type: ignore[valid-type]
        else:
            return List
    elif type_ == "object":
        properties = json_schema.get("properties")
        if properties:
            nested_model = create_model_from_schema(
                json_schema, root_schema=root_schema
            )
            return nested_model
        else:
            return Dict
    elif type_ == "null":
        return None
    elif type_ is None:
        return Any
    else:
        raise ValueError(f"Unsupported JSON schema type: {type_} from {json_schema}")


__all__ = ["create_model_from_schema"]
