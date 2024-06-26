# Generated by Django 4.2.9 on 2024-04-27 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChartsOfAccount",
            fields=[
                (
                    "code",
                    models.CharField(max_length=10, primary_key=True, serialize=False),
                ),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("KB", "Kas & Bank"),
                            ("PU", "Piutang Usaha"),
                            ("Per", "Persediaan"),
                            ("ALL", "Aset Lancar Lainnya"),
                            ("AT", "Aset Tetap"),
                            ("AP", "Akumulasi Penyusutan"),
                            ("AL", "Aset Lainnya"),
                            ("UU", "Utang Usaha"),
                            ("LJPe", "Liabilitas Jangka Pendek"),
                            ("LJPa", "Liabilitas Jangka Panjang"),
                            ("M", "Modal"),
                            ("Pen", "Pendapatan"),
                            ("BPP", "Beban Pokok Penjualan"),
                            ("B", "Beban"),
                            ("BL", "Beban Lainnya"),
                            ("PL", "Pendapatan Lainnya"),
                        ],
                        max_length=4,
                    ),
                ),
                ("account_name", models.CharField(max_length=100)),
                ("balance", models.IntegerField(default=0, null=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "parent_account",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="charts_of_account.chartsofaccount",
                    ),
                ),
            ],
        ),
    ]
