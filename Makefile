PORTAL_3.2.8?=http://www2.cantemo.com/files/transfer/7d/7dab1827838ec159968fe33d5f3e77cfe57cbad9/RedHat7_Portal_3.2.8.tar

run-3.2.8:
	docker-compose build --build-arg PORTAL_DOWNLOAD_URL=$(PORTAL_3.2.8)
	docker-compose up