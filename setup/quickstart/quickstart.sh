#!/usr/bin/env bash
set -e

echo 'Waiting For Vidispine'
until $(curl --output /dev/null --silent --head --fail "http://${VIDISPINE_HOST}:8080/APInoauth/is-online"); do
    echo '.'
    sleep 1
done
echo 'Vidispine Online!'

if vidispine-api -s -a text/plain configuration/properties/nmrsetup; then
  CURRENT_SETUP_VERSION=`vidispine-api -a text/plain configuration/properties/nmrsetup`
else
  CURRENT_SETUP_VERSION=0
fi

if [ ${CURRENT_SETUP_VERSION} -eq 0 ]; then
  echo "Running Step ${CURRENT_SETUP_VERSION}"
  vidispine-api -X POST -b APIinit -a text/plain /
  vidispine-api -X POST -f /quickstart/resource_transcoder.json resource/transcoder
  vidispine-api -X POST -f /quickstart/resource_thumbnail.json resource/thumbnail
  vidispine-api -X PUT -f /quickstart/configuration_properties_solrpath.json configuration/properties
  vidispine-api -X PUT -f /quickstart/configuration_properties_portal_uri.json configuration/properties
  vidispine-api -X POST -f /quickstart/storage.json storage
  echo "Complete Step ${CURRENT_SETUP_VERSION}"
  CURRENT_SETUP_VERSION=$((${CURRENT_SETUP_VERSION} + 1))
  vidispine-api -X PUT -c text/plain -d ${CURRENT_SETUP_VERSION} configuration/properties/nmrsetup
fi

echo "Vidispine Setup Complete!"

exit 0
