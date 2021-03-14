import utils
import matplotlib.pyplot as plt
import numpy as np 

dataFrom = 'ex1_data.dict.npy'
rawData = np.load(dataFrom, allow_pickle=True).item()
utils.displayData(rawData)

### Task 1.1 ###

# determine the stay in Jungfraujoch (in percentage) by checking the interval in which
# the derivative is "zero" and the air pressure is around 660 hPa
dx = 1000
der = utils.derivate(rawData, dx)

for key in der:
    fig, ax = plt.subplots()
    ax.plot(der[key])
    ax.set_title(key)
    plt.axvline(x=95, color='r', linestyle='-')
    plt.axvline(x=300, color='r', linestyle='-')
    plt.show()
    print('The percentage of time spent in Jungfraujoch is: {0:4.3f}'.format((300-95)*1000/len(rawData[key])))