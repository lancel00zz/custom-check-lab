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
```bash
sudo cp ~/Desktop/repo/custom-check-lab/script_and_config/helloworld2.py /opt/datadog-agent/etc/checks.d/ && echo "✅ Copied helloworld2.py in checks.d" \
&& sudo mkdir -p /opt/datadog-agent/etc/conf.d/helloworld2.d && echo "✅ Created directory \"helloworld2.d\"" \
&& sudo cp ~/Desktop/repo/custom-check-lab/script_and_config/conf.yaml /opt/datadog-agent/etc/conf.d/helloworld2.d/ && echo "✅ Copied conf.yaml in helloworld2.d"
```
