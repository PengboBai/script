#!/bin/bash
# author 白鹏博 baipengbb@163.com
set -x
# install docker docker-compose
issue=`cat /etc/issue`
if [[ "${issue}" =~ "Ubuntu" ]]
then
    echo "Ubuntu"
    sudo apt-get install -y git
    sudo apt-get install -y docker
    sudo apt-get install -y docker-compose
else
    echo "Other"
    sudo yum install -y git
    sudo yum install -y docker
    sudo yum install -y docker-compose
fi

# pull images
sudo docker pull baipengbo/phabricator:latest
sudo docker pull baipengbo/jenkins:latest
sudo docker pull baipengbo/build:latest
sudo docker pull baipengbo/dev:latest

base_path=/home/${USER}/baipengbo
if [[ ! -d "${base_path}/workspace" ]]
then
    mkdir -p ${base_path}/workspace
fi

cd ${base_path}
# clone repo from github
repo_list=( phabricator script jenkins)
for repo in ${repo_list[*]}
do
    if [[ ! -d "${base_path}/${repo}" ]]
    then
        git clone https://github.com/baipengbo/${repo}.git
    fi
done

# prepare phabricator image entrypoint.sh
cp -a ${base_path}/script/init_env/entrypoint.sh ${base_path}/phabricator
sudo chmod +x ${base_path}/phabricator/entrypoint.sh

# prepare docker-compose file
compose_file=${base_path}/script/init_env/docker-compose.yml
sudo sed "s/\/base_path/${base_path//\//\\/}/g" ${compose_file}>>${base_path}/docker-compose.yml

# config env base_path for jenkins
sed -i "s/<string>\/base_path<\/string>/<string>${base_path//\//\\/}<\/string>/g" ${base_path}/jenkins/config.xml

# docker-compose up
container=`sudo docker-compose -f ${base_path}/docker-compose.yml ps`
if [[ "x${container}" == "x" ]]
then
    sudo docker-compose -f ${base_path}/docker-compose.yml stop
    sudo docker-compose -f ${base_path}/docker-compose.yml rm -f
fi
sudo docker-compose -f ${base_path}/docker-compose.yml up -d

echo "Init env success"
echo "Phabricator url: http://127.0.0.1"
echo "Phabricator admin account: admin/root2ci."
echo "Phabricator user account: baipengbo/root2ci."
echo "Phabricator build example: http://127.0.0.1/D3"
echo "Jenkins url: http://127.0.0.1:8888"
echo "Jenkins account admin/root2ci."
