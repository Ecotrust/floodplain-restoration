#!flask/bin/python
from flask import Flask, jsonify, redirect, request
from bayesian.bbn import build_bbn

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
    return redirect("/static/main.html")

#@app.route('/climate/<lon>/<lat>', methods = ['GET'])
@app.route('/query', methods = ['GET'])
def query_CPT():
    args = dict([(k, float(v)/100.0) for k, v in request.args.items()])
    landscape_p = args.get('landscape')
    current_p = args.get('current')
    future_p = args.get('future')
    site_p = args.get('site')

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


    def f_restore(landscape, site, current, future, restore):
        """
         aa = itertools.product(*[[True, False]] * 4)
         for bb in aa: print bb
        """
        cpt = {
        #landscape, site, current, future) : restore
         (True, True, True, True): args.get('cpt1'),
         (True, True, True, False): args.get('cpt2'),
         (True, True, False, True): args.get('cpt3'),
         (True, True, False, False): args.get('cpt4'),
         (True, False, True, True): args.get('cpt5'),
         (True, False, True, False): args.get('cpt6'),
         (True, False, False, True): args.get('cpt7'),
         (True, False, False, False): args.get('cpt8'),
         (False, True, True, True): args.get('cpt9'),
         (False, True, True, False): args.get('cpt10'),
         (False, True, False, True): args.get('cpt11'),
         (False, True, False, False): args.get('cpt12'),
         (False, False, True, True): args.get('cpt13'),
         (False, False, True, False): args.get('cpt14'),
         (False, False, False, True): args.get('cpt15'),
         (False, False, False, False): args.get('cpt16')
        }
        p = cpt[(landscape, site, current, future)]
        if restore:
            return p
        else:
            return 1.0 - p

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
    prob = net.query()[('restore', True)]
    return jsonify({'restore': round(prob * 100, 0)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug = True)
