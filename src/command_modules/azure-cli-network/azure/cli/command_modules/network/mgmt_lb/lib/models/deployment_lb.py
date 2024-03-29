#pylint: skip-file
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DeploymentLb(Model):
    """
    Deployment operation parameters.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar uri: URI referencing the template. Default value:
     "https://azuresdkci.blob.core.windows.net/templatehost/CreateLb_2016-07-19/azuredeploy.json"
     .
    :vartype uri: str
    :param content_version: If included it must match the ContentVersion in
     the template.
    :type content_version: str
    :ivar _artifacts_location: Container URI of of the template. Default
     value:
     "https://azuresdkci.blob.core.windows.net/templatehost/CreateLb_2016-07-19"
     .
    :vartype _artifacts_location: str
    :param backend_pool_name: Name of load balancer backend pool.
    :type backend_pool_name: str
    :param dns_name_type: Associate VMs with a public IP address to a DNS
     name. Possible values include: 'none', 'new'. Default value: "none" .
    :type dns_name_type: str or :class:`dnsNameType
     <lbcreationclient.models.dnsNameType>`
    :param frontend_ip_name: Name of the frontend IP configuration. Default
     value: "LoadBalancerFrontEnd" .
    :type frontend_ip_name: str
    :param load_balancer_name: Name for load balancer.
    :type load_balancer_name: str
    :param location: Location for load balancer resource.
    :type location: str
    :param private_ip_address: Static private IP address to use.
    :type private_ip_address: str
    :param private_ip_address_allocation: Private IP address allocation
     method. Possible values include: 'dynamic', 'static'. Default value:
     "dynamic" .
    :type private_ip_address_allocation: str or
     :class:`privateIpAddressAllocation
     <lbcreationclient.models.privateIpAddressAllocation>`
    :param public_ip_address: Name or ID of the public IP address to use.
    :type public_ip_address: str
    :param public_ip_address_allocation: Public IP address allocation method.
     Possible values include: 'dynamic', 'static'. Default value: "dynamic" .
    :type public_ip_address_allocation: str or
     :class:`publicIpAddressAllocation
     <lbcreationclient.models.publicIpAddressAllocation>`
    :param public_ip_address_type: Type of Public IP Address to associate
     with the load balancer. Possible values include: 'none', 'new',
     'existingName', 'existingId'. Default value: "new" .
    :type public_ip_address_type: str or :class:`publicIpAddressType
     <lbcreationclient.models.publicIpAddressType>`
    :param public_ip_dns_name: Globally unique DNS Name for the Public IP
     used to access the Virtual Machine (new public IP only).
    :type public_ip_dns_name: str
    :param subnet: The subnet name or ID to associate with the load balancer.
     Cannot be used in conjunction with a Public IP.
    :type subnet: str
    :param subnet_address_prefix: The subnet address prefix in CIDR format
     (new subnet only). Default value: "10.0.0.0/24" .
    :type subnet_address_prefix: str
    :param subnet_type: Use new, existing or no subnet. Possible values
     include: 'none', 'new', 'existingName', 'existingId'. Default value:
     "none" .
    :type subnet_type: str or :class:`subnetType
     <lbcreationclient.models.subnetType>`
    :param tags: Tags object.
    :type tags: object
    :param virtual_network_name: The VNet name containing the subnet. Cannot
     be used in conjunction with a Public IP.
    :type virtual_network_name: str
    :param vnet_address_prefix: The virtual network IP address prefix in CIDR
     format (new subnet only). Default value: "10.0.0.0/16" .
    :type vnet_address_prefix: str
    :ivar mode: Gets or sets the deployment mode. Default value:
     "Incremental" .
    :vartype mode: str
    """ 

    _validation = {
        'uri': {'required': True, 'constant': True},
        '_artifacts_location': {'required': True, 'constant': True},
        'load_balancer_name': {'required': True},
        'mode': {'required': True, 'constant': True},
    }

    _attribute_map = {
        'uri': {'key': 'properties.templateLink.uri', 'type': 'str'},
        'content_version': {'key': 'properties.templateLink.contentVersion', 'type': 'str'},
        '_artifacts_location': {'key': 'properties.parameters._artifactsLocation.value', 'type': 'str'},
        'backend_pool_name': {'key': 'properties.parameters.backendPoolName.value', 'type': 'str'},
        'dns_name_type': {'key': 'properties.parameters.dnsNameType.value', 'type': 'dnsNameType'},
        'frontend_ip_name': {'key': 'properties.parameters.frontendIpName.value', 'type': 'str'},
        'load_balancer_name': {'key': 'properties.parameters.loadBalancerName.value', 'type': 'str'},
        'location': {'key': 'properties.parameters.location.value', 'type': 'str'},
        'private_ip_address': {'key': 'properties.parameters.privateIpAddress.value', 'type': 'str'},
        'private_ip_address_allocation': {'key': 'properties.parameters.privateIpAddressAllocation.value', 'type': 'privateIpAddressAllocation'},
        'public_ip_address': {'key': 'properties.parameters.publicIpAddress.value', 'type': 'str'},
        'public_ip_address_allocation': {'key': 'properties.parameters.publicIpAddressAllocation.value', 'type': 'publicIpAddressAllocation'},
        'public_ip_address_type': {'key': 'properties.parameters.publicIpAddressType.value', 'type': 'publicIpAddressType'},
        'public_ip_dns_name': {'key': 'properties.parameters.publicIpDnsName.value', 'type': 'str'},
        'subnet': {'key': 'properties.parameters.subnet.value', 'type': 'str'},
        'subnet_address_prefix': {'key': 'properties.parameters.subnetAddressPrefix.value', 'type': 'str'},
        'subnet_type': {'key': 'properties.parameters.subnetType.value', 'type': 'subnetType'},
        'tags': {'key': 'properties.parameters.tags.value', 'type': 'object'},
        'virtual_network_name': {'key': 'properties.parameters.virtualNetworkName.value', 'type': 'str'},
        'vnet_address_prefix': {'key': 'properties.parameters.vnetAddressPrefix.value', 'type': 'str'},
        'mode': {'key': 'properties.mode', 'type': 'str'},
    }

    uri = "https://azuresdkci.blob.core.windows.net/templatehost/CreateLb_2016-07-19/azuredeploy.json"

    _artifacts_location = "https://azuresdkci.blob.core.windows.net/templatehost/CreateLb_2016-07-19"

    mode = "Incremental"

    def __init__(self, load_balancer_name, content_version=None, backend_pool_name=None, dns_name_type="none", frontend_ip_name="LoadBalancerFrontEnd", location=None, private_ip_address=None, private_ip_address_allocation="dynamic", public_ip_address=None, public_ip_address_allocation="dynamic", public_ip_address_type="new", public_ip_dns_name=None, subnet=None, subnet_address_prefix="10.0.0.0/24", subnet_type="none", tags=None, virtual_network_name=None, vnet_address_prefix="10.0.0.0/16"):
        self.content_version = content_version
        self.backend_pool_name = backend_pool_name
        self.dns_name_type = dns_name_type
        self.frontend_ip_name = frontend_ip_name
        self.load_balancer_name = load_balancer_name
        self.location = location
        self.private_ip_address = private_ip_address
        self.private_ip_address_allocation = private_ip_address_allocation
        self.public_ip_address = public_ip_address
        self.public_ip_address_allocation = public_ip_address_allocation
        self.public_ip_address_type = public_ip_address_type
        self.public_ip_dns_name = public_ip_dns_name
        self.subnet = subnet
        self.subnet_address_prefix = subnet_address_prefix
        self.subnet_type = subnet_type
        self.tags = tags
        self.virtual_network_name = virtual_network_name
        self.vnet_address_prefix = vnet_address_prefix
