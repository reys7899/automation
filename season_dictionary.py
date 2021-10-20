import os 
import subprocess as sp
# --------------------------------------------------
def season_dictionary():
    
    season_dict = {
        '10': {
            'scanner3DTop': {
                'containers': {
                    'gantry_notifications': {
                        'simg': 'gantry_notifications.simg', 
                        'dockerhub_path': 'docker://phytooracle/slack_notifications:latest'
                    },
                    'preprocessing': {
                        'simg': '3d_preprocessing.simg', 
                        'dockerhub_path': 'docker://phytooracle/3d_preprocessing:latest'
                    },
                    'sequential_alignment': {
                        'simg': '3d_sequential_align.simg',
                        'dockerhub_path': 'docker://phytooracle/3d_sequential_align:latest'
                    }
                },
                'workflow_1': {
                    'jx2json main_workflow_phase1.jx -a bundle_list.json > main_workflow_phase1.json', 
                    'makeflow -T wq --json main_workflow_phase1.json -a -N phytooracle_3d -M phytooracle_3d -r 3 -p 0 -dall -o dall.log $@'
                },
                'workflow_2': {
                    'jx2json main_workflow_phase-2.jx -a bundle_list.json > main_workflow_phase2.json', 
                    'makeflow -T wq --json main_workflow_phase2.json -a -r 2 -M phytooracle_3d -N phytooracle_3d -p 60221 -dall -o dall.log --disable-cache $@'
                }
            }
        }
    }

    return season_dict


# --------------------------------------------------
def build_containers(season, sensor, season_dict):

    for k, v in season_dict[season][sensor]['containers'].items():
        if not os.path.isfile(v["simg"]):
            print(f'Building {v["simg"]}.')
            sp.call(f'singularity build {v["simg"]} {v["dockerhub_path"]}', shell=True)

    