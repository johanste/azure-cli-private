#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------
#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ProviderResourceType(Model):
    """
    Resource type managed by the resource provider.

    :param resource_type: Gets or sets the resource type.
    :type resource_type: str
    :param locations: Gets or sets the collection of locations where this
     resource type can be created in.
    :type locations: list of str
    :param api_versions: Gets or sets the api version.
    :type api_versions: list of str
    :param properties: Gets or sets the properties.
    :type properties: dict
    """ 

    _attribute_map = {
        'resource_type': {'key': 'resourceType', 'type': 'str'},
        'locations': {'key': 'locations', 'type': '[str]'},
        'api_versions': {'key': 'apiVersions', 'type': '[str]'},
        'properties': {'key': 'properties', 'type': '{str}'},
    }

    def __init__(self, resource_type=None, locations=None, api_versions=None, properties=None):
        self.resource_type = resource_type
        self.locations = locations
        self.api_versions = api_versions
        self.properties = properties
