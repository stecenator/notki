select cast(node_name as char(15)) Node,cast(DOMAIN_NAME as char(20)) Domain, -
        cast(CLIENT_VERSION || '.' || CLIENT_RELEASE || '.' || CLIENT_LEVEL || '.' || CLIENT_SUBLEVEL as char(12)) as ver, -
        cast(APPLICATION_VERSION || '.' || APPLICATION_RELEASE || '.' || APPLICATION_LEVEL || '.' || APPLICATION_SUBLEVEL as char(15)) as app, -
        PLATFORM_NAME, -
        cast(CLIENT_OS_LEVEL as char(20)) as os_ver, -
        cast(TCP_NAME as char(32)) as hostname, -
        cast(TCP_ADDRESS as char(16)) as ip, -
        dec(days(current date) - days(LASTACC_TIME), 6,0) as LAST_ACC -
    from nodes -
    order by LAST_ACC desc, NODE_NAME asc