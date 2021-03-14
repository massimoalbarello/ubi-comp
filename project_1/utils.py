import matplotlib.pyplot as plt

def displayData(data):
    fig, ax = plt.subplots()
    for key in data:
        ax.plot(data[key], label=key)
    ax.legend(loc='lower right')
    ax.set_title('Raw data')
    plt.axhline(y=6600000, color='r', linestyle='-')    # Jungfraujoch has air pressure around 660 hPa
    plt.show()

def derivate(data, dx):
    der = {}
    for key in data:
        x = 0
        der[key] = []
        while x < len(data[key]) - dx:
            der[key].append((data[key][x+dx] - data[key][x]) / dx)
            x = x + dx
    return der