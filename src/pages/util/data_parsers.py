
import os
import subprocess

# def fake_data():
#     """
#     For test only
#     """
#     fake_jobs_data = [(1, "Single_cell","Silly_Mokey","29-10-2020T15:57",'Complete',"0","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"), 
#                       (2,"Super SC","Envy_John","30-01-2020T15:57",'Pending',"0","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"),
#                       (3,"Vib 10X","Careful_lizard","27-10-2020T15:57",'Running',"0","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"),
#                       (4,"SC-Genomics","Donald_duck","30-01-2020T15:57",'Failed',"127","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"),
    
#     ]

#     return fake_jobs_data

def _paser_string_stats(stats):
    """ 
        This fucntion is needed because the stats are read from stdout, which cames as a string not a list of tuples :(

    """

    lst_lst_stats = []
    p_list = []
    rep_pattern = ['[', ']', '(', ')', '\\n','b"', '\'', ' ','"' ]

    for rep in rep_pattern:
        stats = stats.replace(rep,'')


    list_stats = stats.split(',')
    
    for i, l in enumerate(list_stats):
        p_list.append(l)
        if (i + 1) % 11 == 0:
            lst_lst_stats.append(p_list)
            p_list = []

    return lst_lst_stats
   


def get_db_stats(user):
    """
        This function fetches the jobs from the database and 
        :param:
        :return jobs: A dict of dict  job={ "pipeline_name" - "run_name": { "job_id": "14074",
                                                                            "PI": "PI_user_name",
                                                                            "run_name": "Silly Mokey",
                                                                            "elapsed": "00:30:04",
                                                                            "start": "29-10-2020T15:57",
                                                                            "state": "COMPLETED",
                                                                            "exit": "0"",
                                                                            "submission_dir": "/path/",
                                                                            "level": danger
                                                                            "pipeline_name": "Single_cell",
                                                                           }, 
    """
    
    level = {
        'COMPLETED' : 'success',
        'PENDING': 'primary',
        'REQUEUED': 'primary',
        'SUSPENDED': 'primary',
        'RESIZING': 'warning',
        'RUNNING': 'warning',
        'CANCELLED': 'danger',
        'BOOT_FAIL': 'danger',
        'DEADLINE': 'danger',
        'NODE_FAIL': 'danger',
        'OUT_OF_MEMORY': 'danger',
        'PREEMPTED': 'danger',
        'REVOKED': 'danger',
        'TIMEOUT': 'danger',
        'FAILED': 'danger'
    }
    
    jobs = {}
    

    ### Get Stats from DB ################################
    cmd = ['/home/dmorais/anaconda3/envs/pyjob/bin/python', '/home/dmorais/projects/pyjobs/pyselect.py',
          '-u', user]


    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
            
        stdout_value, stderr_value = proc.communicate()
        str_jobs = str(stdout_value)   
        db_jobs = _paser_string_stats(str_jobs)

        for tuple_job in db_jobs:
            for j in db_jobs:
                color = level[j[6]]

                jobs[j[10] + " - " + j[3]] = {
                        "job_id": j[1],
                        "PI": j[2],
                        "run_name": j[3],
                        "elapsed": j[4],
                        "start": j[5],
                        "state": j[6],
                        "exit": j[7],
                        "submission_dir": j[8],
                        "level": color,
                        "pipeline_name": j[10]
                    }


        return jobs

    except NameError as e:
        print(e)

    print(jobs)

def create_app_dirs(app_dir):
    access_rights = 0o755

    if not os.path.exists(app_dir):
        try:
            os.makedirs(os.path.join(app_dir), access_rights)
        except OSError:
            print ("Failed to create the directory %s " % app_dir)
        else:
            print ("Successfully created the directory %s" % app_dir)


def create_user_dict(app_dir, app_user):

    users_path = os.path.join(app_dir,app_user)

    if not os.path.exists(users_path):
        with open(users_path, 'w') as f:
            user = "user name=user_name"
            f.write(user)

            print(f"File {users_path} as created")

    return 0


def get_user_dict(app_dir, app_user):

    user_dict = {}
    with open(os.path.join(app_dir,app_user), 'r') as f:

        for line in f:
            user = line.strip().split('=')
            user_dict[user[0]] = user[1]
    
    return user_dict


def add_new_user(app_dir, app_user, user_name):

    user = "_".join(user_name.lower().split())
  
    users_path = os.path.join(app_dir,app_user)
    new_user = user_name + "=" + user + "\n"

    with open(os.path.join(app_dir,app_user), 'a') as f:
        f.write(new_user)

