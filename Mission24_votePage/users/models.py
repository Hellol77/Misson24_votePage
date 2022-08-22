from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .choice import *

class UserManager(BaseUserManager):
    def create_user(self, user_id, password, university, role):
        user = self.model(
            user_id = user_id,
            university = university,
            role = role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password):
        user = self.create_user(user_id, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    
    objects = UserManager()

    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    password = models.CharField(max_length=256, verbose_name="비밀번호")
    university = models.CharField(choices=UNIVERSITY_CHOICES, max_length=24, verbose_name="학교", null=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=24, verbose_name="역할", null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = "회원목록"
        verbose_name = "사용자"
        verbose_name_plural = "사용자"

class PostResult(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='아이디')
    team_name = models.CharField(max_length=17, verbose_name="팀명", blank=True, null=True)
    team_members = models.CharField(max_length=30, verbose_name="팀원", blank=True, null=True)
    intro_text = models.CharField(max_length=100, verbose_name="한줄소개", blank=True, null=True)

    image1 = models.ImageField(upload_to='images/',verbose_name='이미지1', blank=True, null=True)
    imagesrc1 = models.CharField(max_length=40, verbose_name='이미지1 주소', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/',verbose_name='이미지2', blank=True, null=True)
    imagesrc2 = models.CharField(max_length=40, verbose_name='이미지2 주소', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/',verbose_name='이미지3', blank=True, null=True)
    imagesrc3 = models.CharField(max_length=40, verbose_name='이미지3 주소', blank=True, null=True)
    image4 = models.ImageField(upload_to='images/',verbose_name='이미지4', blank=True, null=True)
    imagesrc4 = models.CharField(max_length=40, verbose_name='이미지4 주소', blank=True, null=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'PostResult'
        verbose_name = 'PostResult'
        verbose_name_plural = 'PostResult'