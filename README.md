# Attack Simulation Tool
![image](https://github.com/user-attachments/assets/1f61574a-71db-4e59-950e-01088a7efc3f)

This project provides a PowerShell script to simulate various attack commands and generate a comprehensive HTML report of the simulation results. It's designed to help security professionals and system administrators test their defenses against common attack techniques and identify potential vulnerabilities.

## Features

- **Automated Command Extraction**: Automatically extracts attack commands from the LOLBAS project (Living Off The Land Binaries and Scripts) YAML files, categorizing them by Command, Description, Severity, and MITRE ATT&CK Tag.
- **Configurable Attack Scenarios**: Define a list of commands to simulate in a JSON configuration file (`commands.json`). This file is automatically populated from the LOLBAS project data.
- **Detailed Reporting**: Generates an interactive HTML report with:
    - Overall success/failure statistics.
    - Filterable table of individual command execution results.
    - Command, description, severity, MITRE ATT&CK tag, status (succeeded/failed), and error messages.
- **Error Handling**: Captures command output and errors, including specific handling for antivirus blocking.
- **MITRE ATT&CK Mapping**: Each simulated command is mapped to a relevant MITRE ATT&CK technique for better context and understanding of the simulated threat.

## Getting Started

### Prerequisites

- PowerShell 7 or higher (PowerShell Core).
- Python 3.x
- Git (for cloning the LOLBAS project)

### Installation

1. Clone the LOLBAS project repository:
   ```bash
   git clone https://github.com/LOLBAS-Project/LOLBAS-Project.git
   ```
2. Install Python dependencies:
   ```bash
   pip install pyyaml GitPython
   ```

## Usage

First, run the `main.py` script to parse the LOLBAS project and populate `commands.json`:

```bash
python3 main.py
```

To run the attack simulation, execute the PowerShell script:

```powershell
pwsh -ExecutionPolicy Bypass -File .\Simulate-Attack.ps1
```

By default, the script will look for `commands.json` in the same directory and generate `simulation_report.html` in `c:\`.

### Parameters

You can specify custom paths for the configuration and output files:

- `-ConfigPath <path>`: Specifies the path to the JSON configuration file (default: `c:/commands.json`).
- `-OutputPath <path>`: Specifies the path where the HTML report will be saved (default: `c:/simulation_report.html`).

Example:

```powershell
.\Simulate-Attack.ps1 -ConfigPath "C:\Path\To\Your\commands.json" -OutputPath "C:\Path\To\Your\report.html"
```

## Configuration

The `commands.json` file defines the commands to be simulated. Each entry in the JSON array should have the following structure:

```json
{
    "Command": "<The command to execute>",
    "Description": "<A brief description of the command's purpose>",
    "Severity": "<Severity of the command (e.g., Low, Medium, High, Critical, Informational)>",
    "MitreAttackTag": "<Corresponding MITRE ATT&CK technique tag>"
}
```

### Example `commands.json` entry:

```json
{
    "Command": "net group \"Domain Admins\" /domain",
    "Description": "Enumerate Domain Admins group members.",
    "Severity": "Low",
    "MitreAttackTag": "T1069.002 - Permission Groups Discovery: Domain Groups"
}
```

## Report Structure

The generated `simulation_report.html` provides an overview of the simulation and detailed results for each command.

- **Header**: Displays the report title and generation timestamp.
- **Statistics**: Summary of total tests, succeeded, failed, and success rate.
- **Filters**: Buttons to filter results by status (All, Success, Failure) and severity (Critical, High).
- **Results Table**: A sortable table with the following columns:
    - **Command**: The executed command.
    - **Description**: Description of the command.
    - **Severity**: Severity level of the command.
    - **MITRE ATT&CK**: Associated MITRE ATT&CK technique.
    - **Status**: Indicates whether the command succeeded or failed.
    - **Error Message**: Details of any error encountered during execution.


