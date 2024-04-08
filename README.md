# dydantic

[![Documentation](https://img.shields.io/badge/docs-hinthornw.github.io%2Fdydantic-blue)](https://hinthornw.github.io/dydantic/) [![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/hinthornw/dydantic)

<p align="left">
  <img src="https://raw.githubusercontent.com/hinthornw/dydantic/main/docs/docs/static/img/dyno.svg" width="100" alt="dyno">
</p>


Dydantic is a Python library for dynamically generating Pydantic models from JSON schemas. It provides a convenient way to create Pydantic models on-the-fly based on the structure defined in a JSON schema.

## Features

- Automatically generate Pydantic models from JSON schemas
- Support for nested objects and referenced definitions
- Customizable model configurations, base classes, and validators
- Handle various JSON schema types and formats
- Extensible and flexible API

## Installation

You can install dydantic using pip:

```shell
pip install -U dydantic
```

## Usage

Here's a simple example of how to use dydantic to create a Pydantic model from a JSON schema:

```python
from dydantic import create_model_from_schema

json_schema = {
    "title": "Person",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
    },
    "required": ["name"],
}

Person = create_model_from_schema(json_schema)

person = Person(name="John", age=30)
print(person)  # Output: Person(name='John', age=30)
```

For more advanced usage and examples, please refer to the documentation.

## Documentation

The complete documentation for dydantic can be found at:
https://dydantic.readthedocs.io/

The documentation provides detailed information on installation, usage, API reference, and examples.

## Contributing

Contributions to dydantic are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository:
https://github.com/hinthornw/dydantic

Before contributing, please read our [contributing guidelines](CONTRIBUTING.md) for more information on how to get started.

## License

dydantic is open-source software licensed under the [MIT License](LICENSE).

## Acknowledgments

We would like to express our gratitude to the following projects:

- [Pydantic](https://github.com/pydantic/pydantic) - Dydantic builds upon the awesome Pydantic library, which provides the foundation for data validation and serialization.
- [JSON Schema](https://json-schema.org/) - Dydantic leverages the JSON Schema specification to define the structure and constraints of the data models.
- All the contributors who have helped improve dydantic with their valuable feedback, bug reports, and code contributions.

Thank you for using dydantic! If you have any questions or need assistance, please don't hesitate to reach out.