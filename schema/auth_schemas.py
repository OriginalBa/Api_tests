success_auth = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "refresh": {
            "type": "string"
        },
        "access": {
            "type": "string"
        }
    },
    "required": [
        "refresh",
        "access"
    ]
}

base_error_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "detail": {
            "type": "string"
        }
    },
    "required": [
        "detail"
    ]
}

invalid_credentials_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "username": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "password": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": []
}

wrong_credentials_auth = base_error_schema
unsupported_media_type = base_error_schema
