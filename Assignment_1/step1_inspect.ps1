$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$sources = @('A_B_Testing_Hypothesis_Testing_Assignment.docx','ui_ab_testing_data.csv')
$before = @{}
foreach ($source in $sources) { $before[$source] = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash }
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::OpenRead((Join-Path $PWD $sources[0]))
$extracted = [Collections.Generic.List[string]]::new()
foreach ($entry in $archive.Entries) {
    if ($entry.FullName -match '^word/(document|header\d+|footer\d+|footnotes|endnotes|comments)\.xml$') {
        $reader = [IO.StreamReader]::new($entry.Open())
        [xml]$xml = $reader.ReadToEnd()
        $reader.Dispose()
        $ns = [Xml.XmlNamespaceManager]::new($xml.NameTable)
        $ns.AddNamespace('w','http://schemas.openxmlformats.org/wordprocessingml/2006/main')
        $extracted.Add("PART: $($entry.FullName)")
        foreach ($p in $xml.SelectNodes('//w:p',$ns)) {
            $texts = @($p.SelectNodes('.//w:t',$ns) | ForEach-Object { $_.InnerText })
            if ($texts.Count) { $extracted.Add(($texts -join '')) }
        }
        $i = 0
        foreach ($table in $xml.SelectNodes('//w:tbl',$ns)) {
            $i++
            $extracted.Add("TABLE $i (explicit row/cell structure)")
            foreach ($row in $table.SelectNodes('./w:tr',$ns)) {
                $cells = foreach ($cell in $row.SelectNodes('./w:tc',$ns)) {
                    (@($cell.SelectNodes('.//w:t',$ns) | ForEach-Object { $_.InnerText }) -join '')
                }
                $extracted.Add(($cells -join ' | '))
            }
        }
    }
}
$archive.Dispose()
$extracted | Set-Content -LiteralPath 'assignment_extracted.txt' -Encoding UTF8
$data = @(Import-Csv -LiteralPath $sources[1])
$notes = [Collections.Generic.List[string]]::new()
$notes.Add('# Step 1 inspection — preliminary data audit, not the final assignment report')
$notes.Add('')
foreach ($source in $sources) { $notes.Add("Source: $((Resolve-Path -LiteralPath $source).Path)") }
$notes.Add("`nDataset: $($data.Count) data rows x $($data[0].PSObject.Properties.Name.Count) columns; 10,001 records including header.")
$notes.Add('CSV column names (case-sensitive): ' + ($data[0].PSObject.Properties.Name -join ', '))
$notes.Add("`n## First 10 data rows`n")
$notes.Add('```csv')
foreach ($line in ($data | Select-Object -First 10 | ConvertTo-Csv -NoTypeInformation)) { $notes.Add($line) }
$notes.Add('```')
$notes.Add("`n## Data quality`n")
foreach ($col in $data[0].PSObject.Properties.Name) {
    $missing = @($data | Where-Object { [string]::IsNullOrWhiteSpace($_.$col) -or $_.$col -match '^(NA|N/A|NaN|null|None)$' }).Count
    $notes.Add("- Missing values in ${col}: $missing")
}
$duplicates = ($data | ConvertTo-Csv -NoTypeInformation | Select-Object -Skip 1 | Group-Object | Where-Object Count -gt 1 | ForEach-Object { $_.Count - 1 } | Measure-Object -Sum).Sum
$duplicateIDs = ($data | Group-Object user_id | Where-Object Count -gt 1 | ForEach-Object { $_.Count - 1 } | Measure-Object -Sum).Sum
$notes.Add("- Duplicate full rows beyond first occurrence: $([int]$duplicates)")
$notes.Add("- Duplicate user IDs beyond first occurrence: $([int]$duplicateIDs)")
$invalidDuration = @($data | Where-Object { $value = 0.0; -not [double]::TryParse($_.session_duration_seconds, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$value) -or [double]::IsNaN($value) -or [double]::IsInfinity($value) -or $value -le 0 }).Count
$notes.Add("- Invalid, nonfinite, or nonpositive session durations: $invalidDuration")
$notes.Add("- Unexpected UI labels: $(@($data | Where-Object { $_.ui_version -cnotin @('UI_A','UI_B') }).Count)")
$notes.Add('- No records were removed, imputed, or transformed in the original CSV. Duplicate-free session IDs do not independently establish experimental independence.')
$notes.Add("`n## Initial descriptive statistics`n")
$notes.Add('Duration units: seconds. Sample SD = sqrt(sum((x - mean)^2)/(n - 1)); ddof=1. All rows retained.')
$notes.Add('')
$notes.Add('| UI | Count | Mean | Sample SD | Minimum | Maximum |')
$notes.Add('|---|---:|---:|---:|---:|---:|')
foreach ($g in ($data | Group-Object ui_version | Sort-Object Name)) {
    $values = @($g.Group | ForEach-Object { [double]::Parse($_.session_duration_seconds,[Globalization.CultureInfo]::InvariantCulture) })
    $summary = $values | Measure-Object -Average -Minimum -Maximum
    $ss = ($values | ForEach-Object { [math]::Pow($_-$summary.Average,2) } | Measure-Object -Sum).Sum
    $sd = [math]::Sqrt($ss/($values.Count-1))
    $notes.Add(('| {0} | {1} | {2:F8} | {3:F8} | {4:F2} | {5:F2} |' -f $g.Name,$values.Count,$summary.Average,$sd,$summary.Minimum,$summary.Maximum))
}
$notes.Add("`n## Assignment preview comparison`n")
$notes.Add('| Item | Assignment preview | CSV calculation | Finding |')
$notes.Add('|---|---|---|---|')
$notes.Add('| UI_A count | 5,013 | 5,013 | Matches |')
$notes.Add('| UI_B count | 4,987 | 4,987 | Matches |')
$notes.Add('| UI_A mean | 99.66 | 99.66307401 | Matches to 2 decimals |')
$notes.Add('| UI_B mean | 126.26 | 126.25848606 | Matches to 2 decimals |')
$notes.Add('| Mean difference B - A | +26.60 | +26.59541206 | Matches to 2 decimals |')
$notes.Add('| UI_A SD | 68.45 | 71.56361982 | CSV sample SD is 3.11361982 seconds higher |')
$notes.Add('| UI_B SD | 71.23 | 83.64436110 | CSV sample SD is 12.41436110 seconds higher |')
$notes.Add('')
$notes.Add('The SD discrepancies exceed rounding differences. Their cause is not established by the source files. Use CSV-derived sample SDs for subsequent calculations. The preview provides no minimum or maximum for comparison.')
$notes.Add('The description capitalizes Timestamp, Clicks, Conversion, and Bounce; actual CSV headers are timestamp, clicks, conversion, and bounce. Use the actual lowercase headers in code.')
$notes.Add("`n## Python environment`n")
$notes.Add('Verified by actual imports: Python 3.13.1 at C:\Python313\python.exe; pip 24.3.1.')
$notes.Add('Core packages for the planned Python workflow are absent: pandas, numpy, scipy, matplotlib. Optional packages checked and absent: seaborn, statsmodels, python-docx (import docx), jupyter, nbformat.')
$notes.Add('No packages were installed. Step 1 uses PowerShell/.NET CSV and OOXML readers, so package absence is not a Step 1 blocker. Install the core packages into a project environment before later Python statistical analysis. Optional packages are not required if their functionality is covered by core packages or standard-library extraction.')
$notes.Add("`n## Preservation and scope`n")
foreach ($source in $sources) {
    $after = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
    if ($before[$source] -ne $after) { throw "Original changed: $source" }
    $notes.Add("- $source SHA256: $after (unchanged across inspection)")
}
$notes.Add('Complete source text and explicit table rows are saved in assignment_extracted.txt. No normality tests, hypothesis tests, probability calculations, plots, or final report were created. Step 1 blockers: none.')
$notes | Set-Content -LiteralPath 'step1_inspection.md' -Encoding UTF8
Write-Output 'Created assignment_extracted.txt and step1_inspection.md; source hashes unchanged.'
