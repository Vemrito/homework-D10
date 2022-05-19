from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_remove_post_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Russian_mat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=64, unique=True)),
            ],
        ),
    ]
