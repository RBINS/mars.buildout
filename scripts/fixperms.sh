#!/bin/bash
if [ "x${SDEBUG-}" != "x" ];then set -x;fi
cd $(dirname $(readlink -f $0))/..
W=$(pwd)
cd var/blobstorage

cat >acls<<EOF
user::rwx
user:supervisor:r-x
user:zope:rwx
group::---
mask::rwx
other::r-x
EOF

cat >dacls<<EOF
user::rwx
user:supervisor:r-x
user:zope:rwx
group::---
mask::rwx
other::--x
default:user::rwx
default:user:supervisor:r--
default:user:zope:rwx
default:group::---
default:mask::rwx
default:other::--x
EOF

( while read f;do setfacl --set-file=dacls $f&done < <(find $(ls -1d storage*|grep -Ev "\.old$") -type d); )&
( while read f;do setfacl --set-file=acls  $f&done < <(find $(ls -1d storage*|grep -Ev "\.old$") -type f); )&
wait
