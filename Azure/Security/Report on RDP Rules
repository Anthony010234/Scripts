#Script can be run in Azure powershell console

#Start a report/transcript
Start-Transcript -Path "RDPRules.txt" -NoClobber

#Get list of all subscriptions you have access to
$AzureSubscriptions =  (Get-AzSubscription).ID

#For each Subscription, get NSGS and search for RDP rules
foreach ($Sub in $AzureSubscriptions){

	Select-AzSubscription -SubscriptionId $Sub
	$NSGCollection = Get-AzNetworkSecurityGroup

	foreach($NSG in $NSGCollection){
	
		Get-AzNetworkSecurityRuleConfig -NetworkSecurityGroup $NSG | Select-Object * | Where-Object {($_.Access -eq 'Allow' -and $_.SourceAddressPrefix -eq '*' -and $_.Direction -eq 'Inbound') -and ($_.DestinationPortRange -eq '3389' -or $_.DestinationPortRange -eq '*' -or $_.DestinationPortRange -like '-') }
	}
}

#Stop the report / Transcript
Stop-Transcript
