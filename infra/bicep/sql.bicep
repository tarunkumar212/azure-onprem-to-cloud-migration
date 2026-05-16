// sql.bicep
// Deploys Azure SQL Logical Server and Database
// Used in migration project — replaces SQLite on-premises database

@description('Azure region')
param location string = 'westus2'

@description('SQL Server admin username')
param adminUsername string = 'sqladmin'

@description('SQL Server admin password — pass at deploy time, never hardcode')
@secure()
param adminPassword string

@description('Environment name')
param environment string = 'dev'

var serverName = 'sqlserver-migration-${environment}'
var databaseName = 'sqldb-migration-${environment}'

// ── SQL Logical Server ─────────────────────────────────
resource sqlServer 'Microsoft.Sql/servers@2023-02-01-preview' = {
  name: serverName
  location: location
  tags: {
    Project: 'OnPremMigration'
    Environment: environment
  }
  properties: {
    administratorLogin: adminUsername
    administratorLoginPassword: adminPassword
    version: '12.0'
    publicNetworkAccess: 'Enabled'
  }
}

// ── Firewall — Allow Azure Services ───────────────────
resource allowAzureServices 'Microsoft.Sql/servers/firewallRules@2023-02-01-preview' = {
  parent: sqlServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// ── SQL Database ───────────────────────────────────────
resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-02-01-preview' = {
  parent: sqlServer
  name: databaseName
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
    capacity: 5
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    maxSizeBytes: 2147483648
    requestedBackupStorageRedundancy: 'Local'
  }
}

// ── Outputs ────────────────────────────────────────────
output serverFqdn string = sqlServer.properties.fullyQualifiedDomainName
output databaseName string = sqlDatabase.name
output connectionStringTemplate string = 'Server=${sqlServer.properties.fullyQualifiedDomainName};Database=${databaseName};Uid=${adminUsername};Pwd=<password>;Encrypt=yes;'
