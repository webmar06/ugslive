from django.db import models
from ugs_app.models import *
# Create your models here.

class StakeSlot(models.Model):
    user=models.OneToOneField(UserProfile, on_delete=CASCADE)
    s_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    s_name=models.CharField(default=0,max_length=50, blank=True)
    s_rate=models.IntegerField(default=0, blank=True)
    s_amount=models.IntegerField(default=0, blank=True)
    s_date=models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user.username +' - '+str(self.s_name)+' - '+str(self.s_rate))
    
class StakeLogs(models.Model):
    user=models.OneToOneField(UserProfile, on_delete=CASCADE)
    sl_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    sl_name=models.CharField(default=0,max_length=50, blank=True)
    sl_rate=models.IntegerField(default=0, blank=True)
    sl_amount=models.IntegerField(default=0, blank=True)
    sl_type=models.CharField(default=0,max_length=50, blank=True)
    sl_status=models.CharField(max_length=50,default='PENDING',choices=[('PENDING','PENDING'),('RECIEVED','RECIEVED'),('SEND','SEND')])
    sl_duration=models.IntegerField(default=0, blank=True)
    sl_date=models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user.username +' - '+str(self.sl_name)+' - '+str(self.sl_status))