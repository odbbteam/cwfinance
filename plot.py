# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.dates as mdates

def main(name, item, y, period):
    nx = list(range(0, len(y.split(','))))
    ny = list(map(int, y.split(',')))

    plt.plot(nx, ny)
    plt.axis([0, len(nx), min(ny)-1, max(ny)+1])
    plt.grid(True)
    plt.title(item)

    d = datetime.today() - timedelta(days=int(period))
    times = pd.date_range(d, periods=(288*int(period)), freq='5min')
    times = times.format(formatter=lambda x: x.strftime('%m-%d %H:%M'))
    plt.xticks(nx[0::8], times[0::(24 * int(period))], rotation='45', fontsize=10) #time ticks

    plt.savefig(name, bbox_inches='tight', dpi=70)
    plt.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    except IndexError:
        pass
