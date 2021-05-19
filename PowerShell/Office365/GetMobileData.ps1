<#
Description: Script created to collect data about mobile users and format to a CSV
Created by: Anthony

Requirements:
    *Admin rights to O365 exchange

Version: 1
Last Modified by: Anthony

#>

#Connect to ExchangeOnline
Connect-ExchangeOnline

#Get data and Store data into array
$MobileData = Get-MobileDevice | Select-Object *

#Foreach loop to sift through data
foreach($Row in $MobileData){

    #Setting Variables to get data required
    $ID = $Row.Id
    $User = $Row.UserDisplayName
    $ObjectCat = $Row.ObjectCategory
    $ObjectClass = $Row.ObjectClass
    $CreatedDate = $Row.WhenCreated
    $DeviceName = $Row.FriendlyName
    $DeviceOS = $Row.DeviceOS
    $DeviceModel = $Row.DeviceModel
    $DeviceType = $Row.DeviceType
    $DeviceUA = $Row.DeviceUserAgent
    $DeviceAS = $Row.DeviceAccessState
    $DeviceASR = $Row.DeviceAccessStateReason


    #Create a new array to organise data into columns
    $hash = @{ID =$ID; UserDisplayName = $User; ObjectCategory = $ObjectCat; ObjectClass = $ObjectClass; CreatedDate = $CreatedDate; DeviceName = $DeviceName;
    DeviceOS = $DeviceOS; DeviceModel = $DeviceModel; DeviceType = $DeviceType; DeviceUserAgent = $DeviceUA; DeviceAccessState = $DeviceAS; DeviceAccessStateReason = $DeviceASR}

    #Specify new row
    $newRow = New-Object PsObject -Property $hash

    #Export data to CSV
    Export-Csv C:\temp\MobileData.csv -inputobject $newrow -NoTypeInformation -Append | % {$_.Replace('"','')}

}