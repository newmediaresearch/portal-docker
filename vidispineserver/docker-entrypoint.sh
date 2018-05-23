#!/usr/bin/env bash
set -e

export POSTGRES_PASSWORD=${VIDISPINE_DB_PSWD:-vidispine}
export POSTGRES_USER=${VIDISPINE_DB_USER:-vidispine}
export POSTGRES_DB=${VIDISPINE_DB_NAME:-vidispine}
export POSTGRES_HOST=${POSTGRES_HOST:-postgres}
export VIDISPINESERVER_HEAP=${VIDISPINESERVER_HEAP:-2048m}

term_handler() {
  if [ $pid -ne 0 ]; then
    kill -SIGTERM "$pid"
    wait "$pid"
  fi
  exit 143; # 128 + 15 -- SIGTERM
}

trap 'kill ${!}; term_handler' SIGTERM

run_server() {
  cd /var/lib/vidispine/server/

  echo "Pinging Database..."

  until vidispine db ping; do
    >&2 echo "Database is unavailable - sleeping..."
    sleep 1
  done

  >&2 echo "Postgres is up - executing command"

  set +e
  echo "Checking Database..."
  vidispine db check
  if [ ! $? -eq 0 ]; then
    set -e
    echo "Init Database..."
    vidispine db init
    echo "Migrating Database..."
    vidispine db migrate
    echo "Re-checking Database..."
    vidispine db check
  fi
  set -e

  echo "Starting Server..."
  java -Xmx${VIDISPINESERVER_HEAP} \
  -Dcom.vidispine.credentials.dir=/etc/vidispine/ \
  -Dcom.vidispine.license.dir=/etc/vidispine/ \
  -Dcom.vidispine.license.tmpdir=/var/lib/vidispine/server/ \
  -Dcom.vidispine.log.dir=/var/log/vidispine/ \
  -cp /usr/share/vidispine/server/lib/ext/*:/usr/share/vidispine/server/vidispine-server.jar \
  com.vidispine.server.VidispineApplication server /etc/vidispine/server.yaml
}


run_server & wait ${!}
