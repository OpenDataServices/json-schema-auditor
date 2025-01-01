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
        formats_set (Set): Accumulated set of formats used in the schema.

    Returns:
        tuple: Two sets containing the keywords and types found in the schema.
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

            if keyword in ["allOf", "anyOf", "oneOf"]:
                for subschema in schema["keyword"]:
                    audit_schema(subschema, keywords_set, types_set, formats_set)

            if keyword in ["properties", "dependentSchemas"]:
                for prop in schema[keyword].values():
                    for key, value in prop.items():
                        # Recursively audit nested properties
                        if key == "properties":
                            for nested_prop in value.values():
                                audit_schema(nested_prop, keywords_set, types_set, formats_set)
                        else:
                            keywords_set.add(key)
                            if key == "type" and isinstance(value, str):
                                types_set.add(value)
                            elif key == "type" and isinstance(value, list):
                                types_set.update(value)
                            if key == "format":
                                formats_set.add(value)

            if keyword in ["definitions", "$defs"]:
                for defn in schema[keyword].values():
                    audit_schema(defn, keywords_set, types_set, formats_set)

            if keyword in ["not", "if", "then", "else"]:
                audit_schema(schema[keyword])

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
