from time import time

start = time()
for i in range(100):
    print i
stop = time()
print
print float("%.4f"%(stop - start))
