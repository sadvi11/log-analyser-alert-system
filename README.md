# Log Analyser + Alert System

A Python script that connects to AWS CloudWatch, scans log groups for errors, and saves an alert report.

## Tech Stack
- Python 3
- boto3 (AWS SDK)
- AWS CloudWatch Logs

## What It Does
- Connects to AWS CloudWatch using boto3
- Scans all log groups from last 24 hours
- Detects ERROR, CRITICAL, Exception, Failed keywords
- Alerts when errors are found
- Saves full report to log_report.json

## How to Run

1. Install dependencies: pip install -r requirements.txt
2. Configure AWS: aws configure
3. Run the script: python3 log_analyser.py

## Sample Output
Starting Log Analyser...
Connecting to AWS CloudWatch...
Found 1 log groups
Analysing: /myapp/test-logs
ALERT! Found 2 errors in /myapp/test-logs
Report saved to log_report.json
Total errors found: 2

## Author
Sadhvi - Cloud Engineer | AWS Certified Solutions Architect