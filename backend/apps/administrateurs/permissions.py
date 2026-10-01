from rest_framework.permissions import SAFE_METHODS, BasePermission

class EstSuperAdmin(BasePermission):
    message = "Cette action est réservée au Super Administrateur."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.role == "super_admin"
        )

class PeutGererMenu(BasePermission):
    """Gérant ou Super Admin : écriture. 'personnel' : lecture seule."""
    message = "Seuls un Gérant ou un Super Administrateur peuvent modifier le menu."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.role in ("gerant", "super_admin"))
