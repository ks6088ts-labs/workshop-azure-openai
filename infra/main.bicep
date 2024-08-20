// Parameters
@description('Specifies the name prefix for all the Azure resources.')
@minLength(4)
@maxLength(10)
param prefix string = substring(uniqueString(resourceGroup().id, location), 0, 4)

@description('Specifies the location for all the Azure resources.')
param location string = resourceGroup().location

@description('Specifies the name of the Azure Log Analytics resource.')
param logAnalyticsName string = ''

@description('Specifies the service tier of the workspace: Free, Standalone, PerNode, Per-GB.')
@allowed([
  'Free'
  'Standalone'
  'PerNode'
  'PerGB2018'
])
param logAnalyticsSku string = 'PerNode'

@description('Specifies the workspace data retention in days. -1 means Unlimited retention for the Unlimited Sku. 730 days is the maximum allowed for all other Skus.')
param logAnalyticsRetentionInDays int = 60

@description('Specifies the name of the Azure AI Services resource.')
param aiServicesName string = ''

@description('Specifies the resource model definition representing SKU.')
param aiServicesSku object = {
  name: 'S0'
}

@description('Specifies the identity of the Azure AI Services resource.')
param aiServicesIdentity object = {
  type: 'SystemAssigned'
}

@description('Specifies an optional subdomain name used for token-based authentication.')
param aiServicesCustomSubDomainName string = ''

@description('Specifies whether disable the local authentication via API key.')
param aiServicesDisableLocalAuth bool = false

@description('Specifies whether or not public endpoint access is allowed for this account..')
@allowed([
  'Enabled'
  'Disabled'
])
param aiServicesPublicNetworkAccess string = 'Enabled'

@description('Specifies the location for the Azure AI Services resource.')
param aiServicesLocation string = 'eastus'

@description('Specifies the OpenAI deployments to create.')
param openAiDeployments array = []

@description('Specifies the resource tags for all the resoources.')
param tags object = {}

@description('Specifies the object id of a Microsoft Entra ID user. In general, this the object id of the system administrator who deploys the Azure resources.')
param userObjectId string = ''

@description('Specifies the name of the Azure AI Search resource.')
param aiSearchName string = '${prefix}aisearch'

@description('Specifies the name of the Azure Cosmos DB resource.')
param cosmosDbName string = '${prefix}cosmosdb'

@description('Specifies the name of the Azure Storage Account resource.')
param storageAccountName string = '${prefix}storageaccount'

@description('Specifies the name of the Azure Storage Account containers.')
param storageAccountContainerNames array = []

// Resources
module workspace 'modules/logAnalytics.bicep' = {
  name: 'workspace'
  params: {
    // properties
    name: empty(logAnalyticsName) ? toLower('${prefix}-log-analytics') : logAnalyticsName
    location: location
    tags: tags
    sku: logAnalyticsSku
    retentionInDays: logAnalyticsRetentionInDays
  }
}

module aiServices 'modules/aiServices.bicep' = {
  name: 'aiServices'
  params: {
    // properties
    name: empty(aiServicesName) ? toLower('${prefix}-ai-services') : aiServicesName
    location: aiServicesLocation
    tags: tags
    sku: aiServicesSku
    identity: aiServicesIdentity
    customSubDomainName: empty(aiServicesCustomSubDomainName)
      ? toLower('${prefix}-ai-services')
      : aiServicesCustomSubDomainName
    disableLocalAuth: aiServicesDisableLocalAuth
    publicNetworkAccess: aiServicesPublicNetworkAccess
    deployments: openAiDeployments
    workspaceId: workspace.outputs.id

    // role assignments
    userObjectId: userObjectId
  }
}

module aiSearch './modules/aiSearch.bicep' = {
  name: 'aiSearch'
  params: {
    name: aiSearchName
    location: location
    tags: tags
  }
}

module cosmosDb './modules/cosmosDb.bicep' = {
  name: 'cosmosDb'
  params: {
    name: cosmosDbName
    location: location
    tags: tags
    primaryRegion: location
    secondaryRegion: 'japanwest'
  }
}

module storageAccount './modules/storageAccount.bicep' = {
  name: 'storageAccount'
  params: {
    name: storageAccountName
    containerNames: storageAccountContainerNames
    location: location
    tags: tags
  }
}

output deploymentInfo object = {
  subscriptionId: subscription().subscriptionId
  resourceGroupName: resourceGroup().name
  location: location
  aiServicesName: aiServices.outputs.name
  aiServicesEndpoint: aiServices.outputs.endpoint
  aiSearchName: aiSearch.outputs.name
  cosmosDbAccountName: cosmosDb.outputs.accountName
  cosmosDbAccountEndpoint: cosmosDb.outputs.accountEndpoint
  storageAccountName: storageAccount.outputs.name
}
