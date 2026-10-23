select cast(VOLUME_NAME as char(30)) VOL, -
        date(LAST_WRITE_DATE) "Last write" -
    from volumes -
    where days(current date) - days(LAST_READ_DATE)>90 -
    order by LAST_WRITE_DATE