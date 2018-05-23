#!/usr/bin/env bash
set -e

term_handler() {
  if [ $pid -ne 0 ]; then
    kill -SIGTERM "$pid"
    wait "$pid"
  fi
  exit 143; # 128 + 15 -- SIGTERM
}

trap 'kill ${!}; term_handler' SIGTERM

run_server() {
  chown vidispine:vidispine /var/lib/vidispine/solr/collection1/data
  su vidispine -c "/usr/bin/java \
   -Xmx${SOLR_HEAP:-512m} \
  -Dlog4j.configuration=file:/etc/vidispine/solr/log4j.properties \
  -Djetty.home=/usr/share/vidispine/solr \
  -Dsolr.solr.home=/var/lib/vidispine/solr \
  -jar /usr/share/vidispine/solr/start.jar"
}

run_server & wait ${!}
