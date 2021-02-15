import ansible_runner, os, json





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
        playbook =ansible_path+'/test.yml',
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
            # print("\n\n***************************************")
            # print(aux)
            # print(each_host_event['event'])
            # print(each_host_event)
            # print("Final status: " , r.stats)
            # print(r.stats)

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

    print("\n\n", runner_on_start, "\n\n")

    # print("\n\n\n************", mydict)res


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
