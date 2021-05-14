#MFA Audit

Connect-MsolService

$MFAEnabled = 'False'

$UsersData = Get-MsolUser -EnabledFilter EnabledOnly -All | Select-Object DisplayName,Title,UserPrincipalName,StrongAuthenticationMethods | Where-Object{($_.Title -notmatch 'Volunteer') -or ($_.Title -notmatch '')}

foreach($Row in $UsersData){

    $MFAChecker = ($Row.StrongAuthenticationMethods).isdefault

    foreach($object in $MFAChecker){

        if($object -match 'True') {
            
            $MFAEnabled = 'True'
            #Write-host 'MFA Enabled'
        }
        
    }

    if(($MFAEnabled -eq 'False')){
        Write-Output "$($Row.DisplayName) + DOESNT HAVE MFA ENABLED" >> C:\temp\MFANOTENABLED.txt

    }

    $MFAEnabled = 'False'

}
Write-Host "The audit covered $($UsersData.Count) Users"