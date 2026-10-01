from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image
from rest_framework import serializers

from .serializers import MAX_IMAGE_SIZE, ProduitAdminSerializer


class ProduitImageValidationTests(SimpleTestCase):
    def setUp(self):
        self.serializer = ProduitAdminSerializer()

    def test_accepts_a_valid_png(self):
        content = BytesIO()
        Image.new("RGB", (16, 16), "red").save(content, format="PNG")
        image = SimpleUploadedFile("produit.png", content.getvalue(), content_type="image/png")

        self.assertEqual(self.serializer.validate_image(image), image)

    def test_rejects_a_file_that_is_not_an_image(self):
        image = SimpleUploadedFile("faux.png", b"not an image", content_type="image/png")

        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_image(image)

    def test_rejects_an_image_larger_than_five_mebibytes(self):
        image = SimpleUploadedFile(
            "trop-grand.jpg",
            b"x" * (MAX_IMAGE_SIZE + 1),
            content_type="image/jpeg",
        )

        with self.assertRaises(serializers.ValidationError):
            self.serializer.validate_image(image)
