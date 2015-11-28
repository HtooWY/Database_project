from django.db import models

# Create your models here.
class faculty(models.Model):
    fid = models.CharField(max_length=9, primary_key=True)
    fname = models.CharField(max_length=60)
    def __unicode__(self):
        return u'%s' % (self.fname)
        
class course(models.Model):
    cid = models.CharField(max_length=9, primary_key=True)
    cname = models.CharField(max_length=60)
    credits = models.IntegerField()
    def __unicode__(self):
        return u'%s' % (self.cname)
        
class teach(models.Model):
    tid = models.CharField(max_length=9, primary_key=True)
    cid = models.ForeignKey(course, db_column='cid')
    fid = models.ForeignKey(faculty, db_column='fid')
    semester = models.CharField(max_length=6)
    year = models.IntegerField()
    enrollment = models.IntegerField()
    capacity = models.IntegerField()
    def __unicode__(self):
        return u'%s, %s' % (self.tid, self.enrollment)