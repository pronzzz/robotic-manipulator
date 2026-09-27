# llm/schema.py

ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["move_to", "grasp", "release"]
                    },
                    "target": {
                        "type": "string",
                        "description": "The name of the object or location, e.g., 'red_block', 'shelf'."
                    }
                },
                "required": ["action"],
                "additionalProperties": False
            }
        }
    },
    "required": ["steps"],
    "additionalProperties": False
}
