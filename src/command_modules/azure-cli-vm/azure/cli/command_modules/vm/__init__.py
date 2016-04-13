from azure.mgmt.compute import ComputeManagementClient, ComputeManagementClientConfiguration
from azure.mgmt.compute.operations import (AvailabilitySetsOperations,
                                           VirtualMachineExtensionImagesOperations,
                                           VirtualMachineExtensionsOperations,
                                           VirtualMachineImagesOperations,
                                           UsageOperations,
                                           VirtualMachineSizesOperations,
                                           VirtualMachinesOperations,
                                           VirtualMachineScaleSetsOperations,
                                           VirtualMachineScaleSetVMsOperations)

from azure.cli.commands._command_creation import get_mgmt_service_client
from azure.cli.commands._auto_command import build_operation, AutoCommandDefinition
from azure.cli.commands import CommandTable, LongRunningOperation, COMMON_PARAMETERS
from azure.cli._locale import L

def _compute_client_factory(_):
    return get_mgmt_service_client(ComputeManagementClient, ComputeManagementClientConfiguration)

command_table = CommandTable()

# pylint: disable=line-too-long
build_operation("vm availabilityset",
                "availability_sets",
                _compute_client_factory,
                [
                    AutoCommandDefinition(AvailabilitySetsOperations.delete, None),
                    AutoCommandDefinition(AvailabilitySetsOperations.get, 'AvailabilitySet'),
                    AutoCommandDefinition(AvailabilitySetsOperations.list, '[AvailabilitySet]'),
                    AutoCommandDefinition(AvailabilitySetsOperations.list_available_sizes, '[VirtualMachineSize]', 'list-sizes')
                ],
                command_table)


build_operation("vm machineextensionimage",
                "virtual_machine_extension_images",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineExtensionImagesOperations.get, 'VirtualMachineExtensionImage'),
                    AutoCommandDefinition(VirtualMachineExtensionImagesOperations.list_types, '[VirtualMachineImageResource]'),
                    AutoCommandDefinition(VirtualMachineExtensionImagesOperations.list_versions, '[VirtualMachineImageResource]'),
                ],
                command_table)

build_operation("vm extension",
                "virtual_machine_extensions",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineExtensionsOperations.delete, LongRunningOperation(L('Deleting VM extension'), L('VM extension deleted'))),
                    AutoCommandDefinition(VirtualMachineExtensionsOperations.get, 'VirtualMachineExtension'),
                ],
                command_table)

build_operation("vm image",
                "virtual_machine_images",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineImagesOperations.get, 'VirtualMachineImage'),
                    AutoCommandDefinition(VirtualMachineImagesOperations.list, '[VirtualMachineImageResource]'),
                    AutoCommandDefinition(VirtualMachineImagesOperations.list_offers, '[VirtualMachineImageResource]'),
                    AutoCommandDefinition(VirtualMachineImagesOperations.list_publishers, '[VirtualMachineImageResource]'),
                    AutoCommandDefinition(VirtualMachineImagesOperations.list_skus, '[VirtualMachineImageResource]'),
                ],
                command_table)

build_operation("vm usage",
                "usage",
                _compute_client_factory,
                [
                    AutoCommandDefinition(UsageOperations.list, '[Usage]'),
                ],
                command_table)

build_operation("vm size",
                "virtual_machine_sizes",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineSizesOperations.list, '[VirtualMachineSize]'),
                ],
                command_table)

build_operation("vm",
                "virtual_machines",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachinesOperations.delete, LongRunningOperation(L('Deleting VM'), L('VM Deleted'))),
                    AutoCommandDefinition(VirtualMachinesOperations.deallocate, LongRunningOperation(L('Deallocating VM'), L('VM Deallocated'))),
                    AutoCommandDefinition(VirtualMachinesOperations.generalize, None),
                    AutoCommandDefinition(VirtualMachinesOperations.get, 'VirtualMachine'),
                    AutoCommandDefinition(VirtualMachinesOperations.list, '[VirtualMachine]'),
                    AutoCommandDefinition(VirtualMachinesOperations.list_all, '[VirtualMachine]'),
                    AutoCommandDefinition(VirtualMachinesOperations.list_available_sizes, '[VirtualMachineSize]', 'list-sizes'),
                    AutoCommandDefinition(VirtualMachinesOperations.power_off, LongRunningOperation(L('Powering off VM'), L('VM powered off'))),
                    AutoCommandDefinition(VirtualMachinesOperations.restart, LongRunningOperation(L('Restarting VM'), L('VM Restarted'))),
                    AutoCommandDefinition(VirtualMachinesOperations.start, LongRunningOperation(L('Starting VM'), L('VM Started'))),
                ],
                command_table)

build_operation("vm scaleset",
                "virtual_machine_scale_sets",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.deallocate, LongRunningOperation(L('Deallocating VM scale set'), L('VM scale set deallocated'))),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.delete, LongRunningOperation(L('Deleting VM scale set'), L('VM scale set deleted'))),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.get, 'VirtualMachineScaleSet'),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.delete_instances, LongRunningOperation(L('Deleting VM scale set instances'), L('VM scale set instances deleted'))),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.get_instance_view, 'VirtualMachineScaleSetInstanceView'),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.list, '[VirtualMachineScaleSet]'),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.list_all, '[VirtualMachineScaleSet]'),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.list_skus, '[VirtualMachineScaleSet]'),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.power_off, LongRunningOperation(L('Powering off VM scale set'), L('VM scale set powered off'))),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.restart, LongRunningOperation(L('Restarting VM scale set'), L('VM scale set restarted'))),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.start, LongRunningOperation(L('Starting VM scale set'), L('VM scale set started'))),
                    AutoCommandDefinition(VirtualMachineScaleSetsOperations.update_instances, LongRunningOperation(L('Updating VM scale set instances'), L('VM scale set instances updated'))),
                ],
                command_table)

build_operation("vm scalesetvm",
                "virtual_machine_scale_set_vms",
                _compute_client_factory,
                [
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.deallocate, LongRunningOperation(L('Deallocating VM scale set VMs'), L('VM scale set VMs deallocated'))),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.delete, LongRunningOperation(L('Deleting VM scale set VMs'), L('VM scale set VMs deleted'))),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.get, 'VirtualMachineScaleSetVM'),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.get_instance_view, 'VirtualMachineScaleSetVMInstanceView'),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.list, '[VirtualMachineScaleSetVM]'),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.power_off, LongRunningOperation(L('Powering off VM scale set VMs'), L('VM scale set VMs powered off'))),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.restart, LongRunningOperation(L('Restarting VM scale set VMs'), L('VM scale set VMs restarted'))),
                    AutoCommandDefinition(VirtualMachineScaleSetVMsOperations.start, LongRunningOperation(L('Starting VM scale set VMs'), L('VM scale set VMs started'))),
                ],
                command_table)

# Patch/update operations for Virtual Machines

from azure.mgmt.compute.models.compute_management_client_enums import DiskCreateOptionTypes, CachingTypes
from azure.mgmt.compute.models import DataDisk, VirtualHardDisk

def vm_getter(args):
    client = _compute_client_factory(args)
    result = client.virtual_machines.get(args.get('resourcegroup'), args.get('vm_name'))
    return result

def vm_setter(args, instance, start_msg, end_msg):
    instance .resources = None # Issue: https://github.com/Azure/autorest/issues/934
    client = _compute_client_factory(args)
    poller = client.virtual_machines.create_or_update(resource_group_name = args.get('resourcegroup'), 
                                                      vm_name = args.get('vm_name'), 
                                                      parameters = instance)
    return LongRunningOperation(start_msg, end_msg)(poller)

def patches_vm(start_msg, finish_msg):
    '''Decorator indicating that the decorated function modifies an existing Virtual Machine
    in Azure.
    It automatically adds arguments required to identify the Virtual Machine to be patched and
    handles the actual put call to the compute service, leaving the decorated function to only
    have to worry about the modifications it has to do.
    '''
    def wrapped(func):
        def invoke(args):
            instance = vm_getter(args)
            func(args, instance)
            vm_setter(args, instance, start_msg, finish_msg)

        command_table[invoke]['arguments'].append(COMMON_PARAMETERS['resource_group_name'])
        command_table[invoke]['arguments'].append({
            'name': '--vm-name -n',
            'dest': 'vm_name',
            'help': 'Name of Virtual Machine to update',
            'required': True
            })
        return invoke
    return wrapped

@command_table.command('vm disk attach-new', help=L('Attach a new disk to an existing Virtual Machine'))
@command_table.option('--lun', dest='lun', type=int, required=True)
@command_table.option('--diskname', dest='name', help='Disk name', required=True)
@command_table.option('--disksize', dest='disksize', help='Size of disk (Gb)', type=int, default=1023)
@command_table.option('--vhd', required=True, type=VirtualHardDisk)
@patches_vm('Attaching disk', 'Disk attached')
def _vm_disk_attach_new(args, instance):
    disk = DataDisk(lun=args.get('lun'), vhd = args.get('vhd'), name=args.get('name'), create_option=DiskCreateOptionTypes.empty, disk_size_gb = args.get('disksize'))
    instance.storage_profile.data_disks.append(disk)

@command_table.command('vm disk attach-existing', help=L('Attach an existing disk to an existing Virtual Machine'))
@command_table.option('--lun', dest='lun', type=int, required=True)
@command_table.option('--diskname', dest='name', help='Disk name', required=True)
@command_table.option('--vhd', required=True, type=VirtualHardDisk)
@command_table.option('--disksize', dest='disksize', help='Size of disk (Gb)', type=int, default=1023)
@patches_vm('Attaching disk', 'Disk attached')
def _vm_disk_attach_new(args, instance):
    disk = DataDisk(lun=args.get('lun'), vhd = args.get('vhd'), name=args.get('name'), create_option=DiskCreateOptionTypes.attach, disk_size_gb = args.get('disksize'))
    instance.storage_profile.data_disks.append(disk)

@command_table.command('vm disk detach')
@command_table.option('--diskname', dest='name', help='Disk name', required=True)
@patches_vm('Detaching disk', 'Disk detached')
def _vm_disk_detach(args, instance):
    instance.resources = None # Issue: https://github.com/Azure/autorest/issues/934
    disk = next(iter(([d for d in instance.storage_profile.data_disks if d.name == args.get('name')])))
    if disk:
        instance.storage_profile.data_disks.remove(disk)
    else:
        raise RuntimeError("No disk with the name '%s' found" % args.get('name'))

