<#
This Script will remove all items from preservation hold library.
Make sure to disable retention policies first
#>

Connect-SPOService -Url "" #Enter SharePoint Admin URL
Connect-PnPOnline -Url "" -UseWebLogin #Enter the OneDrive URL for the user you need to connect to

    $i = 0
    Do{
        $items3 = Get-PnPListItem -List PreservationHoldLibrary -PageSize 100 | Select-Object ID -first 100
        [array]::Reverse($items3)
        foreach($Row in $items3) {
            Write-Host $row.id
            Remove-PnPListItem -list PreservationHoldLibrary  -Identity $Row.id -force
        }
        $i++
        Write-Host $i
    }while($items3 -ne "")

