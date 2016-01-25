from django.contrib.gis.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from ..users.models import User


class SuspicionReasons(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserWhitelist(models.Model):
    user = models.ForeignKey(User)
    whitelist_user = models.CharField(max_length=1000)

    def __str__(self):
        return '%s' % self.whitelist_user

    class Meta:
        unique_together = ('user', 'whitelist_user',)


class Changeset(models.Model):

    user = models.CharField(max_length=1000, db_index=True)
    uid = models.CharField(_('User ID'), max_length=255)
    editor = models.CharField(max_length=255)
    powerfull_editor = models.BooleanField(_('Powerfull Editor'), default=False)
    comment = models.CharField(max_length=1000, blank=True)
    source = models.CharField(max_length=1000, blank=True)
    imagery_used = models.CharField(max_length=1000, blank=True)
    date = models.DateTimeField()
    reasons = models.ManyToManyField(
        SuspicionReasons, related_name='changesets')
    create = models.IntegerField()
    modify = models.IntegerField()
    delete = models.IntegerField()
    bbox = models.PolygonField()
    is_suspect = models.BooleanField()
    harmful = models.NullBooleanField()
    checked = models.BooleanField(default=False)
    check_user = models.ForeignKey(User, blank=True, null=True)
    check_date = models.DateTimeField(null=True, blank=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def osm_link(self):
        """Return the link to the changeset page on OSM website."""
        return 'http://www.openstreetmap.org/changeset/%s' % self.id

    def achavi_link(self):
        """Return the link to the changeset page on ACHAVI."""
        return 'https://overpass-api.de/achavi/?changeset=%s' % self.id

    def josm_link(self):
        """Return link to open changeset in JOSM."""
        josm_base = "http://127.0.0.1:8111/import?url="
        changeset_url = "http://www.openstreetmap.org/api/0.6/changeset/%s/download" % self.id
        return "%s%s" % (josm_base, changeset_url,)


class Import(models.Model):
    """Class to register the import of Changesets."""
    start = models.IntegerField()
    end = models.IntegerField()
    date = models.DateTimeField(_('Date of the import'), auto_now_add=True)

    def __str__(self):
        return '%s %i - %i' % (_('Import'), self.start, self.end)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Import, self).save(*args, **kwargs)
