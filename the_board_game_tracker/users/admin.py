from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from the_board_game_tracker.users.forms import (
    UserAdminChangeForm,
    UserAdminCreationForm,
)

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Important dates"),
            {"fields": ("replayed_game_date", "last_login", "date_joined")},
        ),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_visible",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = ["username", "name", "is_superuser", "is_visible"]
    search_fields = ["name"]
    actions = ["hide_players", "show_players"]

    @admin.action(description="Hide users from the leaderboard")
    def hide_players(self, request, queryset):
        queryset.update(is_visible=False)

    @admin.action(description="Show users on the leaderboard")
    def show_players(self, request, queryset):
        queryset.update(is_visible=True)
