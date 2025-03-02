# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('ProfileUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



class ProfileUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    id = models.UUIDField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'profile_user'


class ProfileProfile(models.Model):
    id = models.UUIDField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    tg_nick = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    date_of_birth = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    token = models.CharField(max_length=50)
    user = models.OneToOneField('ProfileUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_profile'



class ProfileEducationuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    college = models.TextField()
    speciality = models.TextField()
    year_of_study = models.CharField(max_length=50)
    link = models.CharField(max_length=200)
    user = models.ForeignKey('ProfileProfile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_educationuser'


class ProfilePersonalquality(models.Model):
    id = models.BigAutoField(primary_key=True)
    quality = models.TextField()
    link = models.CharField(max_length=200)
    user = models.OneToOneField('ProfileProfile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_personalquality'


class ProfilePersonalqualityvalidator(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'profile_personalqualityvalidator'


class ProfilePlaceofworkuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    company = models.TextField()
    position = models.TextField()
    work_period = models.CharField(max_length=50)
    user = models.ForeignKey('ProfileProfile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_placeofworkuser'


class ProfileProfilevalidator(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'profile_profilevalidator'


class ProfileUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(ProfileUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_user_groups'
        unique_together = (('user', 'group'),)


class ProfileUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(ProfileUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ProfileUseravatar(models.Model):
    id = models.BigAutoField(primary_key=True)
    avatar = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()
    user = models.OneToOneField(ProfileProfile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_useravatar'


class ProfileUserskill(models.Model):
    id = models.BigAutoField(primary_key=True)
    skill_name = models.CharField(max_length=100)
    skill_type = models.CharField(max_length=20)
    user = models.ForeignKey(ProfileProfile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_userskill'


class ProfileUserspecialization(models.Model):
    id = models.BigAutoField(primary_key=True)
    specialization = models.CharField(max_length=100)
    user = models.ForeignKey(ProfileProfile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'profile_userspecialization'

class ProfileVWUsProfileFull(models.Model):

    class Meta:
        managed = False
        db_table = 'profile_vw_us_profile_full'