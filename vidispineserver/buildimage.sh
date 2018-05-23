#! /bin/bash -xe

cat <<EOT >> /etc/yum.repos.d/vidispine.repo
[vidispine]
name=Vidispine YUM repository
baseurl=http://repo.vidispine.com/yum/stable/${VIDISPINE_VERSION}/el7/x86_64/
enabled=1
gpgcheck=0
repo_gpgcheck=1
gpgkey=http://repo.vidispine.com/yum/pkg_sign_pub.gpg
EOT

yum install -y vidispine-server vidispine-tools vidispine-tools-debuginfo
