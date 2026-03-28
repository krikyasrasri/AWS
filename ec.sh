#!/bin/bash
# ============================================================
# Combined Standby & GoldenGate Health Check Script
# Environments: Revstream, SIEBEL, OBill, DBill (PROD)
# All output -> single combined log + Slack + Email
# ============================================================

CHANGE_REQUEST="CHG8176680"
KNOWN_HOSTS="/Users/srinivas/.ssh/known_hosts"
BASE_SCRIPT_DIR="/Users/srinivas/scripts"
COMBINED_LOG="/Users/srinivas/scripts/combined_gg_DG_health_check.log"

# ── Slack Configuration ───────────────────────────────────────
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX"
# SLACK_BOT_TOKEN="xoxb-your-bot-token"
# SLACK_CHANNEL="#your-channel-name"

# ── Email Configuration ───────────────────────────────────────
##EMAIL_TO="aaaaa5y67q5og4yzn3pgrjky6i@intuit.org.slack.com"
EMAIL_TO="t4imsedbteam-aaaaejwuunjjishtdjdsdjoikm@intuit.org.slack.com"
EMAIL_FROM="srinivas_pothu@intuit.com"
EMAIL_SUBJECT="PROD DB DataGurad and GoldenGate Health Check Report - $(date '+%Y-%m-%d %H:%M:%S')"
SMTP_HOST="smtp.com"
SMTP_PORT="587"
SMTP_USER="wnp2"
SMTP_PASS="test"

# ── ANSI colors (terminal only) ──────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Per-env status helpers (bash 3.x safe — no associative arrays) ──
set_env_status() { eval "ENV_STATUS_$(echo "$1" | tr ' ' '_')=$2"; }
get_env_status() { eval "echo \"\${ENV_STATUS_$(echo "$1" | tr ' ' '_'):-UNKNOWN}\""; }

# ── Shared error handler ─────────────────────────────────────
handle_error() {
    echo "[ERROR] Error occurred at line $1 (env: ${CURRENT_ENV:-unknown})"
}

echo -e "${CYAN}[INFO] Removing old known_hosts file...${RESET}"
rm -f "$KNOWN_HOSTS"
> "$COMBINED_LOG"

# ============================================================
# send_email — HTML formatted + coloured email via curl SMTP
# ============================================================
send_email() {
    local RUN_TIME
    RUN_TIME=$(date '+%Y-%m-%d %H:%M:%S')

    # ── Determine overall status for banner colour ────────────
    local OVERALL_STATUS="PASSED"
    local BANNER_BG="#1a7f37"   # green
    for env in "REVSTREAM" "SIEBEL" "OBILL" "DBILL"; do
        local st
        st=$(get_env_status "$env")
        if [[ "$st" != "OK" ]]; then
            OVERALL_STATUS="FAILED"
            BANNER_BG="#b91c1c"  # red
            break
        fi
    done

    # ── Build environment rows ────────────────────────────────
    local ENV_ROWS=""
    for env in "REVSTREAM" "SIEBEL" "OBILL" "DBILL"; do
        local st
        st=$(get_env_status "$env")
        if [[ "$st" == "OK" ]]; then
            ENV_ROWS="${ENV_ROWS}
            <tr>
              <td style='padding:10px 16px;font-size:14px;color:#111;border-bottom:1px solid #e5e7eb;'>${env}</td>
              <td style='padding:10px 16px;border-bottom:1px solid #e5e7eb;'>
                <span style='background:#dcfce7;color:#166534;padding:4px 12px;border-radius:12px;font-size:13px;font-weight:600;'>&#10003; PASSED</span>
              </td>
            </tr>"
        else
            ENV_ROWS="${ENV_ROWS}
            <tr>
              <td style='padding:10px 16px;font-size:14px;color:#111;border-bottom:1px solid #e5e7eb;'>${env}</td>
              <td style='padding:10px 16px;border-bottom:1px solid #e5e7eb;'>
                <span style='background:#fee2e2;color:#991b1b;padding:4px 12px;border-radius:12px;font-size:13px;font-weight:600;'>&#10007; FAILED</span>
              </td>
            </tr>"
        fi
    done

    # ── Escape log content for HTML ───────────────────────────
    local LOG_CONTENT
    LOG_CONTENT=$(cat "$COMBINED_LOG" 2>/dev/null \
        | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' \
        || echo "Log file not found: $COMBINED_LOG")

    # ── Build full HTML body ──────────────────────────────────
    local HTML_BODY
    HTML_BODY=$(cat <<HTMLEOF
<!DOCTYPE html>
<html>
<body style='margin:0;padding:0;background:#f3f4f6;font-family:Arial,sans-serif;'>

  <!-- Wrapper -->
  <table width='100%' cellpadding='0' cellspacing='0' style='background:#f3f4f6;padding:32px 0;'>
  <tr><td align='center'>
  <table width='680' cellpadding='0' cellspacing='0' style='background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);'>

    <!-- Banner -->
    <tr>
      <td style='background:${BANNER_BG};padding:24px 32px;'>
        <p style='margin:0;font-size:20px;font-weight:700;color:#ffffff;'>
          &#128202; PROD DB Health Check &mdash; ${OVERALL_STATUS}
        </p>
        <p style='margin:6px 0 0;font-size:13px;color:#e5e7eb;'>
          Run Time: ${RUN_TIME} &nbsp;|&nbsp; CR#: ${CHANGE_REQUEST}
        </p>
      </td>
    </tr>

    <!-- Summary heading -->
    <tr>
      <td style='padding:24px 32px 8px;'>
        <p style='margin:0;font-size:15px;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.05em;'>
          Environment Summary
        </p>
      </td>
    </tr>

    <!-- Summary table -->
    <tr>
      <td style='padding:0 32px 24px;'>
        <table width='100%' cellpadding='0' cellspacing='0'
               style='border:1px solid #e5e7eb;border-radius:6px;border-collapse:collapse;'>
          <tr style='background:#f9fafb;'>
            <th style='padding:10px 16px;text-align:left;font-size:12px;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;border-bottom:1px solid #e5e7eb;'>Environment</th>
            <th style='padding:10px 16px;text-align:left;font-size:12px;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;border-bottom:1px solid #e5e7eb;'>Status</th>
          </tr>
          ${ENV_ROWS}
        </table>
      </td>
    </tr>

    <!-- Divider -->
    <tr><td style='padding:0 32px;'><hr style='border:none;border-top:1px solid #e5e7eb;margin:0;'/></td></tr>

    <!-- Full log -->
    <tr>
      <td style='padding:24px 32px 8px;'>
        <p style='margin:0;font-size:15px;font-weight:700;color:#374151;text-transform:uppercase;letter-spacing:0.05em;'>
          Full Log Output
        </p>
      </td>
    </tr>
    <tr>
      <td style='padding:0 32px 32px;'>
        <pre style='background:#111827;color:#d1fae5;font-family:monospace;font-size:12px;padding:20px;border-radius:6px;overflow-x:auto;white-space:pre-wrap;word-wrap:break-word;margin:0;line-height:1.6;'>${LOG_CONTENT}</pre>
      </td>
    </tr>

    <!-- Footer -->
    <tr>
      <td style='background:#f9fafb;padding:16px 32px;border-top:1px solid #e5e7eb;'>
        <p style='margin:0;font-size:12px;color:#9ca3af;text-align:center;'>
          Generated automatically by DB Health Monitor &bull; ${RUN_TIME}
        </p>
      </td>
    </tr>

  </table>
  </td></tr>
  </table>

</body>
</html>
HTMLEOF
)

    # ── Write MIME email to temp file ─────────────────────────
    local MAIL_TMP
    MAIL_TMP=$(mktemp /tmp/healthcheck_mail_XXXX.txt)

    printf "From: DB Health Monitor <%s>\r\nTo: %s\r\nSubject: %s\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n" \
        "$EMAIL_FROM" "$EMAIL_TO" "$EMAIL_SUBJECT" > "$MAIL_TMP"
    printf "%s\r\n" "$HTML_BODY" >> "$MAIL_TMP"

    echo -e "${CYAN}[INFO] Sending HTML email to ${EMAIL_TO} via ${SMTP_HOST}:${SMTP_PORT}...${RESET}"

    # ── Try 1: Plain relay (no TLS/auth — typical corporate) ──
    curl -v --url "smtp://${SMTP_HOST}:${SMTP_PORT}" \
        --mail-from "$EMAIL_FROM" --mail-rcpt "$EMAIL_TO" \
        --upload-file "$MAIL_TMP" 2>/tmp/email_curl_err.txt
    local CURL_EXIT=$?

    # ── Try 2: STARTTLS + auth ────────────────────────────────
    if [[ $CURL_EXIT -ne 0 ]]; then
        echo -e "${CYAN}[INFO] Retrying with STARTTLS + auth...${RESET}"
        curl -v --url "smtp://${SMTP_HOST}:${SMTP_PORT}" --ssl \
            --mail-from "$EMAIL_FROM" --mail-rcpt "$EMAIL_TO" \
            --user "${SMTP_USER}:${SMTP_PASS}" \
            --upload-file "$MAIL_TMP" --insecure 2>/tmp/email_curl_err.txt
        CURL_EXIT=$?
    fi

    # ── Try 3: Port 25 fallback ───────────────────────────────
    if [[ $CURL_EXIT -ne 0 ]]; then
        echo -e "${CYAN}[INFO] Retrying on port 25...${RESET}"
        curl -v --url "smtp://${SMTP_HOST}:25" \
            --mail-from "$EMAIL_FROM" --mail-rcpt "$EMAIL_TO" \
            --upload-file "$MAIL_TMP" 2>/tmp/email_curl_err.txt
        CURL_EXIT=$?
    fi

    rm -f "$MAIL_TMP"

    if [[ $CURL_EXIT -eq 0 ]]; then
        echo -e "${GREEN}[OK] HTML email sent successfully to ${EMAIL_TO}.${RESET}"
    else
        echo -e "${RED}[FAIL] All email attempts failed (exit: ${CURL_EXIT}).${RESET}"
        cat /tmp/email_curl_err.txt
        echo -e "${RED}[TIP] Run: telnet ${SMTP_HOST} ${SMTP_PORT}${RESET}"
    fi
}

# ============================================================
# post_to_slack — color-coded Block Kit message
# ============================================================
post_to_slack() {
    local RUN_TIME
    RUN_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    local ATTACHMENTS=""
    local OVERALL="good"

    for env in "REVSTREAM" "SIEBEL" "OBILL" "DBILL"; do
        local st
        st=$(get_env_status "$env")
        local color icon text

        if [[ "$st" == "OK" ]]; then
            color="good"; icon=":white_check_mark:"; text="*${env}* — PASSED"
        else
            color="danger"; icon=":red_circle:"; text="*${env}* — FAILED"
            OVERALL="danger"
        fi

        [[ -n "$ATTACHMENTS" ]] && ATTACHMENTS+=","
        ATTACHMENTS+=$(cat <<EOF
{"color":"${color}","text":"${icon}  ${text}","footer":"Run time: ${RUN_TIME}"}
EOF
)
    done

    local HEADER_ICON
    [[ "$OVERALL" == "good" ]] && HEADER_ICON=":large_green_circle:" || HEADER_ICON=":red_circle:"

    local PAYLOAD
    PAYLOAD=$(cat <<EOF
{
  "username": "DB Health Monitor",
  "icon_emoji": ":database:",
  "attachments": [
    {
      "color": "${OVERALL}",
      "pretext": "${HEADER_ICON}  *PROD DB Health Check — ${RUN_TIME}*",
      "text": "CR: \`${CHANGE_REQUEST}\`  |  Environments: REVSTREAM, SIEBEL, OBILL, DBILL",
      "mrkdwn_in": ["pretext","text"]
    },
    ${ATTACHMENTS}
  ]
}
EOF
)

    echo -e "${CYAN}[INFO] Posting summary to Slack...${RESET}"

    if [[ -n "${SLACK_WEBHOOK_URL:-}" ]]; then
        HTTP_CODE=$(curl -s -o /tmp/slack_response.txt -w "%{http_code}" \
            -X POST -H "Content-Type: application/json" \
            --data "$PAYLOAD" "$SLACK_WEBHOOK_URL")
    elif [[ -n "${SLACK_BOT_TOKEN:-}" ]]; then
        PAYLOAD=$(echo "$PAYLOAD" | jq --arg ch "$SLACK_CHANNEL" '. + {channel: $ch}')
        HTTP_CODE=$(curl -s -o /tmp/slack_response.txt -w "%{http_code}" \
            -X POST -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
            --data "$PAYLOAD" "https://slack.com/api/chat.postMessage")
    else
        echo -e "${RED}[WARN] No Slack config found. Skipping.${RESET}"
        return 1
    fi

    [[ "$HTTP_CODE" == "200" ]] \
        && echo -e "${GREEN}[OK] Slack notification sent (HTTP $HTTP_CODE).${RESET}" \
        || echo -e "${RED}[FAIL] Slack post failed (HTTP $HTTP_CODE): $(cat /tmp/slack_response.txt)${RESET}"
}

# ============================================================
# run_gg_via_ssm  <instance_id> <db_host>
# ============================================================
run_gg_via_ssm() {
    local SSM_INSTANCE_ID="$1"
    local DB_HOST="$2"

    if command -v aws &>/dev/null && [[ -n "$SSM_INSTANCE_ID" ]]; then
        local GG_CMD='sudo su - oracle -c '\''printf "info all\nsh date\nexit\n" | ggsci'\'''
        local PARAMS
        PARAMS=$(jq -n --arg cmd "$GG_CMD" '{commands:[$cmd]}' 2>/dev/null) || \
        PARAMS="{\"commands\":[\"sudo su - oracle -c 'printf \\\"info all\\\\nsh date\\\\nexit\\\\n\\\" | ggsci'\"]}"

        local COMMAND_ID
        COMMAND_ID=$(aws ssm send-command \
            --instance-ids "$SSM_INSTANCE_ID" \
            --document-name "AWS-RunShellScript" \
            --parameters "$PARAMS" \
            --output text \
            --query 'Command.CommandId' 2>/dev/null) || COMMAND_ID=""

        if [[ -n "$COMMAND_ID" ]]; then
            echo "[INFO] SSM command sent (CommandId: $COMMAND_ID), waiting..."
            sleep 8
            for i in 1 2 3 4 5 6 7 8 9 10; do
                local STATUS
                STATUS=$(aws ssm get-command-invocation \
                    --command-id "$COMMAND_ID" \
                    --instance-id "$SSM_INSTANCE_ID" \
                    --query 'Status' --output text 2>/dev/null) || STATUS=""
                [[ "$STATUS" == "Success" || "$STATUS" == "Failed" || "$STATUS" == "Cancelled" ]] && break
                sleep 3
            done
            aws ssm get-command-invocation \
                --command-id "$COMMAND_ID" --instance-id "$SSM_INSTANCE_ID" \
                --query 'StandardOutputContent' --output text 2>/dev/null || true
            aws ssm get-command-invocation \
                --command-id "$COMMAND_ID" --instance-id "$SSM_INSTANCE_ID" \
                --query 'StandardErrorContent' --output text 2>/dev/null | grep -v '^$' || true
        else
            echo "[WARN] SSM failed; falling back to SSH -> $DB_HOST..."
            run_gg_via_ssh "$DB_HOST"
        fi
    else
        echo "[INFO] No AWS CLI / SSM; using SSH -> $DB_HOST..."
        run_gg_via_ssh "$DB_HOST"
    fi
}

# ============================================================
# run_gg_via_ssh  <db_host>
# ============================================================
run_gg_via_ssh() {
    local DB_HOST="$1"
    ssh -q "$DB_HOST" "
sudo su - oracle -c '
ggsci <<EOF | grep -v \"GGSCI.*%\" | grep -v \"GGSCI.*[0-9]>\"
info all
sh date
exit
EOF
'
" || echo "[WARN] SSH to $DB_HOST failed."
}

# ============================================================
# run_env  <label> <account> <python_script> <db_host> <ssm_id>
# ============================================================
run_env() {
    local LABEL="$1"
    local ACCOUNT="$2"
    local PYTHON_SCRIPT="$3"
    local DB_HOST="$4"
    local SSM_INSTANCE_ID="${5:-}"

    CURRENT_ENV="$LABEL"
    local EXIT_CODE=0

    echo -e "${BOLD}${CYAN}"
    echo "============================================================"
    echo "  Starting: $LABEL"
    echo "============================================================"
    echo -e "${RESET}"

    eiamcli aws_ssh -a "$ACCOUNT" -p id_rsa.pub -d ~/.ssh/ -cri "$CHANGE_REQUEST" || EXIT_CODE=$?
    eiamCli getAWSTempCredentials -a "$ACCOUNT" -r PowerUser -p default -cri "$CHANGE_REQUEST" || EXIT_CODE=$?

    {
        echo
        echo "############################################################"
        printf "#   %-54s   #\n" "$LABEL"
        echo "############################################################"
        echo " Timestamp : $(date '+%Y-%m-%d %H:%M:%S')"
        echo

        echo "============================================================"
        echo "                 <<< DATAGUARD STATUS >>>                   "
        echo "============================================================"
        echo
        python3 "$PYTHON_SCRIPT" || { echo "[ERROR] Python script failed for $LABEL"; EXIT_CODE=1; }

        echo
        echo "============================================================"
        echo "                <<< GOLDENGATE STATUS >>>                   "
        echo "============================================================"
        echo
        if [[ -n "$SSM_INSTANCE_ID" ]]; then
            run_gg_via_ssm "$SSM_INSTANCE_ID" "$DB_HOST" || EXIT_CODE=1
        else
            run_gg_via_ssh "$DB_HOST" || EXIT_CODE=1
        fi

        echo
        if [[ $EXIT_CODE -eq 0 ]]; then
            echo "  >>> STATUS : [OK] GREEN - $LABEL health check PASSED <<<"
        else
            echo "  >>> STATUS : [FAIL] RED - $LABEL health check had ERRORS <<<"
        fi
        echo "############################################################"
        echo
    } >> "$COMBINED_LOG" 2>&1

    if [[ $EXIT_CODE -eq 0 ]]; then
        set_env_status "$LABEL" "OK"
        echo -e "${GREEN}[OK] $LABEL completed successfully.${RESET}"
    else
        set_env_status "$LABEL" "FAIL"
        echo -e "${RED}[FAIL] $LABEL completed with errors — check log.${RESET}"
    fi
}

# ============================================================
# MAIN
# ============================================================
run_env "REVSTREAM" "0456-4590-6262" \
    "$BASE_SCRIPT_DIR/Revstream/prod/rds_oracle_replication_report.py" \
    "rvsogg.revstream-db-prod.a.intuit.com" "i-0981f3230a24cfb84"

run_env "SIEBEL" "0465-9463-2597" \
    "$BASE_SCRIPT_DIR/OBill/prod/rds_oracle_replication_report.py" \
    "ogg.siebel.a.intuit.com" "i-0c2729f7bf8b38ed9"

run_env "OBILL" "177794654858" \
    "$BASE_SCRIPT_DIR/OBill/prod/rds_oracle_replication_report.py" \
    "10.69.30.52" ""

run_env "DBILL" "890254371212" \
    "$BASE_SCRIPT_DIR/OBill/prod/rds_oracle_replication_report.py" \
    "ogg.brm101.prod.db.a.intuit.com" ""

# ── Append summary to log ─────────────────────────────────────
{
    echo "############################################################"
    echo "#              FINAL HEALTH CHECK SUMMARY                  #"
    echo "#              $(date '+%Y-%m-%d %H:%M:%S')                   #"
    echo "############################################################"
    for env in "REVSTREAM" "SIEBEL" "OBILL" "DBILL"; do
        st=$(get_env_status "$env")
        [[ "$st" == "OK" ]] && sig="[OK]  GREEN" || sig="[FAIL] RED"
        printf "  %-20s  %s\n" "$env" "$sig"
    done
    echo "############################################################"
} >> "$COMBINED_LOG"

# ── Terminal summary ──────────────────────────────────────────
echo
echo -e "${BOLD}============================================================${RESET}"
echo -e "${BOLD}             FINAL HEALTH CHECK SUMMARY                    ${RESET}"
echo -e "${BOLD}============================================================${RESET}"
for env in "REVSTREAM" "SIEBEL" "OBILL" "DBILL"; do
    st=$(get_env_status "$env")
    [[ "$st" == "OK" ]] \
        && echo -e "  ${GREEN}[OK] GREEN  ${RESET}| $env" \
        || echo -e "  ${RED}[FAIL] RED  ${RESET}| $env"
done
echo -e "${BOLD}============================================================${RESET}"
echo
echo -e "${CYAN}[INFO] Combined log: $COMBINED_LOG${RESET}"

# ── Notify ────────────────────────────────────────────────────
post_to_slack
send_email
