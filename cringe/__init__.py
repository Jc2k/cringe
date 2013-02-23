from .meta import patch_gi
from .glib import patch_glib

def patch_all():
    patch_gi()
    patch_glib()

