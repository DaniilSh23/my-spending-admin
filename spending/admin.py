from django.contrib import admin

from spending.models import ProjectSettings, BotUsers, SpendingCategory, Spending


@admin.register(ProjectSettings)
class ProjectSettingsAdmin(admin.ModelAdmin):
    """
    Регистрация в админке модели для настроек
    """
    list_display = ('key', 'value')
    list_display_links = ('key', 'value')


@admin.register(BotUsers)
class BotUsersAdmin(admin.ModelAdmin):
    """
    Регистрация в админке модели BotUsers
    """
    list_display = (
        'pk',
        'tlg_id',
        'tlg_username',
        'first_name',
        'last_name',
        'start_at',
    )
    list_display_links = (
        'pk',
        'tlg_id',
        'tlg_username',
        'first_name',
        'last_name',
        'start_at',
    )
    search_fields = (
        'pk',
        'tlg_id',
        'tlg_username',
        'first_name',
        'last_name',
        'start_at',
    )
    search_help_text = 'Поиск по полям данной таблицы'


@admin.register(SpendingCategory)
class SpendingCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    list_display_links = (
        'id',
        'name',
    )


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'bot_user',
        'amount',
        'category',
        'description',
        'created_at',
    )
    list_display_links = (
        'id',
        'bot_user',
        'amount',
        'category',
        'description',
        'created_at',
    )
