# Workaround to avoid: "ModuleNotFoundError: No module named 'jsonfield'"
try:
    from jsonfield.fields import JSONField
except ImportError:
    from django.db.models import JSONField

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("extra_settings", "0004_setting_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="value_json",
            field=JSONField(blank=True, default=dict, verbose_name="Value"),
        ),
        migrations.AlterField(
            model_name="setting",
            name="value_type",
            field=models.CharField(
                choices=[
                    ("bool", "bool"),
                    ("date", "date"),
                    ("datetime", "datetime"),
                    ("decimal", "decimal"),
                    ("duration", "duration"),
                    ("email", "email"),
                    ("file", "file"),
                    ("float", "float"),
                    ("image", "image"),
                    ("int", "int"),
                    ("json", "json"),
                    ("string", "string"),
                    ("text", "text"),
                    ("time", "time"),
                    ("url", "url"),
                ],
                max_length=20,
                verbose_name="Type",
            ),
        ),
    ]
