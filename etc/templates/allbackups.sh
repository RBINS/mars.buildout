#!/usr/bin/env bash
set +e
cd "${buildout:directory}"
instances="${instances}"
COMMANDDRYRUN=""
if [[ -n "$DRYRUN" ]];then COMMANDDRYRUN="echo";fi
for i in $instances;do
        $COMMANDDRYRUN bin/backup-$i && $COMMANDDRYRUN touch var/backup-$i-done
done
$COMMANDDRYRUN bin/backup && $COMMANDDRYRUN touch var/backup-done

