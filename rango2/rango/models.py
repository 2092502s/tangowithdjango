from django.db import models
from django.template.defaultfilters import slugify

#Basically, this defines a Category-class as a subclass of another
#class called "Model" inside Django. The name-field basically inherits
#the field inside Model that stores character data, and parameters are
#specified.

class Category(models.Model):
    name = models.CharField( max_length=128, unique=True)
    views = models.IntegerField(default=0)  #added afterwards
    likes = models.IntegerField(default=0)  #added afterwards
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)
    #Every category must be unique. 

    def __unicode__(self):
        return self.name
    #An associated function that is conventional to define.
    #Provides unicode representation.

class Page(models.Model):
    category = models.ForeignKey(Category)
    #Basically, it references a Category object
    title = models.CharField(max_length = 128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title
    #Not sure what it does.
