import pytest
from dydantic import create_model_from_schema
from pydantic import ValidationError

schema = {
    "$defs": {
        "DinoPikaFormat": {
            "properties": {
                "dino_roar_moment": {
                    "description": "moment when the dinosaur expressed a preference",
                    "title": "Dino Roar Moment",
                    "type": "string",
                },
                "pika_choice": {
                    "description": "The pika's chosen item",
                    "title": "Pika Choice",
                    "type": "string",
                },
            },
            "required": ["dino_roar_moment", "pika_choice"],
            "title": "DinoPikaFormat",
            "type": "object",
        },
        "Habitats": {
            "properties": {
                "burrow": {
                    "allOf": [{"$ref": "#/$defs/Burrow"}],
                    "description": "A typical pika burrow",
                },
            },
            "title": "Habitats",
            "type": "object",
        },
        "Burrow": {
            "properties": {
                "favourite_berries": {
                    "description": "The pika's preference in the topic 'Favourite Berries'.",
                    "items": {"$ref": "#/$defs/DinoPikaFormat"},
                    "title": "Favourite Berries",
                    "type": "array",
                },
                "preferred_burrow_location": {
                    "description": "The pika's preference in the topic 'Preferred Burrow Location'.",
                    "items": {"$ref": "#/$defs/DinoPikaFormat"},
                    "title": "Preferred Burrow Location",
                    "type": "array",
                },
            },
            "required": ["favourite_berries"],
            "title": "Burrow",
            "type": "object",
        },
        "CreaturePreferences": {
            "properties": {
                "habitats": {
                    "allOf": [{"$ref": "#/$defs/Habitats"}],
                    "description": "Details of various creature habitats",
                    "title": "Creature Habitats",
                },
            },
            "title": "CreaturePreferences",
            "type": "object",
        },
    },
    "properties": {
        "important_creature_preferences": {
            "allOf": [{"$ref": "#/$defs/CreaturePreferences"}],
            "description": "The creature's important preferences that should be stored long-term in the categories 'Habitats', 'Feeding Patterns', 'Resting Spots', 'Play and Social Interactions'.",
            "title": "Important Creature Preferences",
        }
    },
    "title": "CreaturePreferencesManifest",
    "type": "object",
}


@pytest.mark.parametrize(
    "input,should_error",
    [
        (
            {
                "important_creature_preferences": {
                    "habitats": {
                        # Missing the "dino_roar_moment" key
                        "burrow": {
                            "favourite_berries": [{"pika_choice": "Juniper Berries"}]
                        }
                    }
                }
            },
            True,
        ),
        (
            {
                "important_creature_preferences": {
                    "habitats": {
                        "burrow": {
                            "favourite_berries": [
                                {
                                    "dino_roar_moment": "Morning Dew",
                                    "pika_choice": "Blueberries",
                                }
                            ],
                            # preferred_burrow_location is missing but optional.
                        }
                    }
                }
            },
            False,
        ),
        (
            {
                "important_creature_preferences": {
                    "habitats": {
                        "burrow": {
                            "favourite_berries": [
                                {
                                    "dino_roar_moment": "Nightfall",
                                    "pika_choice": "Cranberries",
                                }
                            ],
                            "preferred_burrow_location": [
                                {
                                    "dino_roar_moment": "Dawn",
                                    "pika_choice": "Underground Burrows",
                                }
                            ],
                        }
                    }
                }
            },
            False,
        ),
    ],
)
def test_create_model_from_dino_pika_schema(input, should_error):
    model = create_model_from_schema(schema)
    model.schema_json()  # test it is serializable
    if should_error:
        with pytest.raises(ValidationError):
            model.model_validate(input)
    else:
        result = model.model_validate(input)
        model.model_validate(result.model_dump())
