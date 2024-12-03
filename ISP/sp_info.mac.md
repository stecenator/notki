# Makro zbierające informacje o Protekcie

Puszczać najlepiej tak: `dsmadmc -se=mój_server -id=ja -pa=moje_hasło -itemcommit -tab`:

```
q system
select DOMAIN_NAME,CLASS_NAME,VEREXISTS,VERDELETED,RETEXTRA,RETONLY,DESTINATION from bu_copygroups  where set_name='ACTIVE'
select DOMAIN_NAME,CLASS_NAME,RETVER,DESTINATION from ar_copygroups where set_name='ACTIVE'
select NODE_NAME,DOMAIN_NAME,PLATFORM_NAME,CLIENT_OS_LEVEL,(days(current date) - days(LASTACC_TIME)) days_ina,CLIENT_VERSION,CLIENT_RELEASE,CLIENT_LEVEL,CLIENT_SUBLEVEL,APPLICATION_VERSION,APPLICATION_RELEASE,APPLICATION_LEVEL,APPLICATION_SUBLEVEL from nodes
```