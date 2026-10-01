from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Administrateur


class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Administrateur
        fields = ["id", "nom", "prenom", "email", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        return Administrateur.objects.create_user(password=password, **validated_data)


class ConnexionSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        user = Administrateur.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("Email ou mot de passe incorrect.")
        if user.statut != "actif":
            raise serializers.ValidationError(
                "Ce compte n'est pas actif (en attente de validation ou désactivé). "
                "Contacte un Super Administrateur."
            )

        data = super().validate(attrs)
        data["administrateur"] = AdministrateurSerializer(user).data
        return data


class AdministrateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ["id", "nom", "prenom", "email", "role", "statut", "date_creation"]


class AdministrateurGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ["id", "nom", "prenom", "email", "role", "statut", "date_creation"]
        read_only_fields = ["date_creation"]

    def validate_role(self, value):
        if self.instance and self.instance.role == "super_admin" and value != "super_admin":
            autres = Administrateur.objects.filter(role="super_admin", statut="actif").exclude(pk=self.instance.pk)
            if not autres.exists():
                raise serializers.ValidationError("Impossible de retirer le rôle Super Administrateur : c'est le dernier compte actif avec ce rôle.")
        return value

    def validate_statut(self, value):
        if self.instance and self.instance.role == "super_admin" and value == "inactif":
            autres = Administrateur.objects.filter(role="super_admin", statut="actif").exclude(pk=self.instance.pk)
            if not autres.exists():
                raise serializers.ValidationError("Impossible de désactiver le dernier Super Administrateur actif.")
        return value


class AdministrateurCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Administrateur
        fields = ["id", "nom", "prenom", "email", "password", "role"]
        extra_kwargs = {"role": {"required": False}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.setdefault("statut", "actif")
        return Administrateur.objects.create_user(password=password, **validated_data)
