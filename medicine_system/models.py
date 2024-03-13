from django.db import models
import uuid

class Baseclass(models.Model):
    uuid = models.UUIDField(primary_key =True ,default = uuid.uuid4 , editable = False, unique=True)
    creted_at = models.DateField(auto_now_add = True)

    class Meta :
        abstract = True

class Medicine(models.Model):
    uuid = models.UUIDField(primary_key =True ,default = uuid.uuid4 , editable = False, unique=True)
    creted_at = models.DateField(auto_now_add = True)
    name = models.CharField(max_length = 100)
    price = models.IntegerField(default = 100)
    expiry_date = models.CharField(max_length = 50)
    medicine_type = models.CharField(max_length = 50)
    is_available = models.BooleanField(default = 0)
    weight_in_ml_or_mg = models.IntegerField(default = 50)
    use_in_disease = models.CharField(max_length = 100)

class Customer(Baseclass):
    # medicine = models.ForeignKey(Medicine , related_name = "medicine_details" , on_delete = models.CASCADE)
    name = models.CharField(max_length = 100)
    age = models.IntegerField(default = 30)
    gender = models.CharField(max_length = 10)
    address = models.CharField(max_length = 200 , default = 1)
    disease = models.CharField(max_length = 100)

    class Meta:
        db_table="customer_details"
   

    

