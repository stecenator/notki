select cast(DOMAIN_NAME as char(20)) Dom, -
		cast(set_name as char(20)) Set, -
		cast(CLASS_NAME as char(20)) Mgmt, - 
		VEREXISTS VerE, VERDELETED VerD, RETEXTRA RetE, RETONLY RetO, -
		cast(DESTINATION as char(20)) as Dest - 
	from bu_copygroups -
	order by DOMAIN_NAME, SET_NAME, CLASS_NAME