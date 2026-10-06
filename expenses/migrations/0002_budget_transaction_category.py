from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('expenses', '0001_initial')]
    operations = [
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.CharField(choices=[('Food','Food'),('Travel','Travel'),('Shopping','Shopping'),('Bills','Bills'),('Education','Education'),('Health','Health'),('Entertainment','Entertainment'),('Other','Other')], default='Other', max_length=30),
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(help_text='Use the first day of the month.')),
                ('category', models.CharField(choices=[('Food','Food'),('Travel','Travel'),('Shopping','Shopping'),('Bills','Bills'),('Education','Education'),('Health','Health'),('Entertainment','Entertainment'),('Other','Other')], max_length=30)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='budgets', to='auth.user')),
            ],
            options={'ordering':['-month','category']},
        ),
        migrations.AddConstraint(
            model_name='budget',
            constraint=models.UniqueConstraint(fields=('user','month','category'), name='unique_user_month_category_budget'),
        ),
    ]
