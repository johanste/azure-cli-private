from azure.mgmt.network.operations import (ApplicationGatewaysOperations,
                                           ExpressRouteCircuitAuthorizationsOperations,
                                           ExpressRouteCircuitPeeringsOperations,
                                           ExpressRouteCircuitsOperations,
                                           ExpressRouteServiceProvidersOperations,
                                           LoadBalancersOperations,
                                           LocalNetworkGatewaysOperations,
                                           NetworkInterfacesOperations,
                                           NetworkSecurityGroupsOperations,
                                           PublicIPAddressesOperations,
                                           RouteTablesOperations,
                                           RoutesOperations,
                                           SecurityRulesOperations,
                                           SubnetsOperations,
                                           UsagesOperations,
                                           VirtualNetworkGatewayConnectionsOperations,
                                           VirtualNetworkGatewaysOperations,
                                           VirtualNetworksOperations)

from azure.cli.commands._command_creation import get_mgmt_service_client
from azure.cli.command_modules.network.mgmt.lib import (ResourceManagementClient as VNetClient,
                                                        ResourceManagementClientConfiguration
                                                        as VNetClientConfig)
from azure.cli.command_modules.network.mgmt.lib.operations import VNetOperations
from azure.cli.command_modules.network.custom import ConvenienceNetworkCommands
from azure.cli.command_modules.network._params import (VNET_ALIASES, SUBNET_ALIASES,
                                                       _network_client_factory)
from azure.cli.commands._auto_command import build_operation, CommandDefinition
from azure.cli.commands import CommandTable, LongRunningOperation
from azure.cli._locale import L

command_table = CommandTable()

# pylint: disable=line-too-long
# Application gateways
build_operation("network application-gateway",
                "application_gateways",
                _network_client_factory,
                [
                    CommandDefinition(ApplicationGatewaysOperations.delete, LongRunningOperation(L('Deleting application gateway'), L('Application gateway deleted')), id_parameters=('resource_group_name', 'application_gateway_name')),
                    CommandDefinition(ApplicationGatewaysOperations.get, 'ApplicationGateway', command_alias='show', id_parameters=('resource_group_name', 'application_gateway_name')),
                    CommandDefinition(ApplicationGatewaysOperations.list, '[ApplicationGateway]', id_parameters=['resource_group_name']),
                    CommandDefinition(ApplicationGatewaysOperations.list_all, '[ApplicationGateway]', id_parameters=['resource_group_name']),
                    CommandDefinition(ApplicationGatewaysOperations.start, LongRunningOperation(L('Starting application gateway'), L('Application gateway started')), id_parameters=('resource_group_name', 'application_gateway_name')),
                    CommandDefinition(ApplicationGatewaysOperations.stop, LongRunningOperation(L('Stopping application gateway'), L('Application gateway stopped')), id_parameters=('resource_group_name', 'application_gateway_name')),
                ],
                command_table)

# ExpressRouteCircuitAuthorizationsOperations
build_operation("network express-route circuit-auth",
                "express_route_circuit_authorizations",
                _network_client_factory,
                [
                    CommandDefinition(ExpressRouteCircuitAuthorizationsOperations.delete, LongRunningOperation(L('Deleting express route authorization'), L('Express route authorization deleted')), id_parameters=('resource_group_name', 'circuit_name', 'authorization_name')),
                    CommandDefinition(ExpressRouteCircuitAuthorizationsOperations.get, 'ExpressRouteCircuitAuthorization', command_alias='show', id_parameters=('resource_group_name', 'circuit_name', 'authorization_name')),
                    CommandDefinition(ExpressRouteCircuitAuthorizationsOperations.list, '[ExpressRouteCircuitAuthorization]', id_parameters=('resource_group_name', 'circuit_name')),
                ],
                command_table)

# ExpressRouteCircuitPeeringsOperations
build_operation("network express-route circuit-peering",
                "express_route_circuit_peerings",
                _network_client_factory,
                [
                    CommandDefinition(ExpressRouteCircuitPeeringsOperations.delete, LongRunningOperation(L('Deleting express route circuit peering'), L('Express route circuit peering deleted')), id_parameters=('resource_group_name', 'circuit_name', 'peering_name')),
                    CommandDefinition(ExpressRouteCircuitPeeringsOperations.get, 'ExpressRouteCircuitPeering', command_alias='show', id_parameters=('resource_group_name', 'circuit_name', 'peering_name')),
                    CommandDefinition(ExpressRouteCircuitPeeringsOperations.list, '[ExpressRouteCircuitPeering]', id_parameters=['resource_group_name']),
                ],
                command_table)

# ExpressRouteCircuitsOperations
build_operation("network express-route circuit",
                "express_route_circuits",
                _network_client_factory,
                [
                    CommandDefinition(ExpressRouteCircuitsOperations.delete, LongRunningOperation(L('Deleting express route circuit'), L('Express route circuit deleted')), id_parameters=('resource_group_name', 'circuit_name')),
                    CommandDefinition(ExpressRouteCircuitsOperations.get, 'ExpressRouteCircuit', command_alias='show', id_parameters=('resource_group_name', 'circuit_name')),
                    CommandDefinition(ExpressRouteCircuitsOperations.list_arp_table, '[ExpressRouteCircuitArpTable]', 'list-arp', id_parameters=('resource_group_name', 'circuit_name')),
                    CommandDefinition(ExpressRouteCircuitsOperations.list_routes_table, '[ExpressRouteCircuitRoutesTable]', 'list-routes', id_parameters=('resource_group_name', 'circuit_name')),
                    CommandDefinition(ExpressRouteCircuitsOperations.list_stats, '[ExpressRouteCircuitStats]', id_parameters=('resource_group_name', 'circuit_name')),
                    CommandDefinition(ExpressRouteCircuitsOperations.list, '[ExpressRouteCircuit]', id_parameters=['resource_group_name']),
                    CommandDefinition(ExpressRouteCircuitsOperations.list_all, '[ExpressRouteCircuit]'),
                ],
                command_table)

# ExpressRouteServiceProvidersOperations
build_operation("network express-route service-provider",
                "express_route_service_providers",
                _network_client_factory,
                [
                    CommandDefinition(ExpressRouteServiceProvidersOperations.list, '[ExpressRouteServiceProvider]'),
                ],
                command_table)

# LoadBalancersOperations
build_operation("network lb",
                "load_balancers",
                _network_client_factory,
                [
                    CommandDefinition(LoadBalancersOperations.delete, LongRunningOperation(L('Deleting load balancer'), L('Load balancer deleted')), id_parameters=('resource_group_name', 'load_balancer_name')),
                    CommandDefinition(LoadBalancersOperations.get, 'LoadBalancer', command_alias='show', id_parameters=('resource_group_name', 'load_balancer_name')),
                    CommandDefinition(LoadBalancersOperations.list_all, '[LoadBalancer]', id_parameters=['resource_group_name']),
                    CommandDefinition(LoadBalancersOperations.list, '[LoadBalancer]', id_parameters=['resource_group_name']),
                ],
                command_table)

# LocalNetworkGatewaysOperations
build_operation("network local-gateway",
                "local_network_gateways",
                _network_client_factory,
                [
                    CommandDefinition(LocalNetworkGatewaysOperations.get, 'LocalNetworkGateway', command_alias='show', id_parameters=('resource_group_name', 'local_network_gateway_name')),
                    CommandDefinition(LocalNetworkGatewaysOperations.delete, LongRunningOperation(L('Deleting local network gateway'), L('Local network gateway deleted')), id_parameters=('resource_group_name', 'local_network_gateway_name')),
                    CommandDefinition(LocalNetworkGatewaysOperations.list, '[LocalNetworkGateway]', id_parameters=['resource_group_name']),
                ],
                command_table)


# NetworkInterfacesOperations
build_operation("network nic",
                "network_interfaces",
                _network_client_factory,
                [
                    CommandDefinition(NetworkInterfacesOperations.delete, LongRunningOperation(L('Deleting network interface'), L('Network interface deleted')), id_parameters=('resource_group_name', 'network_interface_name')),
                    CommandDefinition(NetworkInterfacesOperations.get, 'NetworkInterface', command_alias='show', id_parameters=('resource_group_name', 'network_interface_name')),
                    CommandDefinition(NetworkInterfacesOperations.list_all, '[NetworkInterface]'),
                    CommandDefinition(NetworkInterfacesOperations.list, '[NetworkInterface]', id_parameters=['resource_group_name']),
                ],
                command_table)

# NetworkInterfacesOperations: scaleset
build_operation("network nic scale-set",
                "network_interfaces",
                _network_client_factory,
                [
                    CommandDefinition(NetworkInterfacesOperations.list_virtual_machine_scale_set_vm_network_interfaces, '[NetworkInterface]', command_alias='list-vm-nics', id_parameters=('resource_group_name', 'virtual_machine_scale_set_name')),
                    CommandDefinition(NetworkInterfacesOperations.list_virtual_machine_scale_set_network_interfaces, '[NetworkInterface]', command_alias='list', id_parameters=('resource_group_name', 'virtual_machine_scale_set_name')),
                    CommandDefinition(NetworkInterfacesOperations.get_virtual_machine_scale_set_network_interface, 'NetworkInterface', command_alias='show', id_parameters=('resource_group_name', 'virtual_machine_scale_set_name', 'virtualmachine_index', 'network_interface_name')),
                ],
                command_table)

# NetworkSecurityGroupsOperations
build_operation("network nsg",
                "network_security_groups",
                _network_client_factory,
                [
                    CommandDefinition(NetworkSecurityGroupsOperations.delete, LongRunningOperation(L('Deleting network security group'), L('Network security group deleted')), id_parameters=('resource_group_name', 'network_security_group_name')),
                    CommandDefinition(NetworkSecurityGroupsOperations.get, 'NetworkSecurityGroup', command_alias='show', id_parameters=('resource_group_name', 'network_security_group_name')),
                    CommandDefinition(NetworkSecurityGroupsOperations.list_all, '[NetworkSecurityGroup]'),
                    CommandDefinition(NetworkSecurityGroupsOperations.list, '[NetworkSecurityGroup]', id_parameters=('resource_group_name', 'network_security_group_name')),
                ],
                command_table)

# PublicIPAddressesOperations
build_operation("network public-ip",
                "public_ip_addresses",
                _network_client_factory,
                [
                    CommandDefinition(PublicIPAddressesOperations.delete, LongRunningOperation(L('Deleting public IP address'), L('Public IP address deleted')), id_parameters=('resource_group_name', 'public_ip_address_name')),
                    CommandDefinition(PublicIPAddressesOperations.get, 'PublicIPAddress', command_alias='show', id_parameters=('resource_group_name', 'public_ip_address_name')),
                    CommandDefinition(PublicIPAddressesOperations.list_all, '[PublicIPAddress]'),
                    CommandDefinition(PublicIPAddressesOperations.list, '[PublicIPAddress]', id_parameters=['resource_group_name']),
                ],
                command_table)

# RouteTablesOperations
build_operation("network route-table",
                "route_tables",
                _network_client_factory,
                [
                    CommandDefinition(RouteTablesOperations.delete, LongRunningOperation(L('Deleting route table'), L('Route table deleted')), id_parameters=('resource_group_name', 'route_table_name')),
                    CommandDefinition(RouteTablesOperations.get, 'RouteTable', command_alias='show', id_parameters=('resource_group_name', 'route_table_name')),
                    CommandDefinition(RouteTablesOperations.list, '[RouteTable]', id_parameters=['resource_group_name']),
                    CommandDefinition(RouteTablesOperations.list_all, '[RouteTable]'),
                ],
                command_table)


# RoutesOperations
build_operation("network route-operation",
                "routes",
                _network_client_factory,
                [
                    CommandDefinition(RoutesOperations.delete, LongRunningOperation(L('Deleting route'), L('Route deleted')), id_parameters=('resource_group_name', 'route_name')),
                    CommandDefinition(RoutesOperations.get, 'Route', command_alias='show', id_parameters=('resource_group_name', 'route_name')),
                    CommandDefinition(RoutesOperations.list, '[Route]', id_parameters=['resource_group_name']),
                ],
                command_table)

# SecurityRulesOperations
build_operation("network nsg-rule",
                "security_rules",
                _network_client_factory,
                [
                    CommandDefinition(SecurityRulesOperations.delete, LongRunningOperation(L('Deleting security rule'), L('Security rule deleted')), id_parameters=('resource_group_name', 'security_rule_name', 'network_security_group_name')),
                    CommandDefinition(SecurityRulesOperations.get, 'SecurityRule', command_alias='show', id_parameters=('resource_group_name', 'security_rule_name', 'network_security_group_name')),
                    CommandDefinition(SecurityRulesOperations.list, '[SecurityRule]', id_parameters=['resource_group_name']),
                ],
                command_table)

# SubnetsOperations
build_operation("network vnet subnet",
                "subnets",
                _network_client_factory,
                [
                    CommandDefinition(SubnetsOperations.delete, LongRunningOperation(L('Deleting subnet'), L('Subnet deleted')), id_parameters=('resource_group_name', 'virtual_network_name', 'subnet_name')),
                    CommandDefinition(SubnetsOperations.get, 'Subnet', command_alias='show', id_parameters=('resource_group_name', 'virtual_network_name', 'subnet_name')),
                    CommandDefinition(SubnetsOperations.list, '[Subnet]', id_parameters=('resource_group_name', 'virtual_network_name')),
                ],
                command_table)

build_operation(
    'network subnet', None, ConvenienceNetworkCommands,
    [
        CommandDefinition(ConvenienceNetworkCommands.create_update_subnet, 'Object', 'create', id_parameters=('resource_group_name', 'virtual_network_name', 'subnet_name'))
    ],
    command_table, SUBNET_ALIASES)

# UsagesOperations
build_operation("network",
                "usages",
                _network_client_factory,
                [
                    CommandDefinition(UsagesOperations.list, '[Usage]', command_alias='list-usages'),
                ],
                command_table)

# VirtualNetworkGatewayConnectionsOperations
build_operation("network vpn-connection",
                "virtual_network_gateway_connections",
                _network_client_factory,
                [
                    CommandDefinition(VirtualNetworkGatewayConnectionsOperations.delete, LongRunningOperation(L('Deleting virtual network gateway connection'), L('Virtual network gateway connection deleted')), id_parameters=('resource_group_name', 'virtual_network_gateway_connection_name')),
                    CommandDefinition(VirtualNetworkGatewayConnectionsOperations.get, 'VirtualNetworkGatewayConnection', command_alias='show', id_parameters=('resource_group_name', 'virtual_network_gateway_connection_name')),
                    CommandDefinition(VirtualNetworkGatewayConnectionsOperations.list, '[VirtualNetworkGatewayConnection]', id_parameters=['resource_group_name']),
                ],
                command_table)

# VirtualNetworkGatewayConnectionsOperations: shared-key
build_operation("network vpn-connection shared-key",
                "virtual_network_gateway_connections",
                _network_client_factory,
                [
                    CommandDefinition(VirtualNetworkGatewayConnectionsOperations.get_shared_key, 'ConnectionSharedKeyResult', command_alias='show', id_parameters=('resource_group_name', 'connection_shared_key_name')),
                    CommandDefinition(VirtualNetworkGatewayConnectionsOperations.reset_shared_key, 'ConnectionResetSharedKey', command_alias='reset', id_parameters=('resource_group_name', 'virtual_network_gateway_connection_name')),
                    CommandDefinition(VirtualNetworkGatewayConnectionsOperations.set_shared_key, 'ConnectionSharedKey', command_alias='set', id_parameters=('resource_group_name', 'virtual_network_gateway_connection_name')),
                ],
                command_table)

# VirtualNetworkGatewaysOperations
build_operation("network vpn-gateway",
                "virtual_network_gateways",
                _network_client_factory,
                [
                    CommandDefinition(VirtualNetworkGatewaysOperations.delete, LongRunningOperation(L('Deleting virtual network gateway'), L('Virtual network gateway deleted')), id_parameters=('resource_group_name', 'virtual_network_gateway_name')),
                    CommandDefinition(VirtualNetworkGatewaysOperations.get, 'VirtualNetworkGateway', command_alias='show', id_parameters=('resource_group_name', 'virtual_network_gateway_name')),
                    CommandDefinition(VirtualNetworkGatewaysOperations.list, '[VirtualNetworkGateway]', id_parameters=['resource_group_name']),
                ],
                command_table)

# VirtualNetworksOperations
build_operation("network vnet",
                "virtual_networks",
                _network_client_factory,
                [
                    CommandDefinition(VirtualNetworksOperations.delete, LongRunningOperation(L('Deleting virtual network'), L('Virtual network deleted')), id_parameters=('resource_group_name', 'virtual_network_name')),
                    CommandDefinition(VirtualNetworksOperations.get, 'VirtualNetwork', command_alias='show', id_parameters=('resource_group_name', 'virtual_network_name')),
                    CommandDefinition(VirtualNetworksOperations.list, '[VirtualNetwork]', id_parameters=['resource_group_name']),
                    CommandDefinition(VirtualNetworksOperations.list_all, '[VirtualNetwork]'),
                ],
                command_table)

build_operation('network vnet',
                'vnet',
                lambda **_: get_mgmt_service_client(VNetClient, VNetClientConfig),
                [
                    CommandDefinition(VNetOperations.create,
                                      LongRunningOperation(L('Creating virtual network'), L('Virtual network created')),
                                      id_parameters=('resource_group_name', 'deployment_parameter_virtual_network_name_value'))
                ],
                command_table,
                VNET_ALIASES)
