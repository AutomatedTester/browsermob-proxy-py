#!/usr/bin/env bash
if [ "$(uname)" == "Darwin" ]; then
    echo "We're on a MAC!"
   chromeDriver="chromedriver_mac64.zip"
   geckoDriverVersion="v0.13.0"
   geckoDriver="geckodriver-$geckoDriverVersion-macos.tar.gz"
else
    echo "We're not on a MAC!"
   chromeDriver="chromedriver_linux64.zip"
   geckoDriverVersion="v0.14.0"
   geckoDriver="geckodriver-$geckoDriverVersion-linux64.tar.gz"
fi
rm -rf tools
mkdir -p tools && \
cd tools && \
wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip && \
unzip -o browsermob-proxy-2.1.4-bin.zip && \
rm -rf browsermob-proxy*.zip* && \
wget http://selenium-release.storage.googleapis.com/3.0/selenium-server-standalone-3.0.1.jar && \
wget https://github.com/mozilla/geckodriver/releases/download/${geckoDriverVersion}/${geckoDriver} && \
tar zxf ${geckoDriver} && \
rm -rf ${geckoDriver}* && \
wget https://chromedriver.storage.googleapis.com/2.27/${chromeDriver} && \
unzip ${chromeDriver} && \
rm -rf ${chromeDriver}* && \
cd .. 
