// Parameters
@description('Specifies the name of the virtual machine.')
param name string

@description('Specifies the location.')
param location string = resourceGroup().location

@description('Specifies the resource tags.')
param tags object = {}

@description('SKU for the cognitive search service')
@allowed([
  'basic'
  'free'
  'standard'
  'standard2'
  'standard3'
  'storage_optimized_l1'
  'storage_optimized_l2'
])
param sku string = 'basic'

@description('Authentication options for how the data plane API of a search service authenticates requests.')
param authOptions object = {}

@allowed(['enabled', 'disabled'])
param publicNetworkAccess string = 'enabled'

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    authOptions: authOptions
    disableLocalAuth: false
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    hostingMode: 'default'
    networkRuleSet: {
      ipRules: []
    }
    partitionCount: 1
    publicNetworkAccess: publicNetworkAccess
    replicaCount: 1
  }
  sku: {
    name: sku
  }
}

// Outputs
output id string = search.id
output name string = search.name
