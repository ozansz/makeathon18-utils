from django.db import models
from django.contrib.auth.models import User

__all__ = [
    'GeographicRegion',
    'Location',
    'Node',
    'Light',
    'DensityRecord'
]

class GeographicRegion(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'geographicregions'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<GeographicRegion(id={id}, name={name})>".format(id=self.id,
                                                                 name=self.name)

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    region = models.ForeignKey(
        GeographicRegion,
        on_delete=models.CASCADE,
        related_name='locations'
    )

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Location(id={id}, latitude={lat}, longitude={long}, region_id={rid})>".format(
            id=self.id, lat=self.latitude, long=self.longitude,
            rid=self.region_id
        )

class Node(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='nodes'
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='node'
    )

    class Meta:
        db_table = 'nodes'

    @property
    def name(self):
        return self.user.username

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Node(id={id}, location_id={lid}, user_id={uid})>".format(
            id=self.id, lid=self.location_id, uid=self.user_id
        )

class Light(models.Model):
    LIGHT_STATES = (
        ('R', 'Red'),
        ('Y', 'Yellow'),
        ('G', 'Green')
    )

    current_state = models.CharField(max_length=64, choices=LIGHT_STATES,
                                     default='R')
    node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='lights'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='lights'
    )

    class Meta:
        db_table = 'lights'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<Light(id={id}, current_state={state}, node_id={nid}, location_id={lid})>".format(
            id=self.id, state=self.current_state, nid=self.node_id,
            lid=self.location_id
        )

class DensityRecord(models.Model):
    density = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name='density_records'
    )

    class Meta:
        db_table = 'densityrecords'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<DensityRecord(id={id}, density={d}, timestamp={t}, node_id={nid})>".format(
            id=self.id, d=self.density, t=self.timestamp,
            nid=self.node_id
        )

get_register_eligible_models = lambda : [globals()[model] for model in __all__]
