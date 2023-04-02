#!/usr/bin/env bash
set +e
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
cd "${buildout:directory}"
task=${task} && f="var/$task" && rm -f "$f"
timeit() { echo "$(date -Isec): $@" >> $f; }
instances="${instances}"
maininstance="${maininstance}"
COMMANDDRYRUN=""
timeit
if [[ -n "$DRYRUN" ]];then COMMANDDRYRUN="echo";fi
for i in $instances;do
        timeit $task-$i-start && $COMMANDDRYRUN bin/backup-$i && timeit $task-$i-done
done
if [ "x$maininstance" = "x1" ];then
   timeit $task-start && $COMMANDDRYRUN bin/backup && timeit $task-done
fi
timeit
