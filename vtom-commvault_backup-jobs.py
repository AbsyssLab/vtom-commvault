#!/usr/bin/env python3
"""
CommVault Backup Controller Script

This script provides integration with CommVault to launch and monitor backup operations.
It supports authentication via command line arguments, environment variables, or configuration files.

Author: CommVault Integration Team
Version: 1.0
"""

import argparse
import json
import logging
import os
import sys
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import configparser
import getpass


class CommVaultBackupController:
    """Main class for CommVault backup operations."""
    
    def __init__(self, host: str, port: int = 8400, use_ssl: bool = True):
        """
        Initialize the CommVault backup controller.
        
        Args:
            host: CommVault server hostname or IP
            port: CommVault server port (default: 8400)
            use_ssl: Whether to use SSL/TLS (default: True)
        """
        self.host = host
        self.port = port
        self.protocol = "https" if use_ssl else "http"
        self.base_url = f"{self.protocol}://{host}:{port}"
        self.session = requests.Session()
        self.session.verify = use_ssl
        self.auth_token = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger('CommVaultBackup')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticate with CommVault server.
        
        Args:
            username: CommVault username
            password: CommVault password
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            auth_url = f"{self.base_url}/Login"
            auth_data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(auth_url, json=auth_data, timeout=30)
            
            if response.status_code == 200:
                auth_response = response.json()
                if auth_response.get('isAuthenticated'):
                    self.auth_token = auth_response.get('token')
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.auth_token}',
                        'Content-Type': 'application/json'
                    })
                    self.logger.info("Authentication successful")
                    return True
                else:
                    self.logger.error("Authentication failed: Invalid credentials")
                    return False
            else:
                self.logger.error(f"Authentication failed: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Authentication error: {e}")
            return False
    
    def launch_backup(self, client_name: str, backup_set: str, 
                     subclient_name: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        """
        Launch a backup job.
        
        Args:
            client_name: Name of the client to backup
            backup_set: Name of the backup set
            subclient_name: Name of the subclient (optional)
            
        Returns:
            Tuple[int, Dict]: Job ID and job details
        """
        try:
            backup_url = f"{self.base_url}/Backup"
            backup_data = {
                "clientName": client_name,
                "backupSetName": backup_set,
                "subclientName": subclient_name if subclient_name else "",
                "jobType": "BACKUP"
            }
            
            response = self.session.post(backup_url, json=backup_data, timeout=30)
            
            if response.status_code == 200:
                job_info = response.json()
                job_id = job_info.get('jobId')
                self.logger.info(f"Backup job launched successfully. Job ID: {job_id}")
                return job_id, job_info
            else:
                self.logger.error(f"Failed to launch backup: HTTP {response.status_code}")
                return -1, {}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error launching backup: {e}")
            return -1, {}
    
    def get_job_status(self, job_id: int) -> Dict[str, Any]:
        """
        Get the status of a backup job.
        
        Args:
            job_id: Job ID to check
            
        Returns:
            Dict: Job status information
        """
        try:
            status_url = f"{self.base_url}/Job/{job_id}"
            response = self.session.get(status_url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"Failed to get job status: HTTP {response.status_code}")
                return {}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting job status: {e}")
            return {}
    
    def wait_for_job_completion(self, job_id: int, check_interval: int = 30, 
                               timeout: int = 3600) -> Tuple[int, Dict[str, Any]]:
        """
        Wait for job completion with status monitoring.
        
        Args:
            job_id: Job ID to monitor
            check_interval: Interval in seconds between status checks
            timeout: Maximum time to wait in seconds
            
        Returns:
            Tuple[int, Dict]: Exit code and final job status
        """
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                self.logger.error(f"Job {job_id} timed out after {timeout} seconds")
                return 3, {}  # Timeout error code
            
            job_status = self.get_job_status(job_id)
            if not job_status:
                return 4, {}  # Status check error code
            
            status = job_status.get('status', 'UNKNOWN')
            self.logger.info(f"Job {job_id} status: {status}")
            
            if status in ['COMPLETED', 'SUCCESS']:
                self.logger.info(f"Job {job_id} completed successfully")
                return 0, job_status
            elif status in ['FAILED', 'ERROR', 'ABORTED']:
                self.logger.error(f"Job {job_id} failed with status: {status}")
                return 2, job_status  # Job failure error code
            
            time.sleep(check_interval)
    
    def generate_report(self, job_id: int, job_status: Dict[str, Any]) -> str:
        """
        Generate a detailed execution report.
        
        Args:
            job_id: Job ID
            job_status: Final job status information
            
        Returns:
            str: Formatted report
        """
        report = []
        report.append("=" * 60)
        report.append("COMMVAULT BACKUP EXECUTION REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Job ID: {job_id}")
        report.append(f"Status: {job_status.get('status', 'UNKNOWN')}")
        report.append(f"Start Time: {job_status.get('startTime', 'N/A')}")
        report.append(f"End Time: {job_status.get('endTime', 'N/A')}")
        report.append(f"Duration: {job_status.get('duration', 'N/A')}")
        report.append(f"Files Processed: {job_status.get('filesProcessed', 'N/A')}")
        report.append(f"Bytes Processed: {job_status.get('bytesProcessed', 'N/A')}")
        report.append(f"Error Message: {job_status.get('errorMessage', 'None')}")
        report.append("=" * 60)
        
        return "\n".join(report)


def load_auth_from_file(config_file: str) -> Tuple[str, str]:
    """
    Load authentication credentials from configuration file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Tuple[str, str]: Username and password
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    
    username = config.get('Authentication', 'username', fallback='')
    password = config.get('Authentication', 'password', fallback='')
    
    return username, password


def get_credentials(username: Optional[str] = None, 
                   password: Optional[str] = None,
                   config_file: Optional[str] = None) -> Tuple[str, str]:
    """
    Get authentication credentials from various sources.
    
    Args:
        username: Username from command line
        password: Password from command line
        config_file: Configuration file path
        
    Returns:
        Tuple[str, str]: Username and password
    """
    # Try environment variables first
    env_username = os.environ.get('COMMVAULT_USERNAME')
    env_password = os.environ.get('COMMVAULT_PASSWORD')
    
    # Try configuration file
    if config_file and os.path.exists(config_file):
        file_username, file_password = load_auth_from_file(config_file)
    else:
        file_username = file_password = None
    
    # Use command line arguments if provided
    final_username = username or env_username or file_username
    final_password = password or env_password or file_password
    
    # Prompt for credentials if not available
    if not final_username:
        final_username = input("Enter CommVault username: ")
    
    if not final_password:
        final_password = getpass.getpass("Enter CommVault password: ")
    
    return final_username, final_password


def main():
    """Main function to handle command line execution."""
    parser = argparse.ArgumentParser(
        description="CommVault Backup Controller - Launch and monitor backup operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic backup with authentication prompt
  python commvault_backup_controller.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet"
  
  # Backup with command line authentication
  python commvault_backup_controller.py --host commvault.company.com --username admin --password secret --client "SERVER01" --backup-set "DefaultBackupSet"
  
  # Backup using environment variables
  export COMMVAULT_USERNAME=admin
  export COMMVAULT_PASSWORD=secret
  python commvault_backup_controller.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet"
  
  # Backup using configuration file
  python commvault_backup_controller.py --host commvault.company.com --config-file auth.conf --client "SERVER01" --backup-set "DefaultBackupSet"
  
  # Backup with custom monitoring interval
  python commvault_backup_controller.py --host commvault.company.com --client "SERVER01" --backup-set "DefaultBackupSet" --check-interval 60

Environment Variables:
  COMMVAULT_USERNAME: CommVault username
  COMMVAULT_PASSWORD: CommVault password

Configuration File Format (auth.conf):
  [Authentication]
  username = your_username
  password = your_password

Exit Codes:
  0: Success
  1: Authentication error
  2: Job execution error
  3: Timeout error
  4: Status check error
  5: Invalid arguments
        """
    )
    
    # Required arguments
    parser.add_argument('--host', required=True, help='CommVault server hostname or IP address')
    parser.add_argument('--client', required=True, help='Client name to backup')
    parser.add_argument('--backup-set', required=True, help='Backup set name')
    
    # Optional arguments
    parser.add_argument('--port', type=int, default=8400, help='CommVault server port (default: 8400)')
    parser.add_argument('--use-ssl', action='store_true', default=True, help='Use SSL/TLS connection (default: True)')
    parser.add_argument('--subclient', help='Subclient name (optional)')
    parser.add_argument('--username', help='CommVault username')
    parser.add_argument('--password', help='CommVault password')
    parser.add_argument('--config-file', help='Configuration file path for authentication')
    parser.add_argument('--check-interval', type=int, default=30, help='Status check interval in seconds (default: 30)')
    parser.add_argument('--timeout', type=int, default=3600, help='Maximum wait time in seconds (default: 3600)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger('CommVaultBackup').setLevel(logging.DEBUG)
    
    try:
        # Initialize controller
        controller = CommVaultBackupController(
            host=args.host,
            port=args.port,
            use_ssl=args.use_ssl
        )
        
        # Get authentication credentials
        username, password = get_credentials(
            username=args.username,
            password=args.password,
            config_file=args.config_file
        )
        
        # Authenticate
        if not controller.authenticate(username, password):
            print("Authentication failed", file=sys.stderr)
            sys.exit(1)
        
        # Launch backup
        job_id, job_info = controller.launch_backup(
            client_name=args.client,
            backup_set=args.backup_set,
            subclient_name=args.subclient
        )
        
        if job_id == -1:
            print("Failed to launch backup job", file=sys.stderr)
            sys.exit(2)
        
        # Wait for completion
        exit_code, final_status = controller.wait_for_job_completion(
            job_id=job_id,
            check_interval=args.check_interval,
            timeout=args.timeout
        )
        
        # Generate and print report
        report = controller.generate_report(job_id, final_status)
        print(report)
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(6)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(5)


if __name__ == "__main__":
    main() 