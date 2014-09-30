# coding: utf-8

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User

from rest_framework.authtoken.models import Token


class UserProfileManager(BaseUserManager):
    def create_user(self, username, password, email, role, first_name, last_name, protocol, fone_number,
                    cel_number, is_active):
        if not email:
            raise ValueError(_('The given email must be set'))

        now = timezone.now()


        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            role=role,
            first_name=first_name,
            last_name=last_name,
            date_joined=now,
            last_login=now,
            protocol=protocol,
            fone_number=fone_number,
            cel_number=cel_number,
            is_active=is_active,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        Token.objects.create(user=user)
        
        return user


class UserProfile(AbstractBaseUser):
    username = models.CharField(_('username'), max_length=180, unique=True, blank=False, )
    first_name = models.CharField(_('first_name'), max_length=100, blank=False, )
    last_name = models.CharField(_('last_name'), max_length=100, blank=False, )
    email = models.EmailField(_('email'), max_length=150, unique=True, blank=False, )
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now, )
    is_active = models.BooleanField(_('is_active'), default=True, )
    protocol = models.CharField(_('protocol'), max_length=9, blank=False, )
    fone_number = models.CharField(_('fone_number'), max_length=10, blank=True, )
    cel_number = models.CharField(_('cel_number'), max_length=10, blank=True, )
    role = models.CharField(_('role'), max_length=30, blank=False, )

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['protocol', 'email', 'first_name', 'last_name']

    class Meta:
        ordering = ('protocol',)

    def __unicode__(self):
        return self.first_name

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name


class Request(models.Model):
    STATES_OF_REQUEST = (
        ('pending', 'Pendente'),
        ('realized', 'Realizada'),
        ('canceled', 'Cancelada'),
        ('delayed', 'Atrasada'),
    )

    LEVELS_OF_PRIORITY = (
        ('low', 'Baixa'),
        ('medium', u'Médio'),
        ('high', 'Alta'),
    )

    response = models.CharField(max_length=128)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    equipment = models.CharField(max_length=128)
    nature = models.CharField(max_length=128)
    status = models.CharField(max_length=12, choices=STATES_OF_REQUEST)
    priority = models.CharField(max_length=12, choices=LEVELS_OF_PRIORITY)
    who_requested = models.ForeignKey(UserProfile, related_name='who_requested')
    who_executed = models.ForeignKey(UserProfile, related_name='who_executed')