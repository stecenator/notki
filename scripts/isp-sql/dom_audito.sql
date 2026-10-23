select n.domain_name, -
	    dec(sum(o.total_mb)/1024, 9,1) GiB -
    from nodes n , auditocc o -
    where n.node_name=o.node_name -
    group by n.domain_name -
    order by n.domain_name