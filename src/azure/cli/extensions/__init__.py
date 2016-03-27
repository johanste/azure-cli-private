from .query import register as register_query
from .transform import register as register_transform
from .completers import register as register_completers

def register_extensions(application):
    register_query(application)
    register_transform(application)
    register_completers(application)    