import boto3
import json
from datetime import datetime, timedelta

# Keywords to watch for in logs
ERROR_KEYWORDS = ['ERROR', 'error', 'Exception', 'CRITICAL', 'failed', 'Failed']

def get_log_groups():
    client = boto3.client('logs', region_name='ca-central-1')
    response = client.describe_log_groups()
    groups = [group['logGroupName'] for group in response['logGroups']]
    return groups

def analyse_logs(log_group_name):
    client = boto3.client('logs', region_name='ca-central-1')
    
    # Get logs from last 24 hours
    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(hours=24)).timestamp() * 1000)
    
    try:
        response = client.filter_log_events(
            logGroupName=log_group_name,
            startTime=start_time,
            endTime=end_time
        )
        
        events = response.get('events', [])
        errors_found = []
        
        for event in events:
            message = event['message']
            for keyword in ERROR_KEYWORDS:
                if keyword in message:
                    errors_found.append({
                        'timestamp': str(datetime.fromtimestamp(event['timestamp'] / 1000)),
                        'message': message.strip()
                    })
                    break
        
        return errors_found
    
    except Exception as e:
        print(f"Could not read {log_group_name}: {e}")
        return []

def run_analyser():
    print("Starting Log Analyser...")
    print("Connecting to AWS CloudWatch...")
    
    log_groups = get_log_groups()
    
    if not log_groups:
        print("No log groups found in this region.")
        return
    
    print(f"Found {len(log_groups)} log groups")
    
    all_errors = []
    
    for group in log_groups:
        print(f"Analysing: {group}")
        errors = analyse_logs(group)
        if errors:
            print(f"ALERT! Found {len(errors)} errors in {group}")
            all_errors.extend(errors)
        else:
            print(f"All clear in {group}")
    
    # Save report
    report = {
        'generated_at': str(datetime.now()),
        'total_errors': len(all_errors),
        'errors': all_errors
    }
    
    with open('log_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    print(f"\nReport saved to log_report.json")
    print(f"Total errors found: {len(all_errors)}")

run_analyser()