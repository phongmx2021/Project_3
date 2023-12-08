az group create --name RG-LogAnalytics --location eastus
az deployment group create --resource-group RG-LogAnalytics --name log-wsp --template-file deploylaworkspacetemplate.json