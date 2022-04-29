openssl genrsa -out private-key.pem 2048
openssl rsa -in private-key.pem -pubout -out ../public/public-key.pem