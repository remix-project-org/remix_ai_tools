#!/bin/bash
apt-get update

apt-get install gnupg curl

curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor

apt-get update
apt-get install -y mongodb-org

wget -qO - https://pgp.mongodb.com/server-7.0.asc | apt-key add -
#atlas deployments search indexes create --file indexDef-vector.json
#atlas deployments search indexes create --file indexDef-vector-cosine.json