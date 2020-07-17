PORTAL_3.2.8?=http://www2.cantemo.com/files/transfer/7d/7dab1827838ec159968fe33d5f3e77cfe57cbad9/RedHat7_Portal_3.2.8.tar
PORTAL_3.4.13?=https://www2.cantemo.com/files/transfer/4b/4b5765257ec10935fd519a34bf5e3428b11b7c9e/RedHat7_Portal_3.4.13.tar

build-3.2.8:
	cp key portal/key
	cp key vidispineserver/key
	docker-compose build --build-arg PORTAL_DOWNLOAD_URL=$(PORTAL_3.2.8)

build-3.4.13:
	cp key portal/key
	cp key vidispineserver/key
	docker-compose build --build-arg PORTAL_DOWNLOAD_URL=$(PORTAL_3.4.13)

run:
	docker-compose up
