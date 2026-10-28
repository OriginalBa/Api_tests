success_review_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Review Schema",
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "club": {"type": "number"},
        "assessment": {"type": "number"},
        "created": {"type": "string"},
        "text": {"type": "string"}
    },
    "required": ["id", "club", "assessment", "created"]
}
success_create_club = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "id": {
            "type": "number"
        },
        "bookTitle": {
            "type": "string"
        },
        "bookAuthors": {
            "type": "string"
        },
        "publicationYear": {
            "type": "number"
        },
        "description": {
            "type": "string"
        },
        "telegramChatLink": {
            "type": "string"
        },
        "owner": {
            "type": "number"
        },
        "members": {
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "reviews": {
            "type": "array",
            "items": success_review_schema
        },
        "created": {
            "type": "string"
        },
        "modified": {}
    },
    "required": [
        "id",
        "bookTitle",
        "bookAuthors",
        "publicationYear",
        "description",
        "telegramChatLink",
        "owner",
        "members",
        "reviews",
        "created",
        "modified"
    ]
}

success_clubs_list = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Clubs List Schema",
    "type": "object",
    "properties": {
        "count": {"type": "number"},
        "next": {"type": ["string", "null"]},
        "previous": {"type": ["string", "null"]},
        "results": {
            "type": "array",
            "items": success_create_club
        }
    },
    "required": ["count", "next", "previous", "results"]
}
