#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DeploymentPublicIp(Model):
    """
    Deployment operation parameters.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar uri: URI referencing the template. Default value:
     "https://azuresdkci.blob.core.windows.net/templatehost/CreatePublicIp_2016-07-19/azuredeploy.json"
     .
    :vartype uri: str
    :param content_version: If included it must match the ContentVersion in
     the template.
    :type content_version: str
    :ivar _artifacts_location: Container URI of of the template. Default
     value:
     "https://azuresdkci.blob.core.windows.net/templatehost/CreatePublicIp_2016-07-19"
     .
    :vartype _artifacts_location: str
    :param allocation_method: IP address Allocation method. Possible values
     include: 'dynamic', 'static'. Default value: "dynamic" .
    :type allocation_method: str or :class:`allocationMethod
     <publicipcreationclient.models.allocationMethod>`
    :param dns_name: Globally unique DNS entry.
    :type dns_name: str
    :param dns_name_type: Whether to include a DNS entry or not. Possible
     values include: 'new', 'none'. Default value: "none" .
    :type dns_name_type: str or :class:`dnsNameType
     <publicipcreationclient.models.dnsNameType>`
    :param location: Location (e.g. eastus).
    :type location: str
    :param name: Name of the Public IP address.
    :type name: str
    :param tags: Tags object.
    :type tags: object
    :ivar mode: Gets or sets the deployment mode. Default value:
     "Incremental" .
    :vartype mode: str
    """ 

    _validation = {
        'uri': {'required': True, 'constant': True},
        '_artifacts_location': {'required': True, 'constant': True},
        'name': {'required': True},
        'mode': {'required': True, 'constant': True},
    }

    _attribute_map = {
        'uri': {'key': 'properties.templateLink.uri', 'type': 'str'},
        'content_version': {'key': 'properties.templateLink.contentVersion', 'type': 'str'},
        '_artifacts_location': {'key': 'properties.parameters._artifactsLocation.value', 'type': 'str'},
        'allocation_method': {'key': 'properties.parameters.allocationMethod.value', 'type': 'allocationMethod'},
        'dns_name': {'key': 'properties.parameters.dnsName.value', 'type': 'str'},
        'dns_name_type': {'key': 'properties.parameters.dnsNameType.value', 'type': 'dnsNameType'},
        'location': {'key': 'properties.parameters.location.value', 'type': 'str'},
        'name': {'key': 'properties.parameters.name.value', 'type': 'str'},
        'tags': {'key': 'properties.parameters.tags.value', 'type': 'object'},
        'mode': {'key': 'properties.mode', 'type': 'str'},
    }

    uri = "https://azuresdkci.blob.core.windows.net/templatehost/CreatePublicIp_2016-07-19/azuredeploy.json"

    _artifacts_location = "https://azuresdkci.blob.core.windows.net/templatehost/CreatePublicIp_2016-07-19"

    mode = "Incremental"

    def __init__(self, name, content_version=None, allocation_method="dynamic", dns_name=None, dns_name_type="none", location=None, tags=None):
        self.content_version = content_version
        self.allocation_method = allocation_method
        self.dns_name = dns_name
        self.dns_name_type = dns_name_type
        self.location = location
        self.name = name
        self.tags = tags
