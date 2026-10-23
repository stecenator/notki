select cast(DOMAIN_NAME as char(20)) Dom, -
		cast(CLASS_NAME as char(20)) Mgmt, -
		RETVER RetV, -
		cast(DESTINATION as char(20)) as Dest -  
    from ar_copygroups order by DOMAIN_NAME, SET_NAME, CLASS_NAME