#!/bin/bash
cd "$(dirname $(readlink -f "$0"))/.."
set -ex
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
DRYRUN=${DRYRUN-}
COMMANDDRYRUN="$(if [[ -n "$DRYRUN" ]];then COMMANDDRYRUN="echo";fi)"
STRIP_VERSIONS=${STRIP_VERSIONS-}
#instances="${@:-"geology geology-archives geology-biblio geology-biblio-maps geology-biblio-natstones"}"
instances="${@}"
fsrecover="$(./bin/zopepy -c "import ZODB.fsrecover;print(ZODB.fsrecover.__file__)"|sed -re "s/pyc/py/g")"
timeit() { date -Isec;"$@";date -Isec; }
for i in $instances;do
    zodb=$(pwd)/var/filestorage/Data.${i}.fs
    bin/supervisorctl stop instance1-$i zeoserver-${i}
    if [ -e ${zodb} ];then $COMMANDDRYRUN mv $zodb ${zodb}.orig;fi
    torepair=${zodb}.orig
    if [[ -n $STRIP_VERSIONS ]];then
        torepair=${zodb}.stripped
        $COMMANDDRYRUN timeit bin/zopepy scripts/strip_versions.py ${zodb}.orig ${zodb}.stripped
    fi
    $COMMANDDRYRUN timeit bin/zopepy ${fsrecover} -P 0 -f ${torepair} ${zodb}
    bin/supervisorctl start instance1-$i zeoserver-${i}
done
