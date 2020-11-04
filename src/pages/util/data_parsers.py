
import os

def fake_data():
    """
    For test only
    """
    fake_jobs_data = [(1, "Single_cell","Silly_Mokey","29-10-2020T15:57",'Complete',"0","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"), 
                      (2,"Super SC","Envy_John","30-01-2020T15:57",'Pending',"0","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"),
                      (3,"Vib 10X","Careful_lizard","27-10-2020T15:57",'Running',"0","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"),
                      (4,"SC-Genomics","Donald_duck","30-01-2020T15:57",'Failed',"127","/home/dmorais/genap_next_tower/David_Morais/out/nextflow_reports/"),
    
    ]

    return fake_jobs_data



def get_db_stats():
    """
        This function fetches the jobs from the database and 
        :param:
        :return jobs: A dict of dict  job={ "pipeline_name - "run_name": { "pipeline_name": "Single_cell",
                                                                            "run_name": "Silly Mokey",
                                                                            "start": "29-10-2020T15:57",
                                                                            "state": 'Complete',
                                                                            "exit": "0"",
                                                                            "level": danger
                                                                            "submission_dir": "path"}, 
    """
    level = {
        'Complete' : 'success',
        'Pending': 'primary',
        'Running': 'warning',
        'Failed': 'danger'
    }
    
    jobs = {}

    ### TODO ################################
    # Change this for a call to select from db
    # Simulate a db call
    db_jobs = fake_data()

    for j in db_jobs:

        color = level[j[4]]

        jobs[j[1] + " - " + j[2]] = {
            "pipeline_name": j[1],
            "run_name": j[2],
            "start": j[3],
            "state": j[4],
            "exit": j[5],
            "level": color,
            "submission_dir": j[6]
        }

    return jobs


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

