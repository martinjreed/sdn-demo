Mininet SDN vs STP Demonstration
================================

Installation:
-------------

```bash
sudo apt install net-tools
sudo apt-get install openssh-server
sudo apt install git

# Install bazel https://bazel.build/install/ubuntu preferably using baselisk https://github.com/bazelbuild/bazelisk

wget https://github.com/bazelbuild/bazelisk/releases/download/v1.18.0/bazelisk-linux-amd64
sudo mv bazelisk-linux-amd64 /usr/local/bin/bazel
sudo chmod 755 /usr/loca/bin/bazel

# vital onos is in ~/onos !!!!!
cd
git clone https://gerrit.onosproject.org/onos
cd onos
# makes sure you are on a stable branch, this was the one when I did it
git checkout --track origin/onos-2.7.0
# build it
bazel build onos
# run it
bazel run onos-local -- clean debug
# connect to Onos command line:
ssh -q -p 8101 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null onos@127.0.0.1
onos@root > app activate org.onosproject.openflow
onos@root > app activate org.onosproject.fwd
# disconnect from onos command line with Ctrl-D
# note some scripts use json installed using:
# https://github.com/trentm/json
sudo apt install nodejs npm
sudo npm install -g json
```
Running mininet script:
--------
See the SDN Tutorial.doc for how to run the tutorial and demonstration

