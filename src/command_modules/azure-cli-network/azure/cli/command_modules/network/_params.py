# pylint: disable=line-too-long
import argparse

from azure.cli.command_modules.network._actions import LBDNSNameAction, PublicIpDnsNameAction
from azure.cli.commands.parameters import (location_type, get_resource_name_completion_list, name_type, new_name_type, splitter, resource_group_name_type)
from azure.cli.commands import register_cli_argument, CliArgumentType

# BASIC PARAMETER CONFIGURATION

# Resource name/id parameters
public_ip_name_type = CliArgumentType(overrides=name_type, metavar='(ID | PUBLICIPNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/publicIPAddresses'), validator=splitter('public_ip_address_name'))
application_gateway_name_type = CliArgumentType(overrides=name_type, metavar='(ID | APPGATEWAYNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/applicationGateways'), validator=splitter('application_gateway_name'))
express_route_circuit_name_type = CliArgumentType(overrides=name_type, metavar='(ID | CIRCUITNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/expressRouteCircuits'), validator=splitter('circuit_name'))
express_route_authorization_name_type = CliArgumentType(overrides=name_type, metavar='(ID | NAME -g RESOURCEGROUP --circuit-name CIRCUITNAME)', validator=splitter('circuit_name', 'authorization_name'))
express_route_peering_name_type = CliArgumentType(overrides=name_type, metavar='(ID | NAME -g RESOURCEGROUP --circuit-name CIRCUITNAME)', validator=splitter('circuit_name', 'peering_name'))
load_balancer_name_type = CliArgumentType(overrides=name_type, metavar='(ID | LBNAME -g RESOURCEGROUP)', validator=splitter('resource_group_name', 'load_balancer_name'), completer=get_resource_name_completion_list('Microsoft.Network/loadBalancers'))
local_network_gateway_name_type = CliArgumentType(name_type, metavar='(ID | GATEWAYNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/localNetworkGateways'), validator=splitter('local_network_gateway_name'))
network_interface_name_type = CliArgumentType(name_type, metavar='(ID | NIC -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/networkInterfaces'), validator=splitter('network_interface_name'))
nsg_name_type = CliArgumentType(name_type, metavar='(ID | NSGNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/networkSecurityGroups'), validator=splitter('network_security_group_name'))
nsg_rule_name_type = CliArgumentType(name_type, metavar='(ID | NSGRULENAME -g RESOURCEGROUP --nsg-name NSGNAME)', validator=splitter('network_security_group_name', 'security_rule_name'))
route_name_type = CliArgumentType(name_type, metavar='(ID | ROUTENAME -g RESOURCEGROUP --route-table-name ROUTETABLENAME)', validator=splitter('route_table_name', 'route_name'))
route_table_name_type = CliArgumentType(name_type, metavar='(ID | TABLENAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/routeTables'), validator=splitter('route_table_name'))
connection_shared_key_name_type = CliArgumentType(name_type, metavar=('ID | CONNECTIONNAME -g RESOURCEGROUP'), validator=splitter('connection_shared_key_name'))
subnet_name_type = CliArgumentType(name_type, metavar='(ID | SUBNETNAME -g RESOURCEGROUP --vnet-name VNETNAME)', validator=splitter('virtual_network_name', child_resource_name_dest='subnet_name'))
virtual_network_gateway_connection_name = CliArgumentType(name_type, metavar='(ID | VPNCONNECTIONNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/virtualNetworkGatewayConnections'), validator=splitter('virtual_network_gateway_connection_name'))
virtual_network_gateway_vpn_name_type = CliArgumentType(name_type, metavar='(ID | GATEWAYNAME -g RESOURCEGROUP)', completer=get_resource_name_completion_list('Microsoft.Network/virtualNetworkGateways'), validator=splitter('virtual_network_gateway_name'))
virtual_network_name_type = CliArgumentType(overrides=name_type, metavar='(ID | VNETNAME -g RESOURCEGROUP)', help='Name of the virtual network.', completer=get_resource_name_completion_list('Microsoft.Network/virtualNetworks'), validator=splitter('virtual_network_name'))

# Resource type parameters when used to identify child resources
parent_express_route_circuit_name_type = CliArgumentType(overrides=virtual_network_name_type, options_list=('--circuit-name',), metavar='CIRCUITNAME', validator=None)
parent_nsg_name_type = CliArgumentType(overrides=nsg_name_type, options_list=('--nsg-name',), metavar='NSGNAME', validator=None)
parent_route_table_name_type = CliArgumentType(overrides=route_table_name_type, options_list=('--route-table-name',), metavar='ROUTETABLENAME', validator=None)
parent_virtual_network_gateway_connection_name_type = CliArgumentType(overrides=virtual_network_gateway_connection_name, options_list=('--connection-name',), metavar='CONNECTIONNAME', validator=None)
parent_virtual_network_name_type = CliArgumentType(overrides=virtual_network_name_type, options_list=('--vnet-name',), metavar='VNETNAME', validator=None)

# Parameter registration
register_cli_argument('network', 'resource_group_name', resource_group_name_type, required=False)
register_cli_argument('network', 'subnet_name', arg_type=subnet_name_type)
register_cli_argument('network', 'virtual_network_name', virtual_network_name_type)
register_cli_argument('network application-gateway', 'application_gateway_name', arg_type=application_gateway_name_type )

register_cli_argument('network express-route circuit', 'circuit_name', arg_type=express_route_circuit_name_type)
register_cli_argument('network express-route circuit-auth', 'circuit_name', arg_type=parent_express_route_circuit_name_type)
register_cli_argument('network express-route circuit-auth', 'authorization_name', arg_type=express_route_authorization_name_type )
register_cli_argument('network express-route circuit-peering', 'circuit_name', arg_type=parent_express_route_circuit_name_type)
register_cli_argument('network express-route circuit-peering', 'peering_name', arg_type=express_route_peering_name_type)

register_cli_argument('network local-gateway', 'local_network_gateway_name', arg_type=local_network_gateway_name_type)

register_cli_argument('network nic', 'network_interface_name', arg_type=network_interface_name_type)

register_cli_argument('network nic scale-set', 'virtual_machine_scale_set_name', options_list=('--vm-scale-set',), completer=get_resource_name_completion_list('Microsoft.Compute/virtualMachineScaleSets'))
register_cli_argument('network nic scale-set', 'virtualmachine_index', options_list=('--vm-index',))

register_cli_argument('network nsg', 'network_security_group_name', arg_type=nsg_name_type)

register_cli_argument('network nsg rule', 'security_rule_name', arg_type=nsg_rule_name_type)
register_cli_argument('network nsg rule', 'network_security_group_name', arg_type=parent_nsg_name_type)
register_cli_argument('network nsg rule create', 'priority', default=1000)
register_cli_argument('network nsg rule create', 'security_rule_name', arg_type=new_name_type)
register_cli_argument('network nsg rule create', 'network_security_group_name', arg_type=parent_nsg_name_type)

register_cli_argument('network public-ip', 'public_ip_address_name', arg_type=public_ip_name_type)

register_cli_argument('network public-ip create', 'name', arg_type=new_name_type)
register_cli_argument('network public-ip create', 'dns_name', action=PublicIpDnsNameAction)
register_cli_argument('network public-ip create', 'public_ip_address_type', help=argparse.SUPPRESS)
register_cli_argument('network public-ip create', 'allocation_method', choices=['dynamic', 'static'], default='dynamic')

register_cli_argument('network route-operation', 'route_table_name', arg_type=parent_route_table_name_type)
register_cli_argument('network route-operation', 'route_name', arg_type=route_table_name_type)

register_cli_argument('network route-table', 'route_table_name', arg_type=route_table_name_type)

register_cli_argument('network vnet', 'virtual_network_name', virtual_network_name_type)

register_cli_argument('network vnet create', 'location', location_type)
register_cli_argument('network vnet create', 'subnet_prefix', options_list=('--subnet-prefix',), metavar='SUBNET_PREFIX', default='10.0.0.0/24')
register_cli_argument('network vnet create', 'subnet_name', options_list=('--subnet-name',), metavar='SUBNET_NAME', default='Subnet1')
register_cli_argument('network vnet create', 'virtual_network_prefix', options_list=('--vnet-prefix',), metavar='VNET_PREFIX', default='10.0.0.0/16')
register_cli_argument('network vnet create', 'virtual_network_name', arg_type=new_name_type)

register_cli_argument('network vnet subnet', 'virtual_network_name', arg_type=parent_virtual_network_name_type)
register_cli_argument('network vnet subnet', 'subnet_name', arg_type=subnet_name_type)
register_cli_argument('network vnet subnet', 'address_prefix', metavar='PREFIX', help='the address prefix in CIDR format.')

register_cli_argument('network lb', 'load_balancer_name', arg_type=load_balancer_name_type)

register_cli_argument('network lb create', 'load_balancer_name', arg_type=new_name_type)
register_cli_argument('network lb create', 'resource_group_name', arg_type=resource_group_name_type, required=True)
register_cli_argument('network lb create', 'dns_name_for_public_ip', action=LBDNSNameAction)
register_cli_argument('network lb create', 'dns_name_type', help=argparse.SUPPRESS)
register_cli_argument('network lb create', 'private_ip_address_allocation', help='', choices=['dynamic', 'static'], default='dynamic')
register_cli_argument('network lb create', 'public_ip_address_allocation', help='', choices=['dynamic', 'static'], default='dynamic')
register_cli_argument('network lb create', 'public_ip_address_type', help='', choices=['new', 'existing', 'none'], default='new')
register_cli_argument('network lb create', 'virtual_network_name', arg_type=parent_virtual_network_name_type, validator=None)
register_cli_argument('network lb create', 'subnet_name', options_list=('--subnet-name',), metavar='SUBNET', validator=None)

register_cli_argument('network nsg create', 'name', arg_type=new_name_type)

register_cli_argument('network vpn-gateway', 'virtual_network_gateway_name', arg_type=virtual_network_gateway_vpn_name_type)

register_cli_argument('network vpn-connection', 'virtual_network_gateway_connection_name', arg_type=virtual_network_gateway_connection_name)

register_cli_argument('network vpn-connection shared-key', 'connection_shared_key_name', arg_type=connection_shared_key_name_type)
register_cli_argument('network vpn-connection shared-key', 'virtual_network_gateway_connection_name', arg_type=parent_virtual_network_gateway_connection_name_type)
