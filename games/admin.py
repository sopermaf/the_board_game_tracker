from django.contrib import admin, messages
from django.utils.translation import ngettext

from .forms import BoardGameForm, GameCategoryForm, PlayedBoardGameForm
from .models import BoardGame, BoardGameTag, PlayedBoardGame


@admin.register(PlayedBoardGame)
class PlayedBoardGameAdmin(admin.ModelAdmin):
    list_display = ["board_game", "played_by", "date_played"]
    search_fields = ["board_game__name"]
    list_filter = ["played_by"]
    list_per_page = 10
    form = PlayedBoardGameForm


class PlayedGameInline(admin.TabularInline):
    model = PlayedBoardGame
    extra = 0


class HasImageFilter(admin.SimpleListFilter):
    title = "has_image"
    parameter_name = "has_image"

    def lookups(self, request, model_admin):
        return (
            ("Yes", "Yes"),
            ("No", "No"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "Yes":
            return queryset.exclude(image_src__isnull=True)
        elif value == "No":
            return queryset.filter(image_src__isnull=True)
        return queryset


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "game_weight",
        "range_of_players",
        "game_duration_mins",
        "price",
        "has_image",
    ]
    list_filter = [HasImageFilter]
    list_per_page = 20
    search_fields = ["name"]
    form = BoardGameForm
    inlines = [PlayedGameInline]
    actions = ["scrape_boardgamegeek_images"]

    @admin.action(description="Scrape boardgamegeek image sources")
    def scrape_boardgamegeek_images(self, request, queryset):
        # TODO: reimplement as a background job to ensure the request
        # does not time out
        updated = []
        for game in queryset:
            game.image_src = game.scrape_boardgamegeek_img_src()
            game.save()
            updated.append(game)

        self.message_user(
            request,
            ngettext(
                "%d story was successfully marked as published.",
                "%d stories were successfully marked as published.",
                len(updated),
            )
            % len(updated),
            messages.SUCCESS,
        )

    def has_image(self, obj):
        return bool(obj.image_src)

    has_image.boolean = True


@admin.register(BoardGameTag)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = GameCategoryForm
