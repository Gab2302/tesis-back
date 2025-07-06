from rest_framework import serializers
from .models import User, Profile, PatientNutritionist, Scan, Task, Recipe, ScanRecipeSuggestion, ProgressLog
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Agrega el user_id y otros datos que quieras retornar
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['role'] = self.user.role
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password', 'role', 'nutritionist_code']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
    def validate(self, data):
        goal = data.get('goal_type')
        weight = data.get('weight_kg')
        desired = data.get('desired_weight_kg')
        height = data.get('height_cm')
        speed = data.get('goal_speed')

        # Verificar que los valores necesarios estén presentes
        if goal is None or weight is None or desired is None:
            raise serializers.ValidationError("Faltan datos necesarios para validar el perfil.")

        # Validación lógica según el tipo de meta
        if goal == 'ganar' and desired <= weight:
            raise serializers.ValidationError("Para ganar peso, el peso deseado debe ser mayor al actual.")
        if goal == 'perder' and desired >= weight:
            raise serializers.ValidationError("Para perder peso, el peso deseado debe ser menor al actual.")
        if goal == 'mantener' and desired != weight:
            raise serializers.ValidationError("Para mantener el peso, el peso deseado debe ser igual al actual.")

        # Validación para evitar seleccionar velocidad si la meta es mantener
        if goal == 'mantener' and speed:
            raise serializers.ValidationError("No se debe seleccionar una velocidad para mantener el peso.")

        # Validación IMC mínimo (no permitir perder peso si ya tiene bajo peso)
        if goal == 'perder' and weight and height:
            try:
                height_m = float(height) / 100
                imc = float(weight) / (height_m ** 2)
                if imc < 18.5:
                    raise serializers.ValidationError(
                        "Tu IMC actual es bajo. No puedes seleccionar 'Perder peso'."
                    )
            except (ValueError, ZeroDivisionError):
                raise serializers.ValidationError("Error al calcular el IMC. Verifica estatura y peso.")

        return data

class PatientNutritionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientNutritionist
        fields = '_all_'

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '_all_'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '_all_'

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '_all_'

class ScanRecipeSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanRecipeSuggestion
        fields = '_all_'

class ProgressLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgressLog
        fields = '_all_'