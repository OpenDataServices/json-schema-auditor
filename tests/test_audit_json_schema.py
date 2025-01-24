import json
import pytest
from audit_json_schema import audit_schema

@pytest.fixture
def load_schema():
    """
    Loads the test schema.
    """
    with open("fixtures/schema.json", "r", encoding="utf-8") as file:
        return json.load(file)


def test_audit_schema(load_schema):
    
    keywords, types, formats = audit_schema(load_schema)

    assert keywords == {
        "$defs", "allOf", "anyOf", "contains", "definitions", "dependentSchemas", 
        "description", "else", "format", "if", "items", "not", "oneOf", "pattern",
        "prefixItems", "properties", "propertyNames", "then", "title", "type", "unevaluatedItems"
    }
    assert "nonKeyword" not in keywords
    assert types == {"array", "string"}
    assert formats == {"date-time", "uri"}
