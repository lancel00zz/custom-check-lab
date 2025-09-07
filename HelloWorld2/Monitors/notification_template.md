# Suggested Title
```
🚨 [{{status}}] Host {{host.name}} (IP: {{host.ip}}) - Desktop File Count (HelloWorld2)
```

# Suggested Content
```
These are constants included in every alert:
- Host: {{host.name}}
- IP: {{host.ip}}
- Number of files: {{value}}
- Threshold: {{threshold}}

---

{{#is_alert}}
🚨 **ALERT TRIGGERED** 🚨  
The desktop file count has exceeded the threshold!  
- Current value: **{{value}}**  
- Host: **{{host.name}} ({{host.ip}})**  
- Threshold: > {{threshold}}  

👉 Action required: Please connect to the host and clean up the files.  
📧 Notifying: @student-team@datadoghq.com  

{{/is_alert}}

---

{{#is_warning}}
⚠️ **WARNING** ⚠️  
The file count is getting close to the limit.  
- Current value: {{value}}  
- Warning threshold: {{warn_threshold}}  

📧 Notifying: @student-team@datadoghq.com  
{{/is_warning}}

---

{{#is_alert_recovery}}
✅ **RECOVERY** ✅  
Good news! The file count is back under control.  
- Current value: {{value}}  
- Recovery threshold: {{recovery_threshold}}  

System has stabilized. No further action required.  
📧 Notifying: @student-team@datadoghq.com  
{{/is_alert_recovery}}

---

{{#is_no_data}}
❓ **NO DATA RECEIVED** ❓  
No metric data has been reported for:  
- Host: {{host.name}}  
- Metric: `helloworld2.desktop_file_count`  

This might indicate a reporting issue or the agent being down.  
📧 Notifying: @student-team@datadoghq.com  
{{/is_no_data}}

---

💡 *This message shows how Datadog conditional blocks work:*  
- `#is_alert` → Alert text  
- `#is_warning` → Warning text  
- `#is_alert_recovery` → Recovery text  
- `#is_no_data` → No-data state text  
```