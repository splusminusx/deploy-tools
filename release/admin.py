from django.contrib import admin
from .models import ArtifactType, Environment, Artifact,  Release

admin.site.register(ArtifactType)
admin.site.register(Environment)


class ArtifactInline(admin.TabularInline):
    verbose_name = 'Artifacts for Release'
    model = Release.artifacts.through


class ArtifactAdmin(admin.ModelAdmin):
    list_display = ('type', 'version')


class ReleaseAdmin(admin.ModelAdmin):
    fields = ['name', 'environment', 'start_time', 'end_time', 'description']
    inlines = [ArtifactInline]
    list_display = ('name', 'environment', 'manager', 'start_time', 'end_time')

    def save_model(self, request, obj, form, change):
        obj.manager = request.user
        obj.save()


admin.site.register(Release, ReleaseAdmin)
admin.site.register(Artifact, ArtifactAdmin)
