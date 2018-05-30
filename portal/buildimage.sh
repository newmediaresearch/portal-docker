#! /bin/bash -xe

mkdir /install
cd /install

wget -q $PORTAL_DOWNLOAD_URL -O Portal.tar

tar xvf Portal.tar

cd RedHat*[0-9]

yum install -y resources/portal/*.rpm resources/portal/postgresql/*.rpm

rm -rf /install/RedHat* Portal.tar

yum clean all

echo "COMPRESS_ENABLED = False" >> /opt/cantemo/portal/portal/localsettings.py
echo "STATSD_CELERY_SIGNALS = True" >> /opt/cantemo/portal/portal/localsettings.py
