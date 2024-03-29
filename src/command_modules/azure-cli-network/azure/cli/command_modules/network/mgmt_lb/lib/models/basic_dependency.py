#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BasicDependency(Model):
    """
    Deployment dependency information.

    :param id: Gets or sets the ID of the dependency.
    :type id: str
    :param resource_type: Gets or sets the dependency resource type.
    :type resource_type: str
    :param resource_name: Gets or sets the dependency resource name.
    :type resource_name: str
    """ 

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'resource_type': {'key': 'resourceType', 'type': 'str'},
        'resource_name': {'key': 'resourceName', 'type': 'str'},
    }

    def __init__(self, id=None, resource_type=None, resource_name=None):
        self.id = id
        self.resource_type = resource_type
        self.resource_name = resource_name
