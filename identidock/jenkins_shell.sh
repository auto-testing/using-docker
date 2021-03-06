# cd identidock # FOR source: https://github.com/auto-testing/using-docker.git

#Default compose args
COMPOSE_ARGS=" -f jenkins.yml -p jenkins "

#Make sure old containers are gone
sudo docker-compose $COMPOSE_ARGS stop
sudo docker-compose $COMPOSE_ARGS rm --force -v

#build the system
sudo docker-compose $COMPOSE_ARGS build --no-cache
sudo docker-compose $COMPOSE_ARGS up -d

#Run unit tests
sudo docker-compose $COMPOSE_ARGS run --no-deps --rm -e ENV=UNIT identidock
ERR=$?

#Run system test if unit tests passed
if [ $ERR -eq 0 ]; then
  IP=$(sudo docker inspect -f {{.NetworkSettings.IPAddress}} jenkins_identidock_1)
  CODE=$(curl -sL -w "%{http_code}" $IP:9090/monster/bla -o /dev/null) || true
  if [ $CODE -ne 200 ]; then
    HASH=$(git rev-parse --short HEAD)
    echo "Test passed - Tagging: by hash $HASH and 'newest'"
    docker_repo='testerxx09/using-docker.identidock'
    sudo docker tag jenkins_identidock $docker_repo:$HASH
    sudo docker tag jenkins_identidock $docker_repo:newest
    echo "Pushing"
    sudo docker login -u $DOCKER_USER -p $DOCKER_PASS # -e joe@bloggs.com -u jbloggs -p jbloggs123
    sudo docker push $docker_repo:$HASH
    sudo docker push $docker_repo:newest
  else
    echo "Site returned " $CODE
    ERR=1
  fi
fi

#Pull down the system
sudo docker-compose $COMPOSE_ARGS stop
sudo docker-compose $COMPOSE_ARGS rm --force -v

return $ERR
