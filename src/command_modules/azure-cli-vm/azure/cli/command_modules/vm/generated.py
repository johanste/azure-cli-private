from azure.mgmt.compute.operations import (AvailabilitySetsOperations,
                                           VirtualMachineExtensionImagesOperations,
                                           VirtualMachineExtensionsOperations,
                                           VirtualMachineImagesOperations,
                                           UsageOperations,
                                           VirtualMachineSizesOperations,
                                           VirtualMachinesOperations,
                                           VirtualMachineScaleSetsOperations,
                                           VirtualMachineScaleSetVMsOperations)

from azure.cli.commands._auto_command import build_operation, CommandDefinition
from azure.cli.commands._command_creation import get_mgmt_service_client
from azure.cli.commands import CommandTable, LongRunningOperation, patch_aliases
from azure.cli._locale import L
from azure.cli.command_modules.vm.mgmt_avail_set.lib import (AvailSetCreationClient
                                                             as AvailSetClient,
                                                             AvailSetCreationClientConfiguration
                                                             as AvailSetClientConfig)
from azure.cli.command_modules.vm.mgmt_avail_set.lib.operations import AvailSetOperations
from azure.cli.command_modules.vm.mgmt_vm_create.lib import (VMCreationClient as VMClient,
                                                             VMCreationClientConfiguration
                                                             as VMClientConfig)
from azure.cli.command_modules.vm.mgmt_vm_create.lib.operations import VMOperations
from azure.cli._help_files import helps

from ._params import (PARAMETER_ALIASES, VM_CREATE_EXTRA_PARAMETERS, VM_CREATE_PARAMETER_ALIASES,
                      VM_PATCH_EXTRA_PARAMETERS)
from ._factory import _compute_client_factory
from ._help import helps # pylint: disable=unused-import
from .custom import ConvenienceVmCommands

command_table = CommandTable()

# pylint: disable=line-too-long
build_operation("vm availset",
                "availability_sets",
                _compute_client_factory,
                [
                    CommandDefinition(AvailabilitySetsOperations.delete, None, id_parameters=('resource_group_name', 'availability_set_name')),
                    CommandDefinition(AvailabilitySetsOperations.get, 'AvailabilitySet', command_alias='show', id_parameters=('resource_group_name', 'availability_set_name')),
                    CommandDefinition(AvailabilitySetsOperations.list, '[AvailabilitySet]', id_parameters=['resource_group_name']),
                    CommandDefinition(AvailabilitySetsOperations.list_available_sizes, '[VirtualMachineSize]', 'list-sizes', id_parameters=['resource_group_name'])
                ],
                command_table, PARAMETER_ALIASES)

build_operation(
    'vm machine-extension-image', 'virtual_machine_extension_images', _compute_client_factory,
    [
        CommandDefinition(VirtualMachineExtensionImagesOperations.get, 'VirtualMachineExtensionImage', command_alias='show'),
        CommandDefinition(VirtualMachineExtensionImagesOperations.list_types, '[VirtualMachineImageResource]'),
        CommandDefinition(VirtualMachineExtensionImagesOperations.list_versions, '[VirtualMachineImageResource]'),
    ],
    command_table, PARAMETER_ALIASES)

build_operation(
    'vm disk', None, ConvenienceVmCommands,
    [
        CommandDefinition(ConvenienceVmCommands.attach_new_disk, 'Object', 'attach-new'),
        CommandDefinition(ConvenienceVmCommands.attach_existing_disk, 'Object', 'attach-existing'),
        CommandDefinition(ConvenienceVmCommands.detach_disk, 'Object', 'detach'),
    ],
    command_table, PARAMETER_ALIASES, VM_PATCH_EXTRA_PARAMETERS)

build_operation("vm extension",
                "virtual_machine_extensions",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineExtensionsOperations.delete, LongRunningOperation(L('Deleting VM extension'), L('VM extension deleted')), id_parameters=('resource_group_name', 'vm_name', 'vm_extension_name')),
                    AutoCommandDefinition(VirtualMachineExtensionsOperations.get, 'VirtualMachineExtension', command_alias='show', id_parameters=('resource_group_name', 'vm_name', 'vm_extension_name')),
                ],
                command_table, PARAMETER_ALIASES)

build_operation(
    'vm image', 'virtual_machine_images', _compute_client_factory,
    [
        CommandDefinition(VirtualMachineImagesOperations.get, 'VirtualMachineImage', command_alias='show'),
        CommandDefinition(VirtualMachineImagesOperations.list_offers, '[VirtualMachineImageResource]'),
        CommandDefinition(VirtualMachineImagesOperations.list_publishers, '[VirtualMachineImageResource]'),
        CommandDefinition(VirtualMachineImagesOperations.list_skus, '[VirtualMachineImageResource]'),
    ],
    command_table, PARAMETER_ALIASES)

build_operation(
    'vm usage', 'usage', _compute_client_factory,
    [
        CommandDefinition(UsageOperations.list, '[Usage]'),
    ],
    command_table, PARAMETER_ALIASES)

build_operation(
    'vm size', 'virtual_machine_sizes', _compute_client_factory,
    [
        CommandDefinition(VirtualMachineSizesOperations.list, '[VirtualMachineSize]'),
    ],
    command_table, PARAMETER_ALIASES)

build_operation("vm",
                "virtual_machines",
                _compute_client_factory,
                [
                    CommandDefinition(VirtualMachinesOperations.delete, LongRunningOperation(L('Deleting VM'), L('VM Deleted')), id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.deallocate, LongRunningOperation(L('Deallocating VM'), L('VM Deallocated')), id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.generalize, None, id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.get, 'VirtualMachine', command_alias='show', id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.list_available_sizes, '[VirtualMachineSize]', 'list-sizes', id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.power_off, LongRunningOperation(L('Powering off VM'), L('VM powered off')), id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.restart, LongRunningOperation(L('Restarting VM'), L('VM Restarted')), id_parameters=('resource_group_name', 'vm_name')),
                    CommandDefinition(VirtualMachinesOperations.start, LongRunningOperation(L('Starting VM'), L('VM Started')), id_parameters=('resource_group_name', 'vm_name')),
                ],
                command_table, PARAMETER_ALIASES)

build_operation(
    'vm', None, ConvenienceVmCommands,
    [
        CommandDefinition(ConvenienceVmCommands.list_ip_addresses, 'object', id_parameters=('resource_group_name', 'vm_name')),
        CommandDefinition(ConvenienceVmCommands.list, '[VirtualMachine]')
    ],
    command_table, PARAMETER_ALIASES)
build_operation("vm scaleset",
                "virtual_machine_scale_sets",
                _compute_client_factory,
                [
                    CommandDefinition(VirtualMachineScaleSetsOperations.deallocate, LongRunningOperation(L('Deallocating VM scale set'), L('VM scale set deallocated')), id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.delete, LongRunningOperation(L('Deleting VM scale set'), L('VM scale set deleted')), id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.get, 'VirtualMachineScaleSet', command_alias='show', id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.delete_instances, LongRunningOperation(L('Deleting VM scale set instances'), L('VM scale set instances deleted')), id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.get_instance_view, 'VirtualMachineScaleSetInstanceView', id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.list, '[VirtualMachineScaleSet]', id_parameters=('resource_group_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.list_all, '[VirtualMachineScaleSet]'),
                    CommandDefinition(VirtualMachineScaleSetsOperations.list_skus, '[VirtualMachineScaleSet]', id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.power_off, LongRunningOperation(L('Powering off VM scale set'), L('VM scale set powered off')),  id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.restart, LongRunningOperation(L('Restarting VM scale set'), L('VM scale set restarted')), id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.start, LongRunningOperation(L('Starting VM scale set'), L('VM scale set started')), id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetsOperations.update_instances, LongRunningOperation(L('Updating VM scale set instances'), L('VM scale set instances updated')), id_parameters=('resource_group_name', 'vm_scale_set_name')),
                ],
                command_table, PARAMETER_ALIASES)

build_operation("vm scaleset-vm",
                "virtual_machine_scale_set_vms",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.deallocate, LongRunningOperation(L('Deallocating VM scale set VMs'), L('VM scale set VMs deallocated')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.delete, LongRunningOperation(L('Deleting VM scale set VMs'), L('VM scale set VMs deleted')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.get, 'VirtualMachineScaleSetVM', command_alias='show', id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.get_instance_view, 'VirtualMachineScaleSetVMInstanceView', id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.list, '[VirtualMachineScaleSetVM]', id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.power_off, LongRunningOperation(L('Powering off VM scale set VMs'), L('VM scale set VMs powered off')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.restart, LongRunningOperation(L('Restarting VM scale set VMs'), L('VM scale set VMs restarted')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.start, LongRunningOperation(L('Starting VM scale set VMs'), L('VM scale set VMs started')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                ],
                command_table, PARAMETER_ALIASES)
build_operation(
    'vm', 'vm', lambda **_: get_mgmt_service_client(VMClient, VMClientConfig),
    [
        CommandDefinition(
            VMOperations.create_or_update,
            LongRunningOperation(L('Creating virtual machine'), L('Virtual machine created')),
            'create')
    ],
    command_table, VM_CREATE_PARAMETER_ALIASES, VM_CREATE_EXTRA_PARAMETERS)

vm_param_aliases = {
    'os_disk_uri': {
        'name': '--os-disk-uri',
        'help': argparse.SUPPRESS
        },
    'os_offer': {
        'name': '--os_offer',
        'help': argparse.SUPPRESS
        },
    'os_publisher': {
        'name': '--os-publisher',
        'help': argparse.SUPPRESS
        },
    'os_sku': {
        'name': '--os-sku',
        'help': argparse.SUPPRESS
        },
    'os_type': {
        'name': '--os-type',
        'help': argparse.SUPPRESS
        },
    'os_version': {
        'name': '--os-version',
        'help': argparse.SUPPRESS
        },
    }

class VMImageFieldAction(argparse.Action): #pylint: disable=too-few-public-methods
    def __call__(self, parser, namespace, values, option_string=None):
        image = values
        match = re.match('([^:]*):([^:]*):([^:]*):([^:]*)', image)

        if image.lower().endswith('.vhd'):
            namespace.os_disk_uri = image
        elif match:
            namespace.os_type = 'Custom'
            namespace.os_publisher = match.group(1)
            namespace.os_offer = match.group(2)
            namespace.os_sku = match.group(3)
            namespace.os_version = match.group(4)
        else:
            images = load_images_from_aliases_doc(None, None, None)
            matched = next((x for x in images if x['urn alias'].lower() == image.lower()), None)
            if matched is None:
                raise CLIError('Invalid image "{}". Please pick one from {}'.format(image,
                                                                                    [x['urn alias'] for x in images]))
            namespace.os_type = 'Custom'
            namespace.os_publisher = matched['publisher']
            namespace.os_offer = matched['offer']
            namespace.os_sku = matched['sku']
            namespace.os_version = matched['version']


class VMSSHFieldAction(argparse.Action): #pylint: disable=too-few-public-methods
    def __call__(self, parser, namespace, values, option_string=None):
        ssh_value = values

        if os.path.exists(ssh_value):
            with open(ssh_value, 'r') as f:
                namespace.ssh_key_value = f.read()
        else:
            namespace.ssh_key_value = ssh_value

class VMDNSNameAction(argparse.Action): #pylint: disable=too-few-public-methods
    def __call__(self, parser, namespace, values, option_string=None):
        dns_value = values

        if dns_value:
            namespace.dns_name_type = 'new'

        namespace.dns_name_for_public_ip = dns_value

extra_parameters = [
    {
        'name': '--image',
        'action': VMImageFieldAction
        },
    {
        'name': '--ssh-key-value',
        'action': VMSSHFieldAction
        },
    {
        'name': '--dns-name-for-public-ip',
        'action': VMDNSNameAction
        },
    {
        'name': '--dns-name-type',
        'help': argparse.SUPPRESS
        }
    ]

helps['vm create'] = """
            type: command
            short-summary: Create an Azure Virtual Machine
            long-summary: See https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-quick-create-cli/ for an end-to-end tutorial
            parameters: 
                - name: --image
                  type: string
                  required: false
                  short-summary: OS image (Common, URN or URI).
                  long-summary: |
                    Common OS types: Win2012R2Datacenter, Win2012Datacenter, Win2008SP1. For other values please run 'az vm image list'.
                    Example URN: MicrosoftWindowsServer:WindowsServer:2012-R2-Datacenter:latest
                    Example URI: http://<storageAccount>.blob.core.windows.net/vhds/osdiskimage.vhd
                  populator-commands: 
                    - az vm image list
                    - az vm image show
                - name: --ssh-key-value
                  short-summary: SSH key file value or key file path.
            examples:
                - name: Create a simple Windows Server VM with private IP address
                  text: >
                    az vm create --image Win2012R2Datacenter --admin-username myadmin --admin-password Admin_001 
                    -l "West US" -g myvms --name myvm001
                - name: Create a simple Windows Server VM with public IP address and DNS entry
                  text: >
                    az vm create --image Win2012R2Datacenter --admin-username myadmin --admin-password Admin_001 
                    -l "West US" -g myvms --name myvm001 --public-ip-address-type new --dns-name-for-public-ip myGloballyUniqueVmDnsName
                - name: Create a Linux VM with SSH key authentication, add a public DNS entry and add to an existing Virtual Network and Availability Set.
                  text: >
                    az vm create --image <linux image from 'az vm image list'>
                    --admin-username myadmin --admin-password Admin_001 --authentication-type sshkey
                    --virtual-network-type existing --virtual-network-name myvnet --subnet-name default
                    --availability-set-type existing --availability-set-id myavailset
                    --public-ip-address-type new --dns-name-for-public-ip myGloballyUniqueVmDnsName
                    -l "West US" -g myvms --name myvm18o --ssh-key-value "<ssh-rsa-key or key-file-path>"
            """



build_operation(
    'vm image', None, ConvenienceVmCommands,
    [
        CommandDefinition(ConvenienceVmCommands.list_vm_images, 'object', 'list')
    ],
    command_table, patch_aliases(PARAMETER_ALIASES, {
        'image_location': {'name': '--location -l'}
        }))

avail_set_param_aliases = {
    'name': {
        'name': '--name -n'
        }
    }

helps['vm availability-set create'] = """
            type: command
            long-summary: For more info, see https://blogs.technet.microsoft.com/yungchou/2013/05/14/window-azure-fault-domain-and-upgrade-domain-explained-explained-reprised/
"""

build_operation("vm availability-set",
                'avail_set',
                lambda **_: get_mgmt_service_client(AvailSetClient, AvailSetClientConfig),
                [
                    CommandDefinition(AvailSetOperations.create_or_update,
                                      LongRunningOperation(L('Creating availability set'), L('Availability set created')),
                                      'create')
                ],
                command_table,
                avail_set_param_aliases)

