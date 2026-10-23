select cast(library_name as char(15)) Libr, -
        status, -
        count(volume_name) as tape -
    from libvolumes -
    group by library_name, status