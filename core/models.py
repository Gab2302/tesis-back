from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# ---------- MANAGER PERSONALIZADO ----------
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role='paciente'):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# ---------- MODELO DE USUARIO ----------
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [('paciente', 'Paciente'), ('nutricionista', 'Nutricionista')]
    
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    nutritionist_code = models.CharField(max_length=12, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email

# ---------- DEMÁS MODELOS ----------
class Profile(models.Model):
    GENDER_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    GOAL_TYPE_CHOICES = [('perder', 'Perder'), ('ganar', 'Ganar'), ('mantener', 'Mantener')]
    GOAL_SPEED_CHOICES = [('lento', 'Lento'), ('recomendado', 'Recomendado'), ('rápido', 'Rápido')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    desired_weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES, null=True, blank=True)
    goal_speed = models.CharField(max_length=15, choices=GOAL_SPEED_CHOICES, null=True, blank=True)
    daily_kcal_target = models.IntegerField(null=True, blank=True)
    daily_protein_g = models.IntegerField(null=True, blank=True)
    daily_carb_g = models.IntegerField(null=True, blank=True)
    daily_fat_g = models.IntegerField(null=True, blank=True)

class PatientNutritionist(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_links')
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nutritionist_links')
    linked_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Scan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_path = models.TextField(null=True, blank=True)
    scan_datetime = models.DateTimeField(auto_now_add=True)
    ocr_text = models.TextField(null=True, blank=True)
    openai_summary = models.TextField(null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    protein_g = models.IntegerField(null=True, blank=True)
    carb_g = models.IntegerField(null=True, blank=True)
    fat_g = models.IntegerField(null=True, blank=True)
    health_comment = models.TextField(null=True, blank=True)

class Task(models.Model):
    TASK_TYPE_CHOICES = [('receta', 'Receta'), ('ejercicio', 'Ejercicio'), ('otro', 'Otro')]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default='otro')

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image_path = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    protein_g = models.IntegerField(null=True, blank=True)
    carb_g = models.IntegerField(null=True, blank=True)
    fat_g = models.IntegerField(null=True, blank=True)
    is_validated_by_nutritionist = models.BooleanField(default=False)

class ScanRecipeSuggestion(models.Model):
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class ProgressLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    calories_consumed = models.IntegerField(null=True, blank=True)
    protein_g = models.IntegerField(null=True, blank=True)
    carb_g = models.IntegerField(null=True, blank=True)
    fat_g = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

