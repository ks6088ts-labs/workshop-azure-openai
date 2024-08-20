// Parameters
@description('Specifies the name of the storage account.')
param name string

@description('Specifies an array of containers to create.')
param containerNames array = []

@description('Specifies the location.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

// Resources
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'

  // Containers live inside of a blob service
  resource blobService 'blobServices' = {
    name: 'default'
    properties: {
      deleteRetentionPolicy: {
        enabled: false
        allowPermanentDelete: false
      }
    }
    // Creating containers with provided names
    resource containers 'containers' = [
      for containerName in containerNames: {
        name: containerName
        properties: {
          publicAccess: 'None'
          defaultEncryptionScope: '$account-encryption-key'
          denyEncryptionScopeOverride: false
        }
      }
    ]
  }
}

// Outputs
output id string = storageAccount.id
output name string = storageAccount.name
