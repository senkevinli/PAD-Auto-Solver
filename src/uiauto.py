from uiautomator import device as d

print(d.info)
d.swipePoints([(500,500),(500,1000), (700, 1000)], steps=10)