from bayesian.bbn import build_bbn
from bayesian.factor_graph import build_graph
import matplotlib.pyplot as plt
import numpy as np

landscape_p = 0.5
current_p = 0.5
future_p = 0.5
site_p = 0.5

def f_landscape(landscape):
    if landscape:
        return landscape_p
    else:
        return 1 - landscape_p 

def f_current(current):
    if current:
        return current_p
    else:
        return 1 - current_p 

def f_future(future):
    if future:
        return future_p
    else:
        return 1 - future_p 

def f_site(site):
    if site:
        return site_p
    else:
        return 1 - site_p 


def generate_html():
    aa = itertools.product(*[[True, False]] * 4)
    html = "<table>\n"
    html += '<tr><td> landscape</td><td> site</td><td> current</td><td> future</td></tr>'
    for bb in aa:
        html += "<tr>"
        for cc in bb:
            html += '<td class="' + str(cc) + '"> ' + str(cc)  + '</td>'
        html += "</tr>\n"
    html += "</table>\n"
    print html


def f_restore(landscape, site, current, future, restore):
    """
     aa = itertools.product(*[[True, False]] * 4)
     for bb in aa: print bb
    """
    cpt = {
    #landscape, site, current, future) : restore
     (True, True, True, True): 0.8,
     (True, True, True, False): 0.0,
     (True, True, False, True): 1.0,
     (True, True, False, False): 0.1,
     (True, False, True, True): 0.3,
     (True, False, True, False): 0.0,
     (True, False, False, True): 0.5,
     (True, False, False, False): 0.1,
     (False, True, True, True): 0.0,
     (False, True, True, False): 0.0,
     (False, True, False, True): 0.0,
     (False, True, False, False): 0.0,
     (False, False, True, True): 0.0,
     (False, False, True, False): 0.0,
     (False, False, False, True): 0.0,
     (False, False, False, False): 0.0
    }
    p = cpt[(landscape, site, current, future)]
    if restore:
        return p
    else:
        return 1.0 - p


if __name__ == '__main__':
    levels = [True, False]
    net = build_bbn(
        f_landscape,
        f_site,
        f_current,
        f_future,
        f_restore,

        # assume simple binary
        domains=dict(
            landscape=levels,
            environment=levels,
            eco=levels,
            restore=levels
        )
    )

    import itertools 
    prod = itertools.product(
        xrange(0, 101, 25), # landscape metric
        xrange(0, 101, 25), # site metric
        xrange(0, 101, 25), # current metric
        xrange(0, 101, 25), # potential metric
    )
    results = []
    for x in prod:
        landscape_p = x[0] / 100.0
        site_p = x[1] / 100.0
        current_p = x[2] / 100.0
        future_p = x[3] / 100.0
        res = dict(net.query())[('restore', True)]
        results.append(res)

    print sum(results) / float(len(results))
    print min(results), max(results)

    mu, sigma = 100, 15
    hist, bins = np.histogram(results, bins=50)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()

    import ipdb; ipdb.set_trace()
