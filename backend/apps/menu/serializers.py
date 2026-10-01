from PIL import Image, UnidentifiedImageError
from rest_framework import serializers

from .models import Categorie, Menu, Produit


MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MiB
MAX_IMAGE_PIXELS = 16_000_000
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}


class ProduitImageValidationMixin:
    def validate_image(self, image):
        if image.size > MAX_IMAGE_SIZE:
            raise serializers.ValidationError("L'image ne doit pas dépasser 5 Mo.")

        content_type = getattr(image, "content_type", None)
        if content_type and content_type.lower() not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise serializers.ValidationError("Formats acceptés : JPEG, PNG ou WebP.")

        try:
            image.seek(0)
            with Image.open(image) as opened_image:
                image_format = opened_image.format
                width, height = opened_image.size
                opened_image.verify()
        except (UnidentifiedImageError, OSError, ValueError):
            raise serializers.ValidationError("Le fichier envoyé n'est pas une image valide.")
        finally:
            image.seek(0)

        if image_format not in ALLOWED_IMAGE_FORMATS:
            raise serializers.ValidationError("Formats acceptés : JPEG, PNG ou WebP.")
        if width * height > MAX_IMAGE_PIXELS:
            raise serializers.ValidationError("La résolution de l'image est trop élevée.")
        return image


class ProduitSerializer(ProduitImageValidationMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)

    class Meta:
        model = Produit
        fields = ("id", "nom", "description", "prix", "image", "photo", "disponible")


class CategorieSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    produits = ProduitSerializer(many=True, read_only=True)

    class Meta:
        model = Categorie
        fields = ("id", "nom", "description", "image", "ordre_affichage", "produits")


class MenuFormuleSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    produits = ProduitSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ("id", "nom", "description", "prix", "date_debut", "date_fin", "produits")


class CategorieAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    nombre_produits = serializers.IntegerField(source="produits.count", read_only=True)

    class Meta:
        model = Categorie
        fields = ["id", "nom", "description", "ordre_affichage", "image", "nombre_produits"]

    def create(self, validated_data):
        from apps.restaurant.models import Restaurant
        restaurant = validated_data.pop("restaurant", None) or Restaurant.instance()
        return Categorie.objects.create(restaurant=restaurant, **validated_data)


class ProduitAdminSerializer(ProduitImageValidationMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    categorie_id = serializers.SlugRelatedField(source="categorie", slug_field="uuid", queryset=Categorie.objects.all(), write_only=True)
    categorie_nom = serializers.CharField(source="categorie.nom", read_only=True)

    class Meta:
        model = Produit
        fields = ["id", "nom", "description", "prix", "image", "photo", "disponible", "categorie_id", "categorie_nom", "date_creation", "date_modification"]

    def create(self, validated_data):
        categorie = validated_data.pop("categorie")
        return Produit.objects.create(categorie=categorie, **validated_data)

    def update(self, instance, validated_data):
        old_image = instance.image
        updated_instance = super().update(instance, validated_data)
        if old_image and old_image.name != updated_instance.image.name:
            old_image.storage.delete(old_image.name)
        return updated_instance


class MenuAdminSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    produit_ids = serializers.SlugRelatedField(source="produits", slug_field="uuid", queryset=Produit.objects.all(), write_only=True, many=True, required=False)
    produits = ProduitSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ["id", "nom", "description", "prix", "date_debut", "date_fin", "disponible", "produit_ids", "produits"]

    def create(self, validated_data):
        from apps.restaurant.models import Restaurant
        produits = validated_data.pop("produits", [])
        restaurant = validated_data.pop("restaurant", None) or Restaurant.instance()
        menu = Menu.objects.create(restaurant=restaurant, **validated_data)
        menu.produits.set(produits)
        return menu

    def update(self, instance, validated_data):
        produits = validated_data.pop("produits", None)
        instance = super().update(instance, validated_data)
        if produits is not None:
            instance.produits.set(produits)
        return instance


class ProduitDetailSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="uuid", read_only=True)
    categorie = serializers.SerializerMethodField()

    class Meta:
        model = Produit
        fields = ["id", "nom", "description", "prix", "image", "photo", "disponible", "categorie", "date_modification"]

    def get_categorie(self, produit):
        return {"id": str(produit.categorie.uuid), "nom": produit.categorie.nom}
