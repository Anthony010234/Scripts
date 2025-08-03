param (
    [Parameter(Mandatory)]
    [string]$CsvPath
)

# Track visited domains to avoid recursion loops
$visitedDomains = @{}

function Resolve-SPFRecordRecursively {
    param (
        [string]$domain
    )

    if ($visitedDomains.ContainsKey($domain)) {
        return @()
    }

    $visitedDomains[$domain] = $true
    $ips = @()

    try {
        $txtRecords = (Resolve-DnsName -Type TXT -Name $domain -ErrorAction Stop).Strings
    } catch {
        Write-Warning "No TXT record found for $domain"
        return $ips
    }

    $spfRecord = $txtRecords | Where-Object { $_ -like "v=spf1*" } | Select-Object -First 1
    if (-not $spfRecord) {
        return $ips
    }

    $tokens = $spfRecord -split '\s+'

    foreach ($token in $tokens) {
        switch -Regex ($token) {
            '^ip4:(.+)'     { $ips += $Matches[1] }
            '^ip6:(.+)'     { $ips += $Matches[1] }
            '^include:(.+)' { $ips += Resolve-SPFRecordRecursively -domain $Matches[1] }
            '^a$'           { $ips += Resolve-HostToIPs -hostname $domain }
            '^mx$'          { $ips += Resolve-MXToIPs -domain $domain }
            '^a:(.+)'       { $ips += Resolve-HostToIPs -hostname $Matches[1] }
            '^mx:(.+)'      { $ips += Resolve-MXToIPs -domain $Matches[1] }
        }
    }

    return $ips
}

function Resolve-HostToIPs {
    param (
        [string]$hostname
    )
    $resolved = @()
    try {
        $aRecords = Resolve-DnsName -Name $hostname -Type A -ErrorAction Stop
        $resolved += $aRecords.IPAddress
    } catch {}
    try {
        $aaaaRecords = Resolve-DnsName -Name $hostname -Type AAAA -ErrorAction Stop
        $resolved += $aaaaRecords.IPAddress
    } catch {}
    return $resolved
}

function Resolve-MXToIPs {
    param (
        [string]$domain
    )
    $resolved = @()
    try {
        $mxRecords = Resolve-DnsName -Name $domain -Type MX -ErrorAction Stop
        foreach ($mx in $mxRecords) {
            $resolved += Resolve-HostToIPs -hostname $mx.NameExchange
        }
    } catch {}
    return $resolved
}

# Main processing
if (-Not (Test-Path $CsvPath)) {
    Write-Error "CSV file not found: $CsvPath"
    exit 1
}

$csvData = Import-Csv -Path $CsvPath
$allIPs = @()

foreach ($row in $csvData) {
    if ($row.ip) {
        $allIPs += $row.ip
    }

    if ($row.hostname) {
        $allIPs += Resolve-SPFRecordRecursively -domain $row.hostname
    }
}

# Clean and format
$allIPs = $allIPs | Where-Object { $_ -match '\S' } | Sort-Object -Unique
$ip4List = $allIPs | Where-Object { $_ -match '^\d{1,3}(\.\d{1,3}){3}(\/\d{1,2})?$' }
$ip6List = $allIPs | Where-Object { $_ -match ':' }

$spfParts = @("v=spf1")
$spfParts += $ip4List | ForEach-Object { "ip4:$_" }
$spfParts += $ip6List | ForEach-Object { "ip6:$_" }
$spfParts += "~all"

$flattenedSPF = $spfParts -join " "
Write-Output $flattenedSPF
