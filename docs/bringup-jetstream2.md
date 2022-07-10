# Bringup on Jetstream2

This document contains bringup instructions on Jetstream2.


# About Jetstream

https://jetstream2.exosphere.app/exosphere/

Jetstream is a academic cloud provider, for which credit is granted through NSF XSEDE/ACCESS programs.

Features:
 * Jetstream through provisions VMs, Volumes, and public IP addresses.


# Bringup

## Obtain Resources

1. Create a VM manually OR use nsdf-cloud myjetstream2 create 1
2. Follow sub-recipes
    a. Manually deploy
    b. Use ansible to automatically deploy (TODO)

### A: Manually Deploy

3. SSH to VM
4. clone https://github.com/nsdf-fabric/nsdf-catalog
5. Edit compose.yml 
6. docker-compose up



mkdir -p data
docker run --name some-nginx -d -p 80:80 -v data:/usr/share/nginx/html:ro nginx
sudo firewall-cmd --add-service=http --permanent
