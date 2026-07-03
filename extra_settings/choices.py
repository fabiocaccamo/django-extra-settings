from django.db import models


class SettingType(models.TextChoices):
    BOOL = "bool", "bool"
    DATE = "date", "date"
    DATETIME = "datetime", "datetime"
    DECIMAL = "decimal", "decimal"
    DURATION = "duration", "duration"
    EMAIL = "email", "email"
    FILE = "file", "file"
    FLOAT = "float", "float"
    IMAGE = "image", "image"
    INT = "int", "int"
    JSON = "json", "json"
    STRING = "string", "string"
    TEXT = "text", "text"
    TIME = "time", "time"
    URL = "url", "url"
    # COLOR = "color", "color"  # TODO
    # HTML = "html", "html"     # TODO
    # UUID = "uuid", "uuid"     # TODO
