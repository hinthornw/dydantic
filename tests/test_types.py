from collections import defaultdict
import warnings
import pytest
import pydantic
import pydantic.networks
import pydantic.types

# from pydantic._internal import _generate_schema, _config
from pydantic import create_model

# from dydantic._utils import create_model_from_schema


# Silence all warnings in this block
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    generated_formats = defaultdict(list)
    for module in [pydantic, pydantic.networks, pydantic.types]:
        for name in module.__all__:
            val = getattr(module, name)
            try:
                model = create_model("Test", my_arg=(val, ...))
                props = model.model_json_schema()["properties"]
                generated_formats[props["my_arg"]["format"]].append(
                    (f'{name}: {props["my_arg"]["type"]}', val)
                )
            except BaseException:
                continue

from pprint import pprint

pprint(dict(generated_formats))


@pytest.mark.parametrize("format_, type_", sorted(generated_formats.items()))
def test_generated_formats(format_: str, type_: str):
    # print(format_, type_)
    ...
