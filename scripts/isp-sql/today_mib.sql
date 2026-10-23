select cast(entity as char(20)) who, -
        sum(seconds_between(end_time, start_time))as secs, -
        sum(bytes)/1024/1024 MiB -
    from summary -
    where activity='BACKUP' and  date(current date) = date(start_time) -
    group by entity