
def fake_data():
    """
    For test only
    """
    fake_jobs_data = [(1, "Single_cell","Silly_Mokey","29-10-2020T15:57",'Complete',"0","/home/dmorais/projects/nextflow/vib-singlecell/out/nextflow_reports/"), 
                      (2,"Super SC","Envy_John","30-01-2020T15:57",'Pending',"0","/home/dmorais/projects/nextflow/vib-singlecell/out/nextflow_reports/"),
                      (3,"Vib 10X","Careful_lizard","27-10-2020T15:57",'Running',"0","/home/dmorais/projects/nextflow/vib-singlecell/out/nextflow_reports/"),
                      (4,"SC-Genomics","Donald_duck","30-01-2020T15:57",'Failed',"127","/home/dmorais/projects/nextflow/vib-singlecell/out/nextflow_reports/"),
    
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