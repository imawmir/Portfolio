from django.db import models



#COURSE
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.CharField(max_length=10)
    end_date = models.CharField(max_length=10)
    image = models.ImageField(upload_to='course', null=True, blank=True)

    def __str__(self):
        return self.title


#ENROLL
class Enroll(models.Model):
    course = models.CharField(max_length=255, null=False)
    firstname = models.CharField(max_length=60, null=False)
    lastname = models.CharField(max_length=60, null=False)
    student_number = models.CharField(max_length=10, null=False)
    phone = models.CharField(max_length=14, null=False)
    major = models.CharField(max_length=255, null=True)
    enrolled_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname
    
    
# NEWS
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news', null=True, blank=True)

    def __str__(self):
        return self.title


