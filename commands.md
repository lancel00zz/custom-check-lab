# Lab Commands Reference

## About the Agent on a Mac
```bash
datadog-agent launch-gui #display the Agent GUI

#stop datadog agent
(launchctl stop com.datadoghq.agent)
sudo launchctl kill SIGTERM system/com.datadoghq.agent

#start datadog agent
(launchctl start com.datadoghq.agent)
sudo launchctl kickstart system/com.datadoghq.agent

#restart datadog agent
sudo launchctl kickstart -k system/com.datadoghq.agent

#check process ID for datadog agent
sudo launchctl print system/com.datadoghq.agent | grep pid
```


## Repo
```bash
# create the folder that will host the repo:
mkdir ~/Desktop/repo
cd ~/Desktop/repo

# cloning the repo:
git clone git@github.com:lancel00zz/custom-check-lab.git
```


## Single Step Installation
Copy the full block of commands below (five lines) and run it in your Terminal.
```bash
cd ~/Desktop/repo/custom-check-lab/script_and_config && \
cp helloworld2.py /opt/datadog-agent/etc/checks.d/ && \
mkdir -p /opt/datadog-agent/etc/conf.d/helloworld2.d && \
cp conf.yaml /opt/datadog-agent/etc/conf.d/helloworld2.d/ && \
echo $'\033[0;32m\u2705  Files successfully copied and directory created!\033[0m'
```

## Full Disk Access for the Agent
```bash
/opt/datadog-agent/bin/agent/agent
```
