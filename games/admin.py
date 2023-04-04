import contextlib

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
            return queryset.exclude(image_src="")
        elif value == "No":
            return queryset.filter(image_src="")
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

    def save_model(self, request, obj: BoardGame, form, change) -> None:
        # NOTE: scrape images for newly created games within Admin
        # flow only as an easier flow compared to overriding the
        # the model save
        if not change and not obj.image_src:
            # we don't want to cause exceptions for the admin page
            with contextlib.suppress(Exception):
                obj.scrape_boardgamegeek_img_src()

        return super().save_model(request, obj, form, change)

    @admin.action(description="Scrape boardgamegeek image sources")
    def scrape_boardgamegeek_images(self, request, queryset):
        # TODO: reimplement as a background job to ensure the request
        # does not time out
        updated = []
        for game in queryset:
            game.scrape_boardgamegeek_img_src()
            updated.append(game)

        self.message_user(
            request,
            ngettext(
                "%d image was successfully scraped.",
                "%d images were successfully scraped.",
                len(updated),
            )
            % len(updated),
            messages.SUCCESS,
        )

    def has_image(self, obj: BoardGame):
        return bool(obj.image_src)

    has_image.boolean = True


@admin.register(BoardGameTag)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = GameCategoryForm
