SELECT i, grp, parent FROM prince_grp_rel, prince_grp
	WHERE prince_grp_rel.child = prince_grp.i
	ORDER BY i