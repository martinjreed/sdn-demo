Mininet SDN vs STP Demonstration
================================

Installation:
-------------

```bash
sudo apt install net-tools
sudo apt-get install openssh-server
sudo apt install git

cd Downloads
wget https://github.com/bazelbuild/bazel/releases/download/1.1.0/bazel-1.1.0-installer-linux-x86_64.sh
chmod 755 bazel-1.1.0-installer-linux-x86_64.sh 
./bazel-1.1.0-installer-linux-x86_64.sh --user
# vital onos is in ~/onos !!!!!
cd
git clone https://gerrit.onosproject.org/onos
cd onos
# makes sure you are on a stable branch, this was the one when I did it
git checkout --track origin/onos-2.2
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
First make sure Onos is running as above then:

``` bash

```

