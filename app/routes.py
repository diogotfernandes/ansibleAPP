from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app
import re, json, ansible_runner

from app.fun import _mkdocs

# def test():-
#     return "hello!"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/background_process_test')
def background_process_test():
    a = ad_hoc()
    print(a["status"])
    return a


@app.route('/ansible')
def ansible():
    return render_template('ansible.html')


@app.route("/mkdocs/", methods=['POST'])
def mkdocs():
    #Moving forward code
    results = _mkdocs()

    if results['status'] == 'successful' :
         flash('successful', 'success')
         return render_template(
                  'index.html',
                  results = results,
                  # events = results['events'],
                  playbook_on_start=json.dumps(results['playbook_on_start'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  runner_on_start=json.dumps(results['runner_on_start'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  runner_on_ok=json.dumps(results['runner_on_ok'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  playbook_on_stats=json.dumps(results['playbook_on_stats'], sort_keys = False, indent = 4, separators = (',', ': '))
              )
    else:
              flash('something wrong', 'danger')
              return render_template(
              'index.html'
              )
    # print(results)
