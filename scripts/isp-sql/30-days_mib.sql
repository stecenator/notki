select cast(entity as char(20)) Who, - 
        cast(activity as char(15)) as What, -
        dec(dec(sum(bytes), 30,0)/1048576, 10, 2) as MiBs, -
        date(start_time) as day -
    from summary_extended -
    where activity in ('BACKUP', 'ARCHIVE') -
    group by entity, date(start_time), activity -
    having sum(bytes)>0 -
    order by day, MiBs desc