Ansible Deployment
==================

Requirements (Ubuntu 22.04):
* Docker CE
* apt packages:
  * ansible
  * python3-docker 
  * docker-compose 

## Deploy without ssl:

Leave inventory.yml as is. This deployment is suitable for running locally.

        ansible-playbook -i inventory.yml deploy.yml

## Deploy with ssl (letsencrypt):

Edit inventory.yml and change ssl to true and change hostname to the fqdm.

        ansible-playbook -i inventory.yml deploy.yml

## Stop the docker containers:

        ansible-playbook -i inventory.yml deploy.yml -e docker_compose_up=absent