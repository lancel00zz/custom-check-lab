# Lab Commands Reference

## Terminal 
```bash
echo "export PS1='%~:$ '" >> ~/.zshrc && source ~/.zshrc
```

## Repo
```bash
mkdir ~/Desktop/repo
cd ~/Desktop/repo
# cloning the repo:
git clone git@github.com:lancel00zz/helloworld2-lab.git
```

## Single Step Installation
```bash
sudo cp ~/Desktop/repo/helloworld2-lab/HelloWorld2/script\ and\ conf/helloworld2.py /opt/datadog-agent/etc/checks.d/ && echo "✅ Copied helloworld2.py in checks.d" \
&& sudo mkdir -p /opt/datadog-agent/etc/conf.d/helloworld2.d && echo "✅ Created directory \"helloworld2.d\"" \
&& sudo cp ~/Desktop/repo/helloworld2-lab/HelloWorld2/script\ and\ conf/conf.yaml /opt/datadog-agent/etc/conf.d/helloworld2.d/ && echo "✅ Copied conf.yaml in helloworld2.d"
```
