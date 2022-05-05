# docker-compose  --force-rm -f docker-compose-deploy.yml up --build -d
docker-compose -f deploy/docker-compose.yml build --force-rm
docker-compose -f deploy/docker-compose.yml up -d