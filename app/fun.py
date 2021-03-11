from datetime import datetime
import ansible_runner, os, json, yaml

def _play_kvm(playbook, options):

    root_path = "/home/diogo/Documents/ansibleAPP/ansible_data_dir/kvm"
    project_path = root_path + "/project"
    now = datetime.today().strftime('%Y%m%d%H%M%S')

    if os.path.isdir(root_path) == False:
        data = {
        'status': 'failed',
        'msg': 'The folder ' + root_path + ' is missing!'
        }
        return(data)

    if options['userdata_sudo']:
        en_sudo = "ALL=(ALL) NOPASSWD:ALL"
    else:
        en_sudo = "False"

    extra_vars = {
        'kvm_new_vm_qcow2_name': options['userdata_fqdn'] + '.qcow2',
        'kvm_new_vm_qcow_size': options['qcow2_size'],
        'kvm_new_vm_user_data': {
            'hostname': options['userdata_hostname'],
            'fqdn': options['userdata_fqdn'],
            'manage_etc_hosts': options['userdata_manage_etc_hosts'],
            'users' :
            [{
                'name': options['userdata_user_name'],
                'groups': options['userdata_user_group'],
                'home': '/home/' + options['userdata_hostname'],
                'shell': '/bin/bash',
                'ssh-authorized-keys': [options['userdata_user_ssh_key']],
                'sudo': en_sudo
            }],
            'ssh_pwauth': True,
            'disable_root': options['userdata_disable_root'],
            'chpasswd': {
                'list': options['userdata_user_chpasswd'],
                'expire': options['userdata_expire']
                },
        },
        'kvm_new_vm_meta_data': {
           'instance-id': options['userdata_hostname'],
           'local-hostname': options['userdata_hostname'],
       },
       'kvm_static_network': {
           'interface': options['network_interface'],
           'dhcp4': options['network_dhcp4'],
           'ipv4': options['network_ipv4'],
           'gw': options['network_gw'],
           'ns1': options['network_ns1'],
           'ns2': options['network_ns2'],
           'search': options['network_search'],
       },

    }

    print(yaml.dump(extra_vars))
    print("\n\n")
    print(options)

    # return(yaml.dump(extra_vars))
    # https://ansible-runner.readthedocs.io/en/stable/source/ansible_runner.html#module-ansible_runner.interface
    r = ansible_runner.run(
        playbook = playbook,
        json_mode = False,
        quiet = True, # if True no output to console
        rotate_artifacts = 10, # keep n artifact directories; 0 to disable
        private_data_dir = root_path,
        extravars=extra_vars,
        ident = 'create_vm_' + str(now),
    )

    if(r.status == 'successful'):
        data = {
            'status': r.status,
            'rc': r.rc,
            'extra_vars': extra_vars
            }
    else:
        data = {
        'status': r.status,
        'msg': 'Algo correu mal...'
        }
    return (data)


def _change_vm(state):


    root_path = "/home/diogo/Documents/ansibleAPP/ansible_data_dir/kvm"
    project_path = root_path + "/project"
    now = datetime.today().strftime('%Y%m%d%H%M%S')
    #
    # var: state => get desired state and target vm
    # state = 'start_ns1.alcafaz.test'; state[0] => tags; state[1] => vm
    state = state.split('_')
    tags = state[0]
    kvm_name = state[1]

    if os.path.isdir(root_path) == False:
        try:
            os.mkdir(root_path)
        except OSError:
            print ("Creation of the directory %s failed" % root_path)
        else:
            print ("Successfully created the directory %s " % root_path)

    # https://ansible-runner.readthedocs.io/en/stable/source/ansible_runner.html#module-ansible_runner.interface
    r = ansible_runner.run(
        playbook = project_path +'/change_state.yml',
        json_mode = False,
        # quiet = True, # if True no output to console
        rotate_artifacts = 10, # keep n artifact directories; 0 to disable
        # fact_cache = 'test',
        private_data_dir = root_path,
        tags = tags,
        extravars={"kvm_name": kvm_name},
        ident = 'change_vm_' + str(now),
    )

    facts = {}
    vms = {}

    for each_host_event in r.events:
        if(each_host_event['event'] == 'runner_on_ok' ):
            if (each_host_event['event_data']['task_action'] == 'gather_facts'):
                facts["ansible_hostname"] = each_host_event['event_data']['res']['ansible_facts']['ansible_hostname']
                facts["ansible_user_id"] = each_host_event['event_data']['res']['ansible_facts']['ansible_user_id']
                facts["ansible_user_gecos"] = each_host_event['event_data']['res']['ansible_facts']['ansible_user_gecos']
            if (each_host_event['event_data']['task'] == 'kvm_final_info'):
                vms = each_host_event['event_data']['res']['kvm_final_info']

    if(r.status == 'successful'):
        data = {
            'status': r.status,
            'rc': r.rc,
            'vms' : vms
        }
    else:
        data = {
        'status': r.status
        }

    return (data)


def _get_vms():

    root_path = "/home/diogo/Documents/ansibleAPP/ansible_data_dir/kvm"
    project_path = root_path + "/project"

    if os.path.isdir(root_path) == False:
        try:
            os.mkdir(root_path)
        except OSError:
            print ("Creation of the directory %s failed" % root_path)
        else:
            print ("Successfully created the directory %s " % root_path)

    now = datetime.today().strftime('%Y%m%d%H%M%S')
    # https://ansible-runner.readthedocs.io/en/stable/source/ansible_runner.html#module-ansible_runner.interface
    r = ansible_runner.run(
        playbook = project_path +'/list.yml',
        json_mode = False,
        rotate_artifacts = 10, # keep n artifact directories; 0 to disable
        private_data_dir = root_path,
        fact_cache_type = 'jsonfile',
        ident = 'list_vms_' + str(now),
    )

    facts = {}
    vms = {}

    for each_host_event in r.events:
        if(each_host_event['event'] == 'runner_on_ok' ):
            if (each_host_event['event_data']['task_action'] == 'gather_facts'):
                facts["ansible_hostname"] = each_host_event['event_data']['res']['ansible_facts']['ansible_hostname']
                facts["ansible_user_id"] = each_host_event['event_data']['res']['ansible_facts']['ansible_user_id']
                facts["ansible_user_gecos"] = each_host_event['event_data']['res']['ansible_facts']['ansible_user_gecos']
            if (each_host_event['event_data']['task'] == 'kvm_vms_info'):
                vms = each_host_event['event_data']['res']['kvm_info']


    if(r.status == 'successful'):
        data = {
            'status': r.status,
            'rc': r.rc,
            'vms' : vms
        }
    else:
        data = {
        'status': r.status
        }

    return (data)


def _apache2():

    ansible_path = "/etc/ansible"
    path = "/tmp/demo"
    now = datetime.today().strftime('%Y%m%d%H%M%S')

    if os.path.isdir(path) == False:
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

    # https://ansible-runner.readthedocs.io/en/stable/source/ansible_runner.html#module-ansible_runner.interface
    r = ansible_runner.run(
        playbook =ansible_path+'/02.simple-apache.yml',
        json_mode = False,
        private_data_dir = path,
        rotate_artifacts = 2, # keep n artifact directories; 0 to disable
        host_pattern = 'web',
        inventory = '/etc/ansible/inventories/alcafaz.test/hosts',
        ident = 'apache2_' + str(now),
    )

#playbook_on_start
#runner_on_start
#runner_on_ok
#playbook_on_stats

    task_start = 0
    runner_on_start = {}
    task_ok = 0
    runner_on_ok = {}
    facts = {}

    for each_host_event in r.events:

            if(each_host_event['event'] == 'playbook_on_start' ):
                playbook_on_start = each_host_event

            if(each_host_event['event'] == 'runner_on_start' ):
                # runner_on_start = each_host_event
                runner_on_start["task_" + str(task_start)] = {}
                runner_on_start["task_" + str(task_start)]['name'] = each_host_event['event_data']['task']
                runner_on_start["task_" + str(task_start)]['play_pattern'] = each_host_event['event_data']['play_pattern']
                runner_on_start["task_" + str(task_start)]['task_action'] = each_host_event['event_data']['task_action']
                runner_on_start["task_" + str(task_start)]['task_args'] = each_host_event['event_data']['task_args']
                runner_on_start["task_" + str(task_start)]['task_path'] = each_host_event['event_data']['task_path']
                if('role' in each_host_event['event_data']):
                    runner_on_start["task_" + str(task_start)]['role'] = each_host_event['event_data']['role']
                runner_on_start["task_" + str(task_start)]['host'] = each_host_event['event_data']['host']
                runner_on_start["task_" + str(task_start)]['playbook'] = each_host_event['event_data']['playbook']
                task_start = task_start+1

            if(each_host_event['event'] == 'runner_on_ok' ):
                if(each_host_event['event_data']['task_action'] == 'gather_facts'):
                    facts = each_host_event['event_data']
                # runner_on_ok = each_host_event
                print("\n++++++++++\n\n", each_host_event, "\n++++++++++\n\n")
                runner_on_ok["task_" + str(task_ok)] = {}
                runner_on_ok["task_" + str(task_ok)]['name'] = each_host_event['event_data']['task']
                runner_on_ok["task_" + str(task_ok)]['play_pattern'] = each_host_event['event_data']['play_pattern']
                runner_on_ok["task_" + str(task_ok)]['task_action'] = each_host_event['event_data']['task_action']
                runner_on_ok["task_" + str(task_ok)]['task_args'] = each_host_event['event_data']['task_args']
                runner_on_ok["task_" + str(task_ok)]['task_path'] = each_host_event['event_data']['task_path']
                if('role' in each_host_event['event_data']):
                    runner_on_ok["task_" + str(task_ok)]['role'] = each_host_event['event_data']['role']
                runner_on_ok["task_" + str(task_ok)]['host'] = each_host_event['event_data']['host']
                runner_on_ok["task_" + str(task_ok)]['remote_addr'] = each_host_event['event_data']['remote_addr']
                runner_on_ok["task_" + str(task_ok)]['playbook'] = each_host_event['event_data']['playbook']
                if('cmd' in each_host_event['event_data']['res']):
                    runner_on_ok["task_" + str(task_ok)]['cmd'] = each_host_event['event_data']['res']['cmd']
                if('invocation' in each_host_event['event_data']['res']):
                    runner_on_ok["task_" + str(task_ok)]['invocation'] = each_host_event['event_data']['res']['invocation']
                task_ok = task_ok+1


            if(each_host_event['event'] == 'playbook_on_stats' ):
                playbook_on_stats = each_host_event


    if(r.status == 'successful'):
        data = {
            'status': r.status,
            'rc': r.rc,
            # 'events' : json.dumps(mydict, indent=4, sort_keys=True),
            'playbook_on_start' : playbook_on_start,
            'runner_on_start' : runner_on_start,
            'runner_on_ok': runner_on_ok,
            'playbook_on_stats': playbook_on_stats,
            'facts': facts
        }
    else:
        data = {
        'status': r.status
        }

    return (data)


def _mkdocs():

    ansible_path = "/etc/ansible"
    path = "/tmp/demo"
    now = datetime.today().strftime('%Y%m%d%H%M%S')

    if os.path.isdir(path) == False:
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)


    r = ansible_runner.run(
        playbook =ansible_path+'/05.push-mkdocs-to-remote.yml',
        json_mode = False,
        private_data_dir = path,
        host_pattern = 'localhost',
        rotate_artifacts = 5, # keep n artifact directories; 0 to disable
        ident = 'push_mkdocs_' + str(now),
    )

#playbook_on_start
#runner_on_start
#runner_on_ok
#playbook_on_stats

    task_start = 0
    runner_on_start = {}
    task_ok = 0
    runner_on_ok = {}



    for each_host_event in r.events:

            if(each_host_event['event'] == 'playbook_on_start' ):
                playbook_on_start = each_host_event

            if(each_host_event['event'] == 'runner_on_start' ):
                # runner_on_start = each_host_event
                runner_on_start["task_" + str(task_start)] = {}
                runner_on_start["task_" + str(task_start)]['name'] = each_host_event['event_data']['task']
                runner_on_start["task_" + str(task_start)]['play_pattern'] = each_host_event['event_data']['play_pattern']
                runner_on_start["task_" + str(task_start)]['task_action'] = each_host_event['event_data']['task_action']
                runner_on_start["task_" + str(task_start)]['task_args'] = each_host_event['event_data']['task_args']
                runner_on_start["task_" + str(task_start)]['task_path'] = each_host_event['event_data']['task_path']
                if('role' in each_host_event['event_data']):
                    runner_on_start["task_" + str(task_start)]['role'] = each_host_event['event_data']['role']
                runner_on_start["task_" + str(task_start)]['host'] = each_host_event['event_data']['host']
                runner_on_start["task_" + str(task_start)]['playbook'] = each_host_event['event_data']['playbook']
                task_start = task_start+1

            if(each_host_event['event'] == 'runner_on_ok' ):
                # runner_on_ok = each_host_event
                runner_on_ok["task_" + str(task_ok)] = {}
                runner_on_ok["task_" + str(task_ok)]['name'] = each_host_event['event_data']['task']
                runner_on_ok["task_" + str(task_ok)]['play_pattern'] = each_host_event['event_data']['play_pattern']
                runner_on_ok["task_" + str(task_ok)]['task_action'] = each_host_event['event_data']['task_action']
                runner_on_ok["task_" + str(task_ok)]['task_args'] = each_host_event['event_data']['task_args']
                runner_on_ok["task_" + str(task_ok)]['task_path'] = each_host_event['event_data']['task_path']
                if('role' in each_host_event['event_data']):
                    runner_on_ok["task_" + str(task_ok)]['role'] = each_host_event['event_data']['role']
                runner_on_ok["task_" + str(task_ok)]['host'] = each_host_event['event_data']['host']
                runner_on_ok["task_" + str(task_ok)]['remote_addr'] = each_host_event['event_data']['remote_addr']
                runner_on_ok["task_" + str(task_ok)]['playbook'] = each_host_event['event_data']['playbook']
                if('cmd' in each_host_event['event_data']['res']):
                    runner_on_ok["task_" + str(task_ok)]['cmd'] = each_host_event['event_data']['res']['cmd']
                if('invocation' in each_host_event['event_data']['res']):
                    runner_on_ok["task_" + str(task_ok)]['invocation'] = each_host_event['event_data']['res']['invocation']
                task_ok = task_ok+1

            if(each_host_event['event'] == 'playbook_on_stats' ):
                playbook_on_stats = each_host_event


    print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print ("\n+++++STATUS: ", r.status)
    print ("\n+++++rc code: ", r.rc)
    print ("\n+++++STDOUT: ", r.stdout)
    print ("\n+++++STATS: ", r.stats)
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

    if(r.status == 'successful'):
        data = {
            'status': r.status,
            'rc': r.rc,
            # 'events' : json.dumps(mydict, indent=4, sort_keys=True),
            'playbook_on_start' : playbook_on_start,
            'runner_on_start' : runner_on_start,
            'runner_on_ok': runner_on_ok,
            'playbook_on_stats': playbook_on_stats
        }
    else:
        data = {
        'status': r.status
        }

    return (data)
