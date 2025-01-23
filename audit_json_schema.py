import json
import os
import click


def audit_schema(schema, keywords_set=None, types_set=None, formats_set=None):
    """
    Audits a JSON Schema to identify the keywords and types used.

    Args:
        schema (dict): The JSON Schema to audit.
        keywords_set (set): Accumulated set of keywords used in the schema.
        types_set (set): Accumulated set of types used in the schema.
        formats_set (Set): Accumulated set of string formats used in the schema.

    Returns:
        tuple: Three sets containing the keywords, types and string formats found in the schema.
    """
    if keywords_set is None:
        keywords_set = set()
    if types_set is None:
        types_set = set()
    if formats_set is None:
        formats_set = set()

    if isinstance(schema, dict):
        for keyword in schema:
            keywords_set.add(keyword)

            # Keywords whose value is a list of schemas
            if keyword in ["allOf", "anyOf", "oneOf", "prefixItems"]:
                for subschema in schema[keyword]:
                    audit_schema(subschema, keywords_set, types_set, formats_set)

            # Keywords whose value is an object with key-value pairs where the values are schemas
            if keyword in ["properties", "definitions", "$defs", "dependentSchemas"]:
                for subschema in schema[keyword].values():
                    audit_schema(subschema, keywords_set, types_set, formats_set)
            
            # Keywords whose value is a schema
            if keyword in ["items", "unevaluatedItems", "contains", "not", "if", "then", "else", "propertyNames"]:
                audit_schema(schema[keyword], keywords_set, types_set, formats_set)

            if keyword == "type":
                types = schema["type"]
                if isinstance(types, str):
                    types_set.add(types)
                elif isinstance(types, list):
                    types_set.update(types)
            
            if keyword == "format":
                formats_set.add(schema["format"])

    return keywords_set, types_set, formats_set


@click.command()
@click.argument("file_path", type=click.Path(exists=True, readable=True))
def main(file_path):
    """
    CLI to audit a JSON Schema.

    FILE_PATH is the path to the JSON Schema file to audit.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_schema = json.load(file)
    except json.JSONDecodeError as e:
        click.echo(f"Invalid JSON: {e}", err=True)
        return
    except Exception as e:
        click.echo(f"Error reading the file: {e}", err=True)
        return

    # Audit the schema
    keywords, types, formats = audit_schema(json_schema)

    # Report the results
    click.echo("\nKeywords used in the schema:")
    click.echo(", ".join(sorted(keywords)))

    click.echo("\nTypes used in the schema:")
    click.echo(", ".join(sorted(types)))

    click.echo("\nFormats used in the schema:")
    click.echo(", ".join(sorted(formats)))

if __name__ == "__main__":
    main()
