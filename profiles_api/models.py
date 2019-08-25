from django.db import models
#########################self#######################
#these are the base classes which you need when overriding or customizing the  default
#django user model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    #Manager for User profiles

    #In django password must be given but we are not gonna follow this rule
    def create_user(self, email, name, password=None):
        #Create a new user profile
        if not email:
            raise ValueError("User must have an email address")
            #normalizing email address which makes second part of email lower case
            email=self.normalize_email(email)

            #it will create a model object that user manager is representing
            user=self.model(email=email, name=name)

            #We can't pass password as argument here because it will be passed in plain text,
            #so we use set_password function that comes with our user model(AbstractBaseUser)
            user.set_password(password)

            #To save user model and also specify database that you use but
            #it is best practice to add this line to make sure multiple databases are supported
            user.save(using=self._db)

            #retuning newly ceated user object
            return user

    def create_superuser(self, email, name, password):
        #Create and save a new super user with given details
        user=self.create_user(email, name, password)

        user.is_staff=True
        user.is_superuser=True

        user.save(using=self._db)

        return user



    #we are inheriting frm AbstractBaseUser, PermissionsMixin
    #Userprofile is table of DB
class UserProfile(AbstractBaseUser, PermissionsMixin):
    #Database model for users in the system

    #Column names
    email=models.EmailField(max_length=255, unique=True)
    name=models.CharField(max_length=255)

    #Permissions
    #user profile activated or not
    #we did not create is_superuser here because it is auto created by PermissionsMixin
    is_active=models.BooleanField(default=True)

    #to check if user is allowed to access django-admin and some other things
    is_staff=models.BooleanField(default=False)

    #Now we need to specify model manager that we’ll use for the objects and this is required so that
    #we can use our custom model with Django CLI.

    objects= UserProfileManager()
    #we have not created UserProfileManager untill now, will create in future

    #replacing default django model's username with email field and it will be required by default
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    #we interact with custom user model with these functions
    def get_full_name(self):
        #Retrieve full name of user
        return self.name

    def get_short_name(self):
        #Retrieve short name of user
        return self.name

    #Now we need string representation of our model this is the item that we wanna return when we
    #convert a UserProfile object to a string in pyhton
    def __str___(self):
         #Return string representation of user
         return self.email
