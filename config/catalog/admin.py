from django.contrib import admin
from .models import Game, Genre, GameImage


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class GameImageInline(admin.TabularInline):
    model = GameImage
    extra = 1
    fields = ("image", "alt_text", "is_main")

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "genre")
    search_fields = ("name",)
    inlines = [GameImageInline]