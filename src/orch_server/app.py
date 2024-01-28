import os
import subprocess
import time
import datetime

# les details des serveurs distants
servers = [
    {"host": "173.199.70.34", "user": "root", "base_dir": "/root/logs/tensorboard_logs"},
    {"host": "45.77.62.249", "user": "root", "base_dir": "/root/logs/tensorboard_logs"},
]

# le dossier local ou les logs seront synchronises
local_base_dir = "/home/user/logs"  
ssh_key_path = "/home/user/.ssh/pub_key"

# recupere la liste des experiences sur un serveur distant
def get_remote_experiments(server_info):
    
    remote_host = server_info["host"] # recupere l'ip du serveur'
    remote_user = server_info["user"] # recupere l'utilisateur utilisé sur le serveur'
    remote_base_dir = server_info["base_dir"] # recupere le dossier ou sont stockés les logs sur le serveur'
    
    # commande ssh pour recuperer la liste des dossiers d'experiences
    ssh_command = f"ssh -o StrictHostKeyChecking=no -i {ssh_key_path} {remote_user}@{remote_host} 'ls -d {remote_base_dir}/*/'"
    # execute la commande ssh et recupere le resultat
    result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    # recupere la liste des dossiers d'experiences
    experiment_dirs = result.stdout.strip().split('\n')
    # recupere le nom des experiences
    experiment_names = [os.path.basename(os.path.normpath(dir_path)) for dir_path in experiment_dirs if dir_path.strip()]
    return experiment_names
last_modified = {}

# recupere la date de la derniere modification d'une experience sur un serveur distant
def get_last_modified_date(server_info, experiment_name):
    remote_host = server_info["host"]
    remote_user = server_info["user"]
    remote_experiment_dir = os.path.join(server_info["base_dir"], experiment_name)

    ssh_command = f"ssh -o StrictHostKeyChecking=no -i {ssh_key_path} {remote_user}@{remote_host} 'stat -c %Y {remote_experiment_dir}'"
    result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    return datetime.fromtimestamp(int(result.stdout.strip()))

# synchronise les logs d'une experience depuis un serveur distant
def sync_logs(server_info, experiment_name):
    remote_host = server_info["host"]
    remote_user = server_info["user"]

    # recupere le chemin du dossier d'experiences sur le serveur distant
    remote_experiment_dir = os.path.join(server_info["base_dir"], experiment_name)
    # recupere le chemin du dossier d'experiences sur le serveur local
    local_experiment_dir = os.path.join(local_base_dir, remote_host, experiment_name)
    
    # cree le dossier d'experiences sur le serveur local
    os.makedirs(local_experiment_dir, exist_ok=True)

    # commande scp pour synchroniser les logs
    scp_command = f"scp -o StrictHostKeyChecking=no -i {ssh_key_path} -r {remote_user}@{remote_host}:{remote_experiment_dir}/. {local_experiment_dir}/"
    subprocess.run(scp_command, shell=True)
    print(f"Synced logs from {remote_experiment_dir} to {local_experiment_dir}.")


# defini la boucle principale (itere sur les serveurs distants et les experiences)
def main():
    # intervalle de verification des logs
    check_interval = 60
    
    while True:
        # itere sur les serveurs distants
        for server in servers:
            # recupere la liste des experiences sur le serveur distant
            current_experiments = get_remote_experiments(server)
            for experiment_name in current_experiments:
                key = (server["host"], experiment_name)
                last_modified_date = get_last_modified_date(server, experiment_name)

                if key not in last_modified or last_modified[key] < last_modified_date:
                    sync_logs(server, experiment_name)
                    last_modified[key] = last_modified_date

        time.sleep(check_interval)

if __name__ == "__main__":
    main()