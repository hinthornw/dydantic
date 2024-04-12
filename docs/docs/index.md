# Dydantic

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-black?logo=github)](https://github.com/hinthornw/dydantic)
[![PyPI](https://img.shields.io/pypi/v/dydantic)](https://pypi.org/project/dydantic/)

[Dydantic](https://github.com/hinthornw/dydantic) is a Python library for dynamically generating [Pydantic](https://github.com/pydantic/pydantic) models from [JSON Schema](https://json-schema.org/). It provides a convenient way to create Pydantic models on-the-fly from general user-defined schemas.

<p align="center">
  <img src="./static/img/dyno.svg" width="50%" alt="dyno">
</p>

## Install

```python
pip install -U dydantic
```

## Reference

### `def create_model_from_schema(json_schema: Dict[str, Any],*, **kwargs: Any) -> Type[BaseModel]:`
::: dydantic.create_model_from_schema
    handler: python
    options:
      selection:
        docstring_style: google
      rendering:
        heading_level: 3
      show_root_toc_entry: true
      members: 
        - create_model_from_schema

## Contributing

Contributions to dydantic are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository: [https://github.com/hinthornw/dydantic](https://github.com/hinthornw/dydantic)

## License

`dydantic` is open-source software licensed under the [MIT License](https://github.com/hinthornw/dydantic/blob/main/LICENSE).


Built with ❤️ by [![Twitter](https://img.shields.io/twitter/follow/WHinthorn?style=social)](https://twitter.com/WHinthorn)
