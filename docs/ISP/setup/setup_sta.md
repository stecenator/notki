---
icon: material/fast-forward
---

!!! Bug
	Tu brakuje mnóstwa rzeczy. 

# Konfiguracja Storage Agenta

## Tworzenie usługi `systemd`

```ini title="/etc/systemd/system/dsmsta.service"
[Unit]
Description=IBM Spectrum Protect Storage Agent
After=network.target

[Service]
TasksMax=infinity
Type=oneshot
RemainAfterExit=true
ExecStart=/opt/tivoli/tsm/StorageAgent/bin/service/dsmsta.rc start
ExecStop=/opt/tivoli/tsm/StorageAgent/bin/service/dsmsta.rc stop
ExecReload=/opt/tivoli/tsm/StorageAgent/bin/service/dsmsta.rc restart

[Install]
WantedBy=multi-user.target
```
