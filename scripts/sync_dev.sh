#!/bin/bash
cd "$(dirname $(readlink -f "$0"))/.."
set -eo pipefail
if [[ -n ${SHELL_DEBUG-} ]];then set -x;fi
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
de=""
de="--delete-excluded"
DRYRUN=${DRYRUN:-${DRY_RUN-}}
W=$(pwd)
LOGS=$W/var/log
DATECHRONO=${DATECHRONO:-$(date +"%Y%m%d%H%M%S")}
COMMANDDRYRUN="$(if [[ -n "$DRYRUN" ]];then echo "echo";fi)"
STRIP_VERSIONS=${STRIP_VERSIONS-}
instances="${@}"
timeit() { date -Isec >&2;vv "$@";date -Isec >&2; }
log() { echo "$@" >&2; }
vv() { log "${COMMANDDRYRUN} $@";${COMMANDDRYRUN} $@; }
vvtee() { vv "$@"|tee -a ${repairlog}; }
#vv rsync -aAvP  --exclude="*.log" --exclude=.installed.cfg --exclude=.mr.developer.cfg --exclude=var --exclude=parts ./ ../mars.dev/
vv rsync -aAvP --delete $de --exclude="./tmp/*" --exclude="*anthropologydebug*" --exclude="log"   --exclude="filestorage/*.tmp" --exclude="filestorage/*.fs.orig.20*" --exclude="filestorage/*repair*" --exclude="*backup*"  --exclude="blobstorage/*.old" ./var/ ../mars.dev/var/

