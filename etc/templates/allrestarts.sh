#!/usr/bin/env bash
set +e
cd "${buildout:directory}"
instances="${instances}"
COMMANDDRYRUN=""
if [[ -n "$DRYRUN" ]];then COMMANDDRYRUN="echo";fi
for i in $instances;do
        $COMMANDDRYRUN bin/supervisorctl restart instance1-$i
done
$COMMANDDRYRUN bin/supervisorctl restart instance1

