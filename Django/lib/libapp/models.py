from django.db import models


class tableColumn(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)
    rollno = models.CharField(unique=True,null=False,max_length=20,)

    class Meta:
        db_table = 'student'
        
class studentLogInDetails(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    rollno = models.CharField(max_length=50)
    intime = models.DateTimeField()
    outtime = models.DateTimeField()

    class Meta:
        db_table = 'studentLogInDetails'
