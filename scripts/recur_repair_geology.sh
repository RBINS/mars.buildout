#!/bin/bash
cd "$(dirname $(readlink -f "$0"))/.."
set -eo pipefail
if [[ -n ${SHELL_DEBUG-} ]];then set -x;fi
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
DRYRUN=${DRYRUN:-${DRY_RUN-}}
W=$(pwd)
LOGS=$W/var/log
DATECHRONO=${DATECHRONO:-$(date +"%Y%m%d%H%M%S")}
COMMANDDRYRUN="$(if [[ -n "$DRYRUN" ]];then echo "echo";fi)"
STRIP_VERSIONS=${STRIP_VERSIONS-}
USE_REPAIRED=${USE_REPAIRED-}
#instances="${@:-"geology geology-archives geology-biblio geology-biblio-maps geology-biblio-natstones"}"
instances="${@}"
fsrecover="$(./bin/zopepy -c "import ZODB.fsrecover;print(ZODB.fsrecover.__file__)"|sed -re "s/pyc/py/g")"
timeit() { date -Isec >&2;vv "$@";date -Isec >&2; }
log() { echo "$@" >&2; }
vv() { log "${COMMANDDRYRUN} $@";${COMMANDDRYRUN} $@; }
vvtee() { vv "$@"|tee -a ${repairlog}; }
test_repaired() {
    if [[ -z ${repairlogcur} ]];then return 1;fi
    if ( grep -qE "error reading txn header: invalid transaction" ${repairlogcur} );then return 1;fi
    if ( grep -qE "error reading txn header: bad transaction length" ${repairlogcur} );then return 1;fi
    return 0;
}
for i in $instances;do
    zodb=$W/var/filestorage/Data.${i}.fs;szodb=${zodb}
    log=$LOGS/${DATECHRONO}.$(basename ${zodb})
    repairlog=$log.repairlog
    orig=${zodb}.orig.${DATECHRONO}
    repaired=${zodb}.repaired
    echo > ${repairlog}
    if [[ -n ${USE_REPAIRED} ]];then
        vvtee bin/supervisorctl stop instance1-$i zeoserver-${i}
        # if [ ! -e ${orig} ];then
        #     vvtee mv ${zodb} ${orig}
        # else
        #     if [ -e ${orig} ] && [ -e ${zodb} ];then
        #         echo "Both zodb $zodb and $orig exist, please delete one"
        #     fi
        # fi
    fi
    if [ ! -e ${szodb} ];then szodb=${orig};fi && for j in ${orig} ${repaired};do vvtee rsync -aAvP ${szodb} ${j};done
    if [[ -n $STRIP_VERSIONS ]];then
        vvtee timeit bin/zopepy scripts/strip_versions.py ${repaired} ${zodb}.stripped 2>&1
        vvtee mv ${zodb}.stripped ${repaired}
    fi
    ix=0;repairlogcur=;while ! ( test_repaired );do
    ix=$((ix++));repairlogcur=$log.fsrecoverylog.$ix
        echo > "${repairlogcur}"
        if [[ -z ${NO_PACK-} ]];then
            vvtee timeit bin/zopepy ${fsrecover} -P 0 -f ${repaired} ${repaired}.tmp 2>&1 | tee -a ${repairlogcur}
        else
            vvtee timeit bin/zopepy ${fsrecover}      -f ${repaired} ${repaired}.tmp 2>&1 | tee -a ${repairlogcur}
        fi
        vvtee mv ${repaired}.tmp ${repaired}
    done
    if [[ -n ${USE_REPAIRED} ]];then
        vvtee mv ${repaired} ${zodb}
        vvtee bin/supervisorctl start instance1-$i zeoserver-${i}
    fi
done
