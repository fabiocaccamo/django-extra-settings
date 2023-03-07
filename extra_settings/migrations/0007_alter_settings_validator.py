from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("extra_settings", "0006_setting_validator"),
    ]

    operations = [
        migrations.AlterField(
            model_name="setting",
            name="validator",
            field=models.CharField(
                blank=True,
                help_text=(
                    "Full python path to a validator function, "
                    "eg. 'myapp.mymodule.my_validator'"
                ),
                max_length=255,
                null=True,
                verbose_name="Validator",
            ),
        ),
    ]
