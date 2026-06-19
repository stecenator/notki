#!/bin/bash
 
. /db2home/db2inst1/sqllib/db2profile
working_dir=/db2home/db2inst1/db2tsm/bkplogs
logfile="BACKUP_DAILY_`date +%d%m%Y`.log"
bkpdblist=/db2home/db2inst1/db2tsm/bkpdblist
touch $working_dir/$logfile > $working_dir/$logfile
echo "Current working directory $working_dir" >> $working_dir/$logfile
echo "Backup Procedure began `date`" >> $working_dir/$logfile
echo ""  >> $working_dir/$logfile
for i in `cat $bkpdblist`;
do
echo "=============================="  >> $working_dir/$logfile ;
echo "Beginning backup to TSM for database $i at `date`"  >> $working_dir/$logfile ;
echo "=============================="  >> $working_dir/$logfile ;
echo "command : db2 backup db $i online use TSM open 6 sessions dedup_device with 6 buffers buffer 8192 parallelism 6 include logs without prompting"  >> $working_dir/$logfile ;
db2 backup db $i online use TSM open 6 sessions dedup_device with 6 buffers buffer 8192 parallelism 6 include logs without prompting  >> $working_dir/$logfile ;
echo "Backup to TSM for database $i has finished at `date`"  >> $working_dir/$logfile ;
echo "=============================="  >> $working_dir/$logfile ;
bkpstate=$(grep "Backup successful" $working_dir/$logfile | tail -1 | awk '{print $2}');
if ! [[ "$bkpstate" == "successful." ]]
then
mail -s "db2 backup error" wilie.e@acme.com <<EOF
An error has occured during the backup of database $i !!!
Check the log file $working_dir/$logfile for details.
EOF
fi
echo ""  >> $working_dir/$logfile ;
done
echo "Backup Procedure ended `date`" >> $working_dir/$logfile
