select STGPOOL_NAME, -
	cast(case -
		when Status='FULL' and PCT_UTILIZED>=50 then 'FULL' -
		when Status='FULL' and PCT_UTILIZED<49 then 'RECLAIM' -
		else STATUS -
		END as char(10)) as stat, -
	count(volume_name) as vols -
from volumes -
group by STGPOOL_NAME, -
	cast(case -
		when Status='FULL' and PCT_UTILIZED>=50 then 'FULL' -
		when Status='FULL' and PCT_UTILIZED<49 then 'RECLAIM' -
		else STATUS END as char(10)) -
order by stgpool_name, stat
