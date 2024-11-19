
# JSON Schema Auditor

**JSON Schema Auditor** is a command-line tool that inspects a JSON Schema file and reports the keywords and data types used. It supports complex schemas, including nested properties, definitions, and conditionals (`if`, `then`, `else`).

> [!IMPORTANT]
> The tool does not resolve `$ref`s outside of the specified JSON Schema file. If your schema file references other schema files, you need to run the tool against each schema file.

## Features

- **Analyze Keywords**: Identifies all JSON Schema keywords used in a given schema.
- **Extract Data Types**: Lists all data types (`string`, `integer`, etc.) defined in the schema.
- **Supports Nested Structures**: Handles deeply nested properties, `definitions`, `$defs`, and conditionals.
- **JSON Schema Compatibility**: Compatible with JSON Schema Draft 4 and later.

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/OpenDataServices/json-schema-auditor.git
cd json-schema-auditor
pip install -r requirements.txt
```

## Usage

Run the command with the path to your JSON Schema file:

```bash
python audit_json_schema.py <file_path>
```

### Arguments

- `file_path`: The path to the JSON Schema file you want to audit.

### Example

Given the following schema file `example_schema.json`:

```json
{
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" },
        "address": {
            "type": "object",
            "properties": {
                "street": { "type": "string" },
                "city": { "type": "string" }
            }
        }
    },
    "definitions": {
        "example": {
            "type": "object",
            "properties": {
                "id": { "type": "string" }
            }
        }
    }
}
```

Run the tool:

```bash
python audit_json_schema.py example_schema.json
```

Output:

```
Keywords used in the schema:
definitions, properties, type

Types used in the schema:
integer, object, string
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for feature requests and bug reports.

### To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Author**: Duncan Dewhurst
Feel free to reach out with questions or suggestions!