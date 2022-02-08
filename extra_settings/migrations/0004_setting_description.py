# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("extra_settings", "0003_modified_upload_to"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Description"),
        ),
    ]
