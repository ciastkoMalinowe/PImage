import filters

def run(frame):
	return filters.apply(frame, filters.sharpen)
