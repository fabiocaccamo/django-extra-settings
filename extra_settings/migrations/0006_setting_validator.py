from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("extra_settings", "0005_setting_value_json_alter_setting_value_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="validator",
            field=models.CharField(
                blank=True, null=True, max_length=255, verbose_name="Validator"
            ),
        ),
    ]
