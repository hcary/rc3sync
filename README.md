
sudo mkdir /etc/nginx/certs



# SSL Certificates
ssl_certificate /etc/nginx/certs/nginx-selfsigned.crt;   # Replace with your actual SSL certificate path
ssl_certificate_key /etc/nginx/certs/nginx-selfsigned.key; # Replace with your actual SSL key path

openssl rsa -noout -modulus -in /etc/nginx/certs/nginx-selfsigned.key | openssl md5

openssl x509 -noout -modulus -in /etc/nginx/certs/nginx-selfsigned.crt | openssl md5

./client.py --server_url http://10.10.1.40:5000/upload python.encrypt.py 

