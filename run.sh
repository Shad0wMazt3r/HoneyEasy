python3 web_honeypot.py &
web_honeypot_id=$!

echo "Web Honeypot PID: $web_honeypot_id"

python3 ssh_honeypot.py &
ssh_honeypot_id=$!

echo "SSH Honeypot PID: $ssh_honeypot_id"