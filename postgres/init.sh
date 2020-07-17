#!/bin/bash

echo 'Creating Portal database and user'
createdb -U ${POSTGRES_DB} ${PORTAL_DB_NAME}
psql -U ${POSTGRES_DB} -c "CREATE USER ${PORTAL_DB_USER} WITH PASSWORD '${PORTAL_DB_PSWD}';"
psql -U ${POSTGRES_DB} -c "GRANT ALL PRIVILEGES ON DATABASE ${PORTAL_DB_NAME} TO ${PORTAL_DB_USER};"
echo 'Portal database created'

echo 'Creating Activiti database and user'
createdb -U ${POSTGRES_DB} ${ACTIVITI_DB_NAME}
psql -U ${POSTGRES_DB} -c "CREATE USER ${ACTIVITI_DB_USER} WITH PASSWORD '${ACTIVITI_DB_PSWD}';"
psql -U ${POSTGRES_DB} -c "GRANT ALL PRIVILEGES ON DATABASE ${ACTIVITI_DB_NAME} TO ${ACTIVITI_DB_USER};"
echo 'Activiti database created'
