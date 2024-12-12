import os
from git import Repo

repo_path = "git_repo/ethical_hacking_python"  
file_name = "data.txt"  
data_to_add = "Nieuwe gegevensregel\n"  
commit_message = "Voeg nieuwe gegevens toe"

def update_and_push(repo_path, file_name, data_to_add, commit_message):
    file_path = os.path.join(repo_path, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("")

    with open(file_path, "a") as f:
        f.write(data_to_add)

    repo = Repo(repo_path)
    repo.git.add(file_name)
    repo.index.commit(commit_message)
    origin = repo.remote(name="origin")
    origin.push()

update_and_push(repo_path, file_name, data_to_add, commit_message)
