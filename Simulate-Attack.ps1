# Simulate-Attack.ps1
# This file will contain the core logic for the simulation tool.

function New-SimulationResult {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Command,

        [Parameter(Mandatory=$true)]
        [string]$Description,

        [Parameter(Mandatory=$true)]
        [string]$Severity,

        [Parameter(Mandatory=$true)]
        [string]$MitreAttackTag,

        [Parameter(Mandatory=$true)]
        [bool]$Succeeded,

        [Parameter(Mandatory=$false)]
        [string]$ErrorMessage
    )

    [PSCustomObject]@{ 
        Command = $Command
        Description = $Description
        Severity = $Severity
        MitreAttackTag = $MitreAttackTag
        Succeeded = $Succeeded
        ErrorMessage = $ErrorMessage
    }
}

function ConvertTo-SimulationReportHtml {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [array]$SimulationResults
    )

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $totalTests = $SimulationResults.Count
    $successCount = ($SimulationResults | Where-Object { $_.Succeeded }).Count
    $failureCount = $totalTests - $successCount
    $successRate = [math]::Round(($successCount / $totalTests) * 100, 2)

    $html = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Attack Simulation Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }

        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .success { color: #27ae60; }
        .failure { color: #e74c3c; }
        .total { color: #3498db; }
        .rate { color: #9b59b6; }

        .filters {
            padding: 20px 30px;
            background: white;
            border-bottom: 1px solid #eee;
        }

        .filter-group {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 8px 16px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }

        .filter-btn:hover, .filter-btn.active {
            background: #3498db;
            color: white;
            border-color: #3498db;
        }

        .table-container {
            padding: 30px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        th {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            padding: 15px 12px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85em;
        }

        td {
            padding: 15px 12px;
            border-bottom: 1px solid #eee;
            vertical-align: top;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .command-cell {
            font-family: 'Courier New', monospace;
            background: #f1f2f6;
            padding: 8px;
            border-radius: 5px;
            font-size: 0.9em;
            max-width: 300px;
            word-break: break-all;
        }

        .severity-badge {
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .severity-critical { background: #e74c3c; color: white; }
        .severity-high { background: #f39c12; color: white; }
        .severity-medium { background: #f1c40f; color: #333; }
        .severity-low { background: #3498db; color: white; }
        .severity-informational { background: #95a5a6; color: white; }

        .status-badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }

        .status-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }

        .status-failure {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }

        .mitre-tag {
            font-family: 'Courier New', monospace;
            background: #2c3e50;
            color: white;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 0.8em;
        }

        .error-message {
            max-width: 200px;
            font-size: 0.85em;
            color: #666;
            word-break: break-word;
        }

        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
                padding: 20px;
                gap: 15px;
            }
            
            .table-container {
                padding: 20px;
            }
            
            th, td {
                padding: 10px 8px;
                font-size: 0.9em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Attack Simulation Report</h1>
            <p>Generated on $timestamp</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number total">$totalTests</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number success">$successCount</div>
                <div class="stat-label">Succeeded</div>
            </div>
            <div class="stat-card">
                <div class="stat-number failure">$failureCount</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number rate">$successRate%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>

        <div class="filters">
            <div class="filter-group">
                <span style="font-weight: bold;">Filter by:</span>
                <button class="filter-btn active" onclick="filterTable('all')">All</button>
                <button class="filter-btn" onclick="filterTable('success')">Success</button>
                <button class="filter-btn" onclick="filterTable('failure')">Failure</button>
                <button class="filter-btn" onclick="filterTable('critical')">Critical</button>
                <button class="filter-btn" onclick="filterTable('high')">High</button>
            </div>
        </div>

        <div class="table-container">
            <table id="resultsTable">
                <thead>
                    <tr>
                        <th>Command</th>
                        <th>Description</th>
                        <th>Severity</th>
                        <th>MITRE ATT&CK</th>
                        <th>Status</th>
                        <th>Error Message</th>
                    </tr>
                </thead>
                <tbody>
"@

    foreach ($result in $SimulationResults) {
        $statusClass = if ($result.Succeeded) { 'status-success' } else { 'status-failure' }
        $statusText = if ($result.Succeeded) { 'Succeeded' } else { 'Failed' }
        $errorMessage = if ($result.ErrorMessage) { [System.Web.HttpUtility]::HtmlEncode($result.ErrorMessage) } else { '-' }
        $severityClass = "severity-" + $result.Severity.ToLower()
        $rowClass = if ($result.Succeeded) { 'success-row' } else { 'failure-row' }
        $rowClass += " severity-" + $result.Severity.ToLower() + "-row"
        
        $html += @"
                    <tr class="$rowClass">
                        <td><div class="command-cell">$([System.Web.HttpUtility]::HtmlEncode($result.Command))</div></td>
                        <td>$([System.Web.HttpUtility]::HtmlEncode($result.Description))</td>
                        <td><span class="severity-badge $severityClass">$($result.Severity)</span></td>
                        <td><span class="mitre-tag">$([System.Web.HttpUtility]::HtmlEncode($result.MitreAttackTag))</span></td>
                        <td><span class="status-badge $statusClass">$statusText</span></td>
                        <td><div class="error-message">$errorMessage</div></td>
                    </tr>
"@
    }

    $html += @"
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function filterTable(filter) {
            const table = document.getElementById('resultsTable');
            const rows = table.getElementsByTagName('tr');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // Update active button
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            // Filter rows
            for (let i = 1; i < rows.length; i++) {
                const row = rows[i];
                let show = false;
                
                switch(filter) {
                    case 'all':
                        show = true;
                        break;
                    case 'success':
                        show = row.classList.contains('success-row');
                        break;
                    case 'failure':
                        show = row.classList.contains('failure-row');
                        break;
                    case 'critical':
                        show = row.classList.contains('severity-critical-row');
                        break;
                    case 'high':
                        show = row.classList.contains('severity-high-row');
                        break;
                }
                
                row.style.display = show ? '' : 'none';
            }
        }
    </script>
</body>
</html>
"@

    return $html
}

function Invoke-SimulationCommand {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Command,

        [Parameter(Mandatory=$true)]
        [string]$Description,

        [Parameter(Mandatory=$true)]
        [string]$Severity,

        [Parameter(Mandatory=$true)]
        [string]$MitreAttackTag
    )

    Write-Host "Running command: $Command" -ForegroundColor Cyan
    $succeeded = $false
    $errorMessage = ""

    try {
        # Execute the command and capture output and errors
        $output = Invoke-Expression -Command $Command 2>&1

        # Check for errors in the output
        if ($LASTEXITCODE -ne 0 -or $output -is [System.Management.Automation.ErrorRecord] -or ($output | Out-String) -match "Program 'net.exe' failed to run: Access is denied") {
            $succeeded = $false
            $errorMessage = $output | Out-String
        } elseif (($output | Out-String) -match "This script contains malicious content and has been blocked by your antivirus software") {
            $succeeded = $false
            $errorMessage = "ERROR MESSAGE: Blocked By EDR"
        } else {
            $succeeded = $true
        }
    } catch {
        $succeeded = $false
        $errorMessage = $_.Exception.Message
    }

    New-SimulationResult -Command $Command -Description $Description -Severity $Severity -MitreAttackTag $MitreAttackTag -Succeeded $succeeded -ErrorMessage $errorMessage
}

function Start-AttackSimulation {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$false)]
        [string]$ConfigPath = "c:/commands.json",

        [Parameter(Mandatory=$false)]
        [string]$OutputPath = "c:/simulation_report.html"
    )

    Write-Host "Starting Attack Simulation..." -ForegroundColor Green

    # Load commands from configuration file
    if (-not (Test-Path $ConfigPath)) {
        Write-Error "Configuration file not found: $ConfigPath"
        return
    }

    $commands = Get-Content $ConfigPath | ConvertFrom-Json
    $results = @()

    foreach ($cmd in $commands) {
        $result = Invoke-SimulationCommand -Command $cmd.Command -Description $cmd.Description -Severity $cmd.Severity -MitreAttackTag $cmd.MitreAttackTag
        $results += $result
    }

    # Generate HTML report
    $htmlReport = ConvertTo-SimulationReportHtml -SimulationResults $results
    $htmlReport | Out-File -FilePath $OutputPath -Encoding UTF8

    Write-Host "Simulation completed. Report saved to: $OutputPath" -ForegroundColor Green
    
    return $results
}

Start-AttackSimulation


