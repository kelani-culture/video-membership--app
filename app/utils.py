import json
from pydantic import BaseModel
from pydantic import error_wrappers
from pydantic_core import ValidationError
from typing import List, Any
from .users.auth import authenticate

def valid_schema_data_or_error(raw_data: dict, SchemaModel: BaseModel):
    data = {}
    error: List[Any] = []
    error_str = ""

    try:
        cleaned_data = SchemaModel(**raw_data)
        data = {'session_id':cleaned_data.model_dump().get('session_id')}

    except ValidationError as e:
        error_str = e.json()

    if error_str:
        try:
            error = json.loads(error_str)
        except Exception as e:
            error = [{"loc": "non_field_error", "msg": "Unknown error"}]
    return data, error