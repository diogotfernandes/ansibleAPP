from flask import render_template, flash, redirect, request, url_for, jsonify
from app import app
from app.forms import CreateVM
import re, json, ansible_runner

from app.fun import _mkdocs, _apache2, _get_vms, _change_vm, _play_kvm

# def test():-
#     return "hello!"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/create_vm', methods=['GET','POST'])
def create_vm():
    form = CreateVM()

    if request.method == 'POST':
        form_data = form.data
        playbook = 'kvm_cloud_init.yml'

        data = _play_kvm(playbook, form_data)

        return data


    return render_template('kvm/create_vm.html', title='New Virtual Machine', form=form)


@app.route('/ansible')
def ansible():
    return render_template('ansible.html')

@app.route('/kvm')
def kvm():
    return render_template('kvm/index.html')

@app.route('/change_vm', methods=['GET','POST'])
def change_vm():
    if request.method == 'POST':
        req = request.form
        state = req.get("state")
        results = _change_vm(state)
    # return results
    if results['status'] == 'successful' :
         flash('successful', 'success')
         return render_template(
                  'kvm/get_vms.html',
                  results = results,
                  # events = results['events'],
                  # playbook_on_start=json.dumps(results['playbook_on_start'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  # runner_on_start=json.dumps(results['runner_on_start'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  # runner_on_ok=json.dumps(results['runner_on_ok'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  # playbook_on_stats=json.dumps(results['playbook_on_stats'], sort_keys = False, indent = 4, separators = (',', ': '))
                  vms=json.dumps(results['vms'], sort_keys = False, indent = 4, separators = (',', ': '))
              )
    else:
              flash('something wrong', 'danger')
              return render_template(
              'kvm/get_vms.html'
              )

@app.route("/api/get_vms", methods=['POST', 'GET'])
@app.route("/get_vms", methods=['POST'])
def get_vms():

    #Moving forward code
    results = _get_vms()

    url = request.path
    url = url.split('/')
    if url[1] == 'api':
        return results


    if results['status'] == 'successful' :
         flash('successful', 'success')
         return render_template(
                  'kvm/get_vms.html',
                  results = results,
                  # events = results['events'],
                  # playbook_on_start=json.dumps(results['playbook_on_start'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  # runner_on_start=json.dumps(results['runner_on_start'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  # runner_on_ok=json.dumps(results['runner_on_ok'], sort_keys = False, indent = 4, separators = (',', ': ')),
                  # playbook_on_stats=json.dumps(results['playbook_on_stats'], sort_keys = False, indent = 4, separators = (',', ': '))
                  vms=json.dumps(results['vms'], sort_keys = False, indent = 4, separators = (',', ': '))
              )
    else:
              flash('something wrong', 'danger')
              return render_template(
              'kvm/get_vms.html'
              )

@app.route("/mkdocs", methods=['POST'])
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

@app.route("/apache2/", methods=['POST'])
def apache2():
    #Moving forward code
    results = _apache2()

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
