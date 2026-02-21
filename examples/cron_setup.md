# Cron Setup Guide

This guide shows how to automate weather logging using cron.

## Quick Setup

### 1. Find Python Path

```bash
which python3
# Output: /usr/bin/python3
```

### 2. Find Script Path

```bash
realpath weather.py
# Output: /home/username/weather-logger/weather.py
```

### 3. Edit Crontab

```bash
crontab -e
```

## Example Cron Jobs

### Log Every Hour

```cron
# Log weather every hour at minute 0
0 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "Lisbon" --output /home/username/weather_log.csv
```

### Log Every 15 Minutes

```cron
# Log weather every 15 minutes
*/15 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "Lisbon" --output /home/username/weather_log.csv
```

### Log at Specific Times

```cron
# Log at 8:00 AM, 12:00 PM, and 6:00 PM
0 8,12,18 * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "London" --output /home/username/weather_log.csv
```

### Daily Summary

```cron
# Log once per day at 6 AM
0 6 * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "New York" --output /home/username/daily_weather.csv
```

### Multiple Locations

```cron
# Log multiple cities every hour
0 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "Lisbon" --output /home/username/lisbon.csv
5 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "London" --output /home/username/london.csv
10 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "New York" --output /home/username/nyc.csv
```

## Adding Logging

Redirect output to a log file for debugging:

```cron
# Log with timestamps to a separate log file
0 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py --city "Lisbon" >> /home/username/weather_cron.log 2>&1
```

## Verify Cron Jobs

List your cron jobs:

```bash
crontab -l
```

## Cron Syntax Reference

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday = 0)
│ │ │ │ │
│ │ │ │ │
* * * * *  command
```

### Common Patterns

| Schedule | Cron Expression |
|----------|-----------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Every 2 hours | `0 */2 * * *` |
| Daily at 6 AM | `0 6 * * *` |
| Weekdays at 8 AM | `0 8 * * 1-5` |
| Weekly (Sundays) | `0 0 * * 0` |

## Troubleshooting

### Check Cron Logs

```bash
# Ubuntu/Debian
sudo grep CRON /var/log/syslog

# macOS
cat /var/log/cron.log
```

### Test Cron Command Manually

```bash
# Copy the exact command from crontab and run it
/usr/bin/python3 /home/username/weather-logger/weather.py --city "Lisbon"
```

### Common Issues

1. **Permission denied**: Make sure the script is executable
   ```bash
   chmod +x weather.py
   ```

2. **File not found**: Use absolute paths
   ```bash
   # Good
   0 * * * * /usr/bin/python3 /home/username/weather-logger/weather.py
   
   # Avoid
   0 * * * * python3 weather.py
   ```

3. **No output**: Redirect stderr to see errors
   ```bash
   0 * * * * /usr/bin/python3 /path/to/weather.py 2>> /home/username/weather_errors.log
   ```

## Systemd Timer (Alternative)

For systems using systemd, create a timer:

### 1. Create Service File

`~/.config/systemd/user/weather-logger.service`:
```ini
[Unit]
Description=Weather Logger

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/username/weather-logger/weather.py --city "Lisbon" --output /home/username/weather_log.csv
```

### 2. Create Timer File

`~/.config/systemd/user/weather-logger.timer`:
```ini
[Unit]
Description=Run Weather Logger every hour

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

### 3. Enable Timer

```bash
systemctl --user daemon-reload
systemctl --user enable weather-logger.timer
systemctl --user start weather-logger.timer
```

### 4. Check Status

```bash
systemctl --user list-timers
```

## Windows Task Scheduler

For Windows users, use Task Scheduler instead of cron:

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (Daily, Hourly, etc.)
4. Action: Start a program
5. Program: `python.exe` or `python3.exe`
6. Arguments: `C:\path\to\weather.py --city "Lisbon"`
7. Finish
