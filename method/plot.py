import matplotlib.pyplot as plt


def save_fig(x, y, label, label_x, label_y, locate, folder, name, scale):
    plt.figure()
    plt.plot(x, y, label=labels)
    
    plt.axis(scale)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.legend(loc=locate)
    plt.savefig('graph\\' + folder + name.split('.')[0] + '.jpg')
    plt.close()