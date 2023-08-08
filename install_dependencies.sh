#Backend dependencies (Python)
conda create -n its python==3.11.4
conda activate its
pip install -r /api/requirements.txt
#Frontend dependencies (Javascript/Angular)
sudo ap-get install node
sudo apt-install npm
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
sudo npm install -g @angular/cli
#Database dependencies (MongoDB)
wget https://repo.mongodb.org/apt/ubuntu/dists/jammy/mongodb-org/6.0/multiverse/binary-amd64/mongodb-org-server_6.0.8_amd64.deb
sudo dpkg -i mongodb-org-server_6.0.8_amd64.deb
rm mongodb-org-server_6.0.8_amd64.deb
sudo systemctl start mongod
systemctl enable mongod #Enable MongoDB service on every reboot!!!
wget https://downloads.mongodb.com/compass/mongodb-mongosh_1.10.3_amd64.deb
sudo dpkg -i mongodb-mongosh_1.10.3_amd64.deb
rm mongodb-mongosh_1.10.3_amd64.deb
#Run api/tasks/tasks_to_json and select database import to import tasks from a folder into the database