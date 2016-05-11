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
                    CommandDefinition(VirtualMachineExtensionsOperations.delete, LongRunningOperation(L('Deleting VM extension'), L('VM extension deleted')), id_parameters=('resource_group_name', 'vm_name', 'vm_extension_name')),
                    CommandDefinition(VirtualMachineExtensionsOperations.get, 'VirtualMachineExtension', command_alias='show', id_parameters=('resource_group_name', 'vm_name', 'vm_extension_name')),
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
        CommandDefinition(ConvenienceVmCommands.list, '[VirtualMachine]', id_parameters=['resource_group_name'])
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
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.deallocate, LongRunningOperation(L('Deallocating VM scale set VMs'), L('VM scale set VMs deallocated')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.delete, LongRunningOperation(L('Deleting VM scale set VMs'), L('VM scale set VMs deleted')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.get, 'VirtualMachineScaleSetVM', command_alias='show', id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.get_instance_view, 'VirtualMachineScaleSetVMInstanceView', id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.list, '[VirtualMachineScaleSetVM]', id_parameters=('resource_group_name', 'vm_scale_set_name')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.power_off, LongRunningOperation(L('Powering off VM scale set VMs'), L('VM scale set VMs powered off')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.restart, LongRunningOperation(L('Restarting VM scale set VMs'), L('VM scale set VMs restarted')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                    CommandDefinition(VirtualMachineScaleSetVMsOperations.start, LongRunningOperation(L('Starting VM scale set VMs'), L('VM scale set VMs started')), id_parameters=('resource_group_name', 'vm_scale_set_name', 'instance_id')),
                ],
                command_table, PARAMETER_ALIASES)
build_operation(
    'vm', 'vm', lambda **_: get_mgmt_service_client(VMClient, VMClientConfig),
    [
        CommandDefinition(
            VMOperations.create_or_update,
            LongRunningOperation(L('Creating virtual machine'), L('Virtual machine created')),
            'create', id_parameters=('resource_group_name', 'name'))
    ],
    command_table, VM_CREATE_PARAMETER_ALIASES, VM_CREATE_EXTRA_PARAMETERS)

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

