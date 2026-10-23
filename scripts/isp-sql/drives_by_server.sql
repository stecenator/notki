select cast(source_name as char(15)) src, -
		cast(pt.LIBRARY_NAME as char(17)) lib, -
		cast(dr.DRIVE_NAME as char(15)) drv, -
		cast(pt.device as char(42)) dev, -
		cast(dr.drive_serial as char(14)) serial, -
		cast(pt.online as char(7)) online -
	from drives dr, paths pt -
	where dr.drive_name = pt.destination_name -
	order by src, lib, drv