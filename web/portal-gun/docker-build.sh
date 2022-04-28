VALIDATION_IMAGE_NAME=cybermouflons/ccsc2022-portal-gun-validation
PORTAL_IMAGE_NAME=cybermouflons/ccsc2022-portal-gun-core

cat <<- EOF > docker-compose.override.yml
version: '3.5'
services:
  validationsvc:
    image: ${VALIDATION_IMAGE_NAME}
  
  portalsvc:
    image: ${PORTAL_IMAGE_NAME}
EOF

docker-compose -f setup/docker-compose.yml -f docker-compose.override.yml build

rm docker-compose.override.yml

tar -czvf public/portal-gun.tar.gz ./setup/validation-svc setup/portal-svc setup/docker-compose.yml
