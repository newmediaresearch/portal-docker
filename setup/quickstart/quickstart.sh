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

echo 'Waiting For Activiti'
until $(curl --output /dev/null --silent --head --fail "http://${ACTIVITI_HOST}:8008/"); do
    echo '.'
    sleep 1
done
echo 'Activiti Online!'

# Create the admin user
PGPASSWORD=${ACTIVITI_DB_PSWD} psql -h ${POSTGRES_HOST} -U ${ACTIVITI_DB_USER} \
  -c "INSERT INTO act_id_user(id_, rev_, first_, last_, email_, pwd_)
    VALUES('${ACTIVITI_USERNAME}', '1', 'Portal', 'Admin', '', '${ACTIVITI_PASSWORD}');"

# Create the admin role
PGPASSWORD=${ACTIVITI_DB_PSWD} psql -h ${POSTGRES_HOST} -U ${ACTIVITI_DB_USER} \
  -c "INSERT INTO act_id_group VALUES('admin', '1', 'Admin', 'security-role');"

# Add user admin to the admin role
PGPASSWORD=${ACTIVITI_DB_PSWD} psql -h ${POSTGRES_HOST} -U ${ACTIVITI_DB_USER} \
  -c "INSERT INTO act_id_membership VALUES('${ACTIVITI_USERNAME}', 'admin');"

echo "Activiti Setup Complete!"

exit 0
