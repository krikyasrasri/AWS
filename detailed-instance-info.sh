#!/bin/bash
# detailed-oracle-report.sh

REGION="us-west-2"
OUTPUT="detailed-oracle-report.html"

# Create HTML header
cat > $OUTPUT << EOF
<html>
<head>
<title>Oracle RDS Detailed Report</title>
<style>
body { font-family: Arial, sans-serif; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #4CAF50; color: white; }
tr:nth-child(even) { background-color: #f2f2f2; }
h2 { color: #333; }
.section { margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50; }
</style>
</head>
<body>
<h1>Oracle RDS Detailed Configuration Report</h1>
<p>Generated: $(date)</p>
EOF

# Get instance list
##INSTANCES=$(aws rds describe-db-instances --region $REGION --query "DBInstances[?Engine=='oracle-*'].DBInstanceIdentifier" --output text)
##INSTANCES=$(aws rds describe-db-instances --region $REGION --query "DBInstances[?starts_with(Engine, 'oracle')].DBInstanceIdentifier" --output text)

INSTANCES=$(aws rds describe-db-instances --region $REGION --query "DBInstances[?starts_with(Engine, 'oracle') || Engine=='aurora-postgresql' || Engine=='mysql' || Engine=='mariadb'].DBInstanceIdentifier" --output text)

for INSTANCE in $INSTANCES; do
    echo "<div class='section'>" >> $OUTPUT
    echo "<h2>Instance: $INSTANCE</h2>" >> $OUTPUT

    # Get detailed instance information
    aws rds describe-db-instances \
        --region $REGION \
        --db-instance-identifier $INSTANCE \
        --query 'DBInstances[0]' > /tmp/instance.json

    # Convert to HTML table
    echo "<table>" >> $OUTPUT
    jq -r 'to_entries | .[] | "<tr><td><strong>\(.key)</strong></td><td>\(.value)</td></tr>"' /tmp/instance.json >> $OUTPUT
    echo "</table>" >> $OUTPUT

    echo "</div>" >> $OUTPUT
done

echo "</body></html>" >> $OUTPUT
echo "Report generated: $OUTPUT"