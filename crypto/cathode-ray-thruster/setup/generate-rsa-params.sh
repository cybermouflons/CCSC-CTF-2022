openssl genrsa -out private-key.pem 4096
openssl rsa -in private-key.pem -pubout -out ../public/public-key.pem