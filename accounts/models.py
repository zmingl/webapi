from django.db import models

# Create your models here.
class Users(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    mobile = models.CharField(max_length=32)
    group_id = models.IntegerField()
    class Meta:
        db_table = "users"
        unique_together = ['user','mobile']

class Meetings(models.Model):
    founder = models.ForeignKey(Users,on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    class Meta:
        db_table = "meetings"

class Users_Meetings(models.Model):
    # meeting_id = models.IntegerField(unique=True)
    # user_id = models.IntegerField(unique=True)
    meeting = models.ForeignKey(Meetings,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)

    status = models.CharField(max_length=32)
    class Meta:
        db_table = "users_meetings"
        unique_together = ['meeting', 'user']
    
