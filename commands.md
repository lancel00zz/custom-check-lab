# Lab Commands Reference

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
echo '✅ Files successfully copied and directory created!'
```
