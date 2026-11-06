select PARENTRULENAME, -
        SUBRULENAME, -
        ACTION_TYPE, -
        cast(nodename as char(30)) Node -
    from sublrules -
    order by PARENTRULENAME, SUBRULENAME
