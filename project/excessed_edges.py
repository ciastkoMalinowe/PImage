import filters

def run(frame):
	return filters.apply(frame, filters.excess_edges)
