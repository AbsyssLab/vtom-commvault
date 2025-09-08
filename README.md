# CommVault Integration with Visual TOM
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE.md)&nbsp;
[![en](https://img.shields.io/badge/lang-en-green.svg)](readme_github.md)  
This project enables the integration of CommVault backup operations with the Visual TOM scheduler.

The integration provides a comprehensive solution for launching and monitoring CommVault backup jobs through Visual TOM, supporting both Windows and Linux environments.

## Features

The integration supports the following operations:
  * Launch backup jobs for specific clients and backup sets
  * Monitor job execution status in real-time
  * Support for subclient-specific backups
  * Multiple authentication methods (command line, environment variables, configuration files)
  * Configurable monitoring intervals and timeouts
  * Detailed execution reports
  * Cross-platform support (Windows/Linux)

## Disclaimer
No Support and No Warranty are provided by Absyss SAS for this project and related material. The use of this project's files is at your own risk.
Absyss SAS assumes no liability for damage caused by the usage of any of the files offered here via this Github repository.
Consulting days can be requested to help for the implementation.

## Prerequisites

  * Visual TOM 7.1.2 or higher
  * Python 3.x or higher
  * CommVault server with REST API access
  * Network connectivity to CommVault server
  * Valid CommVault user credentials with backup permissions

## Installation

1. Copy the integration files to your Visual TOM binary directory (`%ABM_BIN%` on Windows or `${ABM_BIN}` on Linux)
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Import the application model (`commvault_modele.xml`) into Visual TOM
4. Configure authentication (see Authentication section below)

## Authentication

The integration supports multiple authentication methods:

### Method 1: Command Line Arguments
```bash
python commvault_backup.py --host commvault.company.com --username admin --password secret --client "SERVER01" --backup-set "DefaultBackupSet"
```

### Method 2: Environment Variables
```bash
export COMMVAULT_USERNAME=admin
export COMMVAULT_PASSWORD=secret
python commvault_backup.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet"
```

### Method 3: Configuration File
Create an `auth.conf` file based on `auth.conf.example`:
```ini
[Authentication]
username = your_commvault_username
password = your_commvault_password
```

Then use:
```bash
python commvault_backup.py --host commvault.company.com --config-file auth.conf --client "SERVER01" --backup-set "DefaultBackupSet"
```

## Usage Guidelines

### Visual TOM Integration

The application model should be imported into Visual TOM. The Visual TOM job must be executed from a machine with network access to the CommVault server.

### Required Parameters

- **Host**: CommVault server hostname or IP address
- **Client**: Name of the client to backup
- **Backup Set**: Name of the backup set to execute

### Optional Parameters

- **Port**: CommVault server port (default: 8400)
- **Use SSL**: Enable SSL/TLS connection (default: true)
- **Subclient**: Specific subclient name (optional)
- **Username/Password**: Authentication credentials
- **Config File**: Path to authentication configuration file
- **Check Interval**: Status check interval in seconds (default: 30)
- **Timeout**: Maximum wait time in seconds (default: 3600)
- **Verbose**: Enable detailed logging

## Examples

### Direct Python Execution

```bash
# Basic backup with authentication prompt
python commvault_backup.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet"

# Backup with specific subclient
python commvault_backup.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --subclient "Database"

# Backup with custom monitoring settings
python commvault_backup.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --check-interval 60 --timeout 7200

# Verbose logging
python commvault_backup.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --verbose
```

### Visual TOM Queue Execution

#### Windows
```batch
submit_queue_commvault.bat "commvault.company.com" "SERVER01" "DefaultBackupSet" "8400" "true" "" "admin" "secret" "" "30" "3600" "false"
```

#### Linux
```bash
tom_submit.commvault "commvault.company.com" "SERVER01" "DefaultBackupSet" "8400" "true" "" "admin" "secret" "" "30" "3600" "false"
```

## Exit Codes

The script returns the following exit codes:
- **0**: Success - Job completed successfully
- **1**: Authentication error
- **2**: Job execution error
- **3**: Timeout error
- **4**: Status check error
- **5**: Invalid arguments
- **6**: User interruption (Ctrl+C)

## Configuration Files

### Arguments.json
Contains the parameter definitions for Visual TOM integration, including parameter types, descriptions, and default values.

### commvault_modele.xml
Visual TOM application model that defines the custom job type with all required fields and their properties.

## Monitoring and Reporting

The integration provides comprehensive monitoring capabilities:

- Real-time job status monitoring
- Configurable check intervals
- Automatic timeout handling
- Detailed execution reports including:
  - Job ID and status
  - Start and end times
  - Duration
  - Files and bytes processed
  - Error messages (if any)

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify CommVault server connectivity
   - Check username/password credentials
   - Ensure user has backup permissions

2. **Connection Issues**
   - Verify hostname/IP and port
   - Check SSL/TLS settings
   - Ensure network connectivity

3. **Job Execution Failures**
   - Verify client name exists in CommVault
   - Check backup set configuration
   - Review CommVault server logs

### Debug Mode

Enable verbose logging for detailed troubleshooting:
```bash
python commvault_backup.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --verbose
```

## License
This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details

## Code of Conduct
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.1%20adopted-ff69b4.svg)](code-of-conduct.md)  
Absyss SAS has adopted the [Contributor Covenant](CODE_OF_CONDUCT.md) as its Code of Conduct, and we expect project participants to adhere to it. Please read the [full text](CODE_OF_CONDUCT.md) so that you can understand what actions will and will not be tolerated.
