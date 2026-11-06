select RULENAME, -
        cast(TYPE as char(13)) Type, -
        cast(TGTSRV as char(25)) Target, -
        DURATION, -
        STARTTIME, -
        ACTIVE -
    from stgrules -
    where type in ('REPLICATE', 'NOREPLICATE')