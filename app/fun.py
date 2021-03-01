from datetime import datetime
import ansible_runner, os, json

def _change_vm(state):


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

    state = state.split('_')
    tags = state[0]
    kvm_name = state[1]

    r = ansible_runner.run(
        playbook = project_path +'/change_state.yml',
        json_mode = True,
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

    print("\n\n")
    print(vms)
    print(r.status)
    print("\n")
    print(state)
    print("\n\n")

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

    r = ansible_runner.run(
        playbook = project_path +'/list.yml',
        json_mode = True,
        private_data_dir = root_path,
        fact_cache_type = 'jsonfile',
        ident = 'list_vms_' + str(now),
    )

#playbook_on_start
#runner_on_start
#runner_on_ok
#playbook_on_stats

    facts = {}
    vms = {}

    for each_host_event in r.events:

            # if(each_host_event['event'] == 'playbook_on_start' ):
            #     playbook_on_start = each_host_event
            #
            # if(each_host_event['event'] == 'runner_on_start' ):
            #     # runner_on_start = each_host_event
            #     runner_on_start["task_" + str(task_start)] = {}
            #     runner_on_start["task_" + str(task_start)]['name'] = each_host_event['event_data']['task']
            #     runner_on_start["task_" + str(task_start)]['play_pattern'] = each_host_event['event_data']['play_pattern']
            #     runner_on_start["task_" + str(task_start)]['task_action'] = each_host_event['event_data']['task_action']
            #     runner_on_start["task_" + str(task_start)]['task_args'] = each_host_event['event_data']['task_args']
            #     runner_on_start["task_" + str(task_start)]['task_path'] = each_host_event['event_data']['task_path']
            #     if('role' in each_host_event['event_data']):
            #         runner_on_start["task_" + str(task_start)]['role'] = each_host_event['event_data']['role']
            #     runner_on_start["task_" + str(task_start)]['host'] = each_host_event['event_data']['host']
            #     runner_on_start["task_" + str(task_start)]['playbook'] = each_host_event['event_data']['playbook']
            #     task_start = task_start+1

            if(each_host_event['event'] == 'runner_on_ok' ):
                # runner_on_ok = each_host_event
                # print("\n++++++++++\n\n", each_host_event, "\n++++++++++\n\n")
                # runner_on_ok["task_" + str(task_ok)] = {}
                # runner_on_ok["task_" + str(task_ok)]['name'] = each_host_event['event_data']['task']
                # runner_on_ok["task_" + str(task_ok)]['play_pattern'] = each_host_event['event_data']['play_pattern']
                # runner_on_ok["task_" + str(task_ok)]['task_action'] = each_host_event['event_data']['task_action']
                # runner_on_ok["task_" + str(task_ok)]['task_args'] = each_host_event['event_data']['task_args']
                # runner_on_ok["task_" + str(task_ok)]['task_path'] = each_host_event['event_data']['task_path']
                # if('role' in each_host_event['event_data']):
                #     runner_on_ok["task_" + str(task_ok)]['role'] = each_host_event['event_data']['role']
                # runner_on_ok["task_" + str(task_ok)]['host'] = each_host_event['event_data']['host']
                # runner_on_ok["task_" + str(task_ok)]['remote_addr'] = each_host_event['event_data']['remote_addr']
                # runner_on_ok["task_" + str(task_ok)]['playbook'] = each_host_event['event_data']['playbook']
                # runner_on_ok["task_" + str(task_ok)]['res'] = each_host_event['event_data']['res']
                # task_ok = task_ok+1
                if (each_host_event['event_data']['task_action'] == 'gather_facts'):
                    facts["ansible_hostname"] = each_host_event['event_data']['res']['ansible_facts']['ansible_hostname']
                    facts["ansible_user_id"] = each_host_event['event_data']['res']['ansible_facts']['ansible_user_id']
                    facts["ansible_user_gecos"] = each_host_event['event_data']['res']['ansible_facts']['ansible_user_gecos']


                if (each_host_event['event_data']['task'] == 'kvm_vms_info'):
                    vms = each_host_event['event_data']['res']['kvm_info']


            # if(each_host_event['event'] == 'playbook_on_stats' ):
            #     playbook_on_stats = each_host_event


    # Given a host name, this will return all task events executed on that host
    # print("\n\nhost_events\n\n" , list(r.host_events('localhost')))


    if(r.status == 'successful'):
        data = {
            'status': r.status,
            'rc': r.rc,
            # 'events' : json.dumps(mydict, indent=4, sort_keys=True),
            # 'playbook_on_start' : playbook_on_start,
            # 'runner_on_start' : runner_on_start,
            # 'runner_on_ok': runner_on_ok,
            # 'playbook_on_stats': playbook_on_stats,
            'vms' : vms
        }
    else:
        data = {
        'status': r.status
        }

    print("\n\n")
    print(vms)
    print(r.status)
    print("\n\n")

    return (data)


def _apache2():

    ansible_path = "/etc/ansible/playbooks"
    path = "/tmp/demo"

    if os.path.isdir(path) == False:
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)


    r = ansible_runner.run(
        playbook =ansible_path+'/webserver.yml',
        json_mode = True,
        private_data_dir = path,
        host_pattern = 'web',
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
            'playbook_on_stats': playbook_on_stats
        }
    else:
        data = {
        'status': r.status
        }

    return (data)


def _mkdocs():

    ansible_path = "/etc/ansible/playbooks"
    path = "/tmp/demo"

    if os.path.isdir(path) == False:
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)


    r = ansible_runner.run(
        playbook =ansible_path+'/sync_mkdocs.yml',
        json_mode = True,
        private_data_dir = path,
        host_pattern = 'localhost',
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
                runner_on_ok["task_" + str(task_ok)]['role'] = each_host_event['event_data']['role']
                runner_on_ok["task_" + str(task_ok)]['host'] = each_host_event['event_data']['host']
                runner_on_ok["task_" + str(task_ok)]['remote_addr'] = each_host_event['event_data']['remote_addr']
                runner_on_ok["task_" + str(task_ok)]['playbook'] = each_host_event['event_data']['playbook']
                runner_on_ok["task_" + str(task_ok)]['cmd'] = each_host_event['event_data']['res']['cmd']
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




# def ad_hoc():
#
#     ansible_path = "/etc/ansible"
#     path = "/tmp/demo"
#
#     if os.path.isdir(path) == False:
#         try:
#             os.mkdir(path)
#         except OSError:
#             print ("Creation of the directory %s failed" % path)
#         else:
#             print ("Successfully created the directory %s " % path)
#
#
#
#     # r = ansible_runner.run(
#     # private_data_dir='/tmp/demo',
#     # host_pattern='localhost',
#     # module='shell', module_args='whoami')
#     # print('stats-> ' , r.stats)
#     # print('events-> ' , r.events)
#     # print('status-> ' , r.status)
#     #
#     # print('status_handler-> ' , r.status_handler)
#
#     r = ansible_runner.run_async(
#         playbook ='',
#         json_mode = True,
#         private_data_dir = path,
#         host_pattern = 'localhost',
#         module = 'shell',
#         module_args = 'whoami'
#     )
#
#     print(r[1].status)
#
#
# #playbook_on_start
# #runner_on_start
# #runner_on_ok
# #playbook_on_stats
#
# # run:          r ->  <ansible_runner.runner.Runner object at 0x7f03f2d0aa60>
# # run_async:    r ->  (<Thread(Thread-4, started daemon 140586842289728)>, <ansible_runner.runner.Runner object at 0x7fdcecdab0a0>)
#
#     # print("\n\n")
#     # print("r -> " , r[1].stats)
#     # print("\n\n")
#
#     for each_host_event in r[1].events:
#             # print(each_host_event['event'])
#
#             if(each_host_event['event'] == 'playbook_on_start' ):
#                 playbook_on_start = each_host_event
#
#             if(each_host_event['event'] == 'runner_on_start' ):
#                 runner_on_start = each_host_event
#
#             if(each_host_event['event'] == 'runner_on_ok' ):
#                 runner_on_ok = each_host_event
#                 # print('TASK: ' , each_host_event['event_data']['task'])
#                 # print('HOST: ' , each_host_event['event_data']['host'])
#                 # print('STDOUT: '  , each_host_event['event_data']['res']['stdout'])
#                 # res = each_host_event['event_data']['res']['stdout'],
#
#             if(each_host_event['event'] == 'playbook_on_stats' ):
#                 playbook_on_stats = each_host_event
#
#
#
#     # app.logger.info('stdout: ' , r.stdout)
#     # print('events: ' , r.events)
#     # print('stats: ' , r.stats)
#     # print(r.get_fact_cache('localhost'))
#
#     if(r[1].status == 'successful'):
#         print(r[1].status)
#
#     data ={
#     'status': r[1].status,
#     'rc': r[1].rc,
#     'playbook_on_start' : playbook_on_start,
#     'runner_on_start' : runner_on_start,
#     'runner_on_ok': runner_on_ok,
#     'playbook_on_stats': playbook_on_stats
#     }
#
#     return (data)
