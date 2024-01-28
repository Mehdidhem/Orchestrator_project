import os
import subprocess
import time
import concurrent.futures
import logging
from logging.handlers import RotatingFileHandler


# Configuration initiale du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('orchestrator.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


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

""" def sync_logs(server_info, experiment_name):
    # ... (le reste de votre code) ...
    try:
        subprocess.run(scp_command, shell=True, check=True)
        logger.info(f"Synced logs from {remote_experiment_dir} to {local_experiment_dir}.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error retrieving logs from server {remote_host}: {e}")
 """

        
def main():
    check_interval = 60  # Temps en secondes entre les vérifications
    
    while True:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for server in servers:
                current_experiments = get_remote_experiments(server)
                for experiment_name in current_experiments:
                    # Planification de la tâche de récupération des logs dans un processus séparé
                    futures.append(executor.submit(sync_logs, server, experiment_name))
            
            # Attente de la fin de toutes les tâches de récupération
            for future in concurrent.futures.as_completed(futures):
                try:
                    # Vous pouvez gérer les résultats ou les exceptions ici
                    future.result()
                except Exception as e:
                    print(f"An error occurred: {e}")
        
        time.sleep(check_interval)

if __name__ == "__main__":
    main()