using './main.bicep'

// param prefix = 'secure'
// param suffix = 'test'
// param userObjectId = '<user-object-id>'
// param logAnalyticsName = '${prefix}loganalytics'
param openAiDeployments = [
  {
    model: {
      name: 'text-embedding-3-large'
      version: '1'
    }
    sku: {
      name: 'Standard'
      capacity: 10
    }
  }
  {
    model: {
      name: 'gpt-4o'
      version: '2024-05-13'
    }
    sku: {
      name: 'GlobalStandard'
      capacity: 10
    }
  }
]

param storageAccountContainerNames = [
  'audio'
]

param tags = {
  environment: 'development'
  iac: 'bicep'
}
