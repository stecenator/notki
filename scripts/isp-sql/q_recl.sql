select cast(volume_name as char(30)) VOL, -
        PCT_UTILIZED, -
        STGPOOL_NAME -
    from volumes -
    where status='FULL' and PCT_UTILIZED<50 -
    order by STGPOOL_NAME, PCT_UTILIZED