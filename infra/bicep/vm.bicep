// vm.bicep
// Deploys an Ubuntu Server 24.04 LTS VM
// Includes Public IP, NIC, SSH access, and OS disk
// Depends on network.bicep being deployed first

@description('Azure region')
param location string = 'eastus'

@description('Admin username for the VM')
param adminUsername string = 'azureuser'

@description('SSH public key content')
param sshPublicKey string

@description('Azure VM size')
param vmSize string = 'Standard_D2s_v4'

// Reference existing Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' existing = {
  name: 'vnet-migration-dev-eastus'
}

// Public IP Address
resource publicIp 'Microsoft.Network/publicIPAddresses@2023-04-01' = {
  name: 'pip-vm-onprem-migration'
  location: location

  sku: {
    name: 'Standard'
  }

  properties: {
    publicIPAllocationMethod: 'Static'
  }
}

// Network Interface
resource nic 'Microsoft.Network/networkInterfaces@2023-04-01' = {
  name: 'nic-vm-onprem-migration'
  location: location

  properties: {
    ipConfigurations: [
      {
        name: 'ipconfig1'

        properties: {
          subnet: {
            id: '${vnet.id}/subnets/app-subnet'
          }

          publicIPAddress: {
            id: publicIp.id
          }
        }
      }
    ]
  }
}

// Virtual Machine
resource vm 'Microsoft.Compute/virtualMachines@2023-07-01' = {
  name: 'vm-onprem-simulation'
  location: location

  tags: {
    Project: 'OnPremMigration'
    Environment: 'Dev'
    Purpose: 'OnPremSimulation'
  }

  properties: {

    // VM Size
    hardwareProfile: {
      vmSize: vmSize
    }

    // OS Configuration
    osProfile: {
      computerName: 'vm-onprem-simulation'
      adminUsername: adminUsername

      linuxConfiguration: {
        disablePasswordAuthentication: true

        ssh: {
          publicKeys: [
            {
              path: '/home/${adminUsername}/.ssh/authorized_keys'
              keyData: sshPublicKey
            }
          ]
        }
      }
    }

    // Storage / OS Image
    storageProfile: {

      imageReference: {
        publisher: 'canonical'
        offer: 'ubuntu-24_04-lts'
        sku: 'server'
        version: 'latest'
      }

      osDisk: {
        name: 'osdisk-vm-onprem-simulation'

        createOption: 'FromImage'

        managedDisk: {
          storageAccountType: 'StandardSSD_LRS'
        }

        caching: 'ReadWrite'
        diskSizeGB: 30
      }
    }

    // Network Interface Attachment
    networkProfile: {
      networkInterfaces: [
        {
          id: nic.id
        }
      ]
    }

    // Boot Diagnostics
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
      }
    }
  }
}

// Outputs
output vmName string = vm.name
output vmPublicIp string = publicIp.properties.ipAddress
