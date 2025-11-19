#!/bin/bash
# Quick script to analyze Oracle RDS storage growth

INSTANCE=$1
REGION=${2:-us-west-2}

if [ -z "$INSTANCE" ]; then
    echo "Usage: $0 <instance-id> [region]"
    exit 1
fi

echo "======================================================================"
echo "Oracle RDS Storage Growth Analysis: $INSTANCE"
echo "Region: $REGION"
echo "======================================================================"
echo ""

# Get allocated storage
ALLOCATED_GB=$(aws rds describe-db-instances \
    --region "$REGION" \
    --db-instance-identifier "$INSTANCE" \
    --query 'DBInstances[0].AllocatedStorage' \
    --output text 2>/dev/null)

if [ -z "$ALLOCATED_GB" ]; then
    echo "Error: Could not retrieve instance information"
    exit 1
fi

echo "Allocated Storage: $ALLOCATED_GB GB"
echo ""

# Calculate time range (365 days ago)
if date -v-365d +"%Y-%m-%dT%H:%M:%S" >/dev/null 2>&1; then
    START_TIME=$(date -u -v-365d +"%Y-%m-%dT%H:%M:%S")
else
    START_TIME=$(date -u -d "365 days ago" +"%Y-%m-%dT%H:%M:%S")
fi
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S")

echo "Time Range: $START_TIME to $END_TIME"
echo ""

# Get metrics
echo "Fetching CloudWatch metrics..."
METRICS_JSON=$(aws cloudwatch get-metric-statistics \
    --region "$REGION" \
    --namespace AWS/RDS \
    --metric-name FreeStorageSpace \
    --dimensions Name=DBInstanceIdentifier,Value="$INSTANCE" \
    --start-time "$START_TIME" \
    --end-time "$END_TIME" \
    --period 86400 \
    --statistics Average \
    --output json 2>/dev/null)

if [ -z "$METRICS_JSON" ] || [ "$METRICS_JSON" = "null" ]; then
    echo "Error: No metrics data found"
    exit 1
fi

# Process with Python for calculations
python3 <<EOF
import json
import sys
from datetime import datetime

data = json.loads('''$METRICS_JSON''')
datapoints = data.get('Datapoints', [])

if not datapoints:
    print("No data points found")
    sys.exit(1)

# Sort by timestamp
datapoints.sort(key=lambda x: x['Timestamp'])

# Convert bytes to GB
allocated_gb = float($ALLOCATED_GB)
allocated_bytes = allocated_gb * (1024**3)

# Calculate first and last
first = datapoints[0]
last = datapoints[-1]

first_free_bytes = first['Average']
last_free_bytes = last['Average']

first_free_gb = first_free_bytes / (1024**3)
last_free_gb = last_free_bytes / (1024**3)

first_used_gb = (allocated_bytes - first_free_bytes) / (1024**3)
last_used_gb = (allocated_bytes - last_free_bytes) / (1024**3)

growth_gb = last_used_gb - first_used_gb
growth_percent = (growth_gb / first_used_gb * 100) if first_used_gb > 0 else 0

# Calculate days
first_date = datetime.fromisoformat(first['Timestamp'].replace('Z', '+00:00'))
last_date = datetime.fromisoformat(last['Timestamp'].replace('Z', '+00:00'))
days_diff = (last_date - first_date).days

months = days_diff / 30.0
growth_per_month = growth_gb / months if months > 0 else 0

# Projection
current_free_gb = last_free_gb
months_until_full = current_free_gb / growth_per_month if growth_per_month > 0 else float('inf')

print("=" * 70)
print("STORAGE GROWTH SUMMARY")
print("=" * 70)
print("")
print(f"Analysis Period: {first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}")
print(f"Days Analyzed: {days_diff} days")
print(f"Data Points: {len(datapoints)}")
print("")
print(f"Allocated Storage: {allocated_gb:.2f} GB")
print("")
print("Initial Usage:")
print(f"  Used: {first_used_gb:>12.2f} GB ({100-first_free_gb/allocated_gb*100:.1f}% used)")
print(f"  Free: {first_free_gb:>12.2f} GB ({first_free_gb/allocated_gb*100:.1f}% free)")
print("")
print("Final Usage:")
print(f"  Used: {last_used_gb:>12.2f} GB ({100-last_free_gb/allocated_gb*100:.1f}% used)")
print(f"  Free: {last_free_gb:>12.2f} GB ({last_free_gb/allocated_gb*100:.1f}% free)")
print("")
print("Growth:")
print(f"  Total Growth:    {growth_gb:>12.2f} GB")
print(f"  Growth Percent:  {growth_percent:>12.2f}%")
print(f"  Avg Growth/Month: {growth_per_month:>10.2f} GB")
print("")

if growth_per_month > 0 and months_until_full != float('inf'):
    print("Projection:")
    if months_until_full > 0:
        print(f"  Estimated time until storage full: {months_until_full:.1f} months ({months_until_full/12:.1f} years)")
    else:
        print("  Storage may be stable or shrinking")
print("")

# Show monthly snapshots
print("Monthly Snapshot (first day of each month):")
print("-" * 70)
print(f"{'Date':<12} {'Used (GB)':>12} {'Free (GB)':>12} {'Usage %':>10}")
print("-" * 70)

current_month = None
for point in datapoints:
    timestamp = datetime.fromisoformat(point['Timestamp'].replace('Z', '+00:00'))
    point_month = timestamp.strftime('%Y-%m')
    
    if point_month != current_month:
        free_bytes = point['Average']
        free_gb = free_bytes / (1024**3)
        used_gb = (allocated_bytes - free_bytes) / (1024**3)
        used_pct = (used_gb / allocated_gb * 100) if allocated_gb > 0 else 0
        
        print(f"{timestamp.strftime('%Y-%m-%d'):<12} {used_gb:>12.2f} {free_gb:>12.2f} {used_pct:>9.2f}%")
        current_month = point_month

EOF

echo ""
echo "======================================================================"

