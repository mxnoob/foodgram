from rest_framework import serializers
from rest_framework.reverse import reverse

from shortener.models import LinkMapped


class ShortenerSerializer(serializers.ModelSerializer):
    """Сериализатор коротких ссылок"""

    class Meta:
        model = LinkMapped
        fields = ('original_url',)
        write_only_fields = ('original_url',)

    def get_short_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(
            reverse('shortener:load_url', args=[obj.url_hash])
        )

    def create(self, validated_data):
        original_url = validated_data.get('original_url')
        try:
            return LinkMapped.objects.get(original_url=original_url)
        except LinkMapped.DoesNotExist:
            return super().create(validated_data)

    def to_representation(self, instance):
        return {'short-link': self.get_short_link(instance)}
