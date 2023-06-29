from rest_framework import serializers

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # Placeholder for the stats model
        fields = '__all__'  # Include all fields of the model

    def __init__(self, *args, **kwargs):
        # Dynamically set the model and fields based on the provided stats model
        stats_model = kwargs.pop('stats_model', None)
        if stats_model:
            self.Meta.model = stats_model
        super().__init__(*args, **kwargs)

