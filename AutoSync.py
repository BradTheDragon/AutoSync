import os
import tkinter as tk
import git
import json

def sync_to_github():
    local_folder = local_folder_entry.get()
    github_authorization = authorization_entry.get()
    github_repo_owner = repo_owner_entry.get()
    github_repo_name = repo_name_entry.get()
    github_name = github_repo_name
    repo_public_state = public_state.get()
    repo_pull_state = pull_state.get()
    repo_push_state = push_state.get()
    repo_checkout_state = checkout_state.get()
    repo_new_branch_state = new_branch_state.get()
    commit_message = message_entry.get()
    branch_name = branch_name_entry.get()
    repo_commit_id = commit_id.get()
    
    memory_path = os.getcwd()
    
    os.chdir(local_folder)

    if not repo_public_state:
        github_repo_name = f"https://{github_repo_owner}:{github_authorization}@github.com/{github_repo_owner}/{github_repo_name}.git"
    else:
        github_repo_name = f"https://github.com/{github_repo_owner}/{github_repo_name}.git"
    
    try:
        repo = git.Repo.clone_from(github_repo_name, local_folder)
    except git.GitCommandError:
        repo = git.Repo(local_folder)
    
    if repo_new_branch_state == 1: 
        repo.git.checkout(repo_commit_id)
        commit = repo.head.commit
        new_branch_name = branch_name
        new_branch = repo.create_head(new_branch_name, commit)
        repo.head.reference = new_branch
        repo.head.reset(index=True, working_tree=True)
    elif repo_checkout_state == 1:
        branch = repo.heads[branch_name]
        branch.checkout()
        repo.head.reset(index=True, working_tree=True)
    
    if repo_pull_state == 1:
        repo.remotes.origin.pull()
    
    if repo_push_state == 1:
        repo.git.add(all=True)
        repo.index.commit(commit_message)
        repo.remotes.origin.push(refspec=f'refs/heads/{branch_name}:refs/heads/{branch_name}')    
    os.chdir(memory_path)
    
    memory = {"authorization": github_authorization, "folder": local_folder, "name": github_name, "id": repo_commit_id, "owner": github_repo_owner}

    with open("memory.json", "w") as file:
        json.dump(memory, file, indent=4)


try:
    with open("memory.json", "r") as file:
        memory = json.load(file)
        authorization_memory = memory.get("authorization", "")
        folder_memory = memory.get("folder", "")
        name_memory = memory.get("name", "")
        id_memory = memory.get("id", "")
        owner_memory = memory.get("owner", "")
except FileNotFoundError:
    authorization_memory = ""
    folder_memory = ""
    name_memory = ""
    id_memory = ""
    owner_memory = ""

# Create the main application window
app = tk.Tk()
app.title("GitHub Sync App")

# Create and arrange GUI elements
tk.Label(app, text="Local Folder Path:").pack()
local_folder_entry = tk.Entry(app)
local_folder_entry.insert(0, folder_memory)
local_folder_entry.pack()

tk.Label(app, text="Authorization:").pack()
authorization_entry = tk.Entry(app)
authorization_entry.insert(0, authorization_memory)
authorization_entry.pack()

tk.Label(app, text="GitHup Repo Owner:").pack()
repo_owner_entry = tk.Entry(app)
repo_owner_entry.insert(0, owner_memory)
repo_owner_entry.pack()

tk.Label(app, text="GitHub Repo Name:").pack()
repo_name_entry = tk.Entry(app)
repo_name_entry.insert(0, name_memory)
repo_name_entry.pack()

tk.Label(app, text="Commit Message:").pack()
message_entry = tk.Entry(app)
message_entry.insert(0, "Auto Sync")
message_entry.pack()

tk.Label(app, text="Branch Name:").pack()
branch_name_entry = tk.Entry(app)
branch_name_entry.insert(0, "main")
branch_name_entry.pack()

tk.Label(app, text="New Branch Commit ID:").pack()
commit_id = tk.Entry(app)
commit_id.insert(0, id_memory)
commit_id.pack()

public_state = tk.IntVar()
publicCheckbox = tk.Checkbutton(app, text="Public Repo", variable=public_state)
publicCheckbox.pack()

pull_state = tk.IntVar()
pullCheckbox = tk.Checkbutton(app, text="Pull Repo", variable=pull_state)
pullCheckbox.pack()

push_state = tk.IntVar()
pushCheckbox = tk.Checkbutton(app, text="Push Repo", variable=push_state)
pushCheckbox.pack()

checkout_state = tk.IntVar()
checkoutCheckbox = tk.Checkbutton(app, text="Checkout Branch", variable=checkout_state)
checkoutCheckbox.pack()

new_branch_state = tk.IntVar()
new_branchCheckbox = tk.Checkbutton(app, text="Create New Branch", variable=new_branch_state)
new_branchCheckbox.pack()

sync_button = tk.Button(app, text="Sync to GitHub", command=sync_to_github)
sync_button.pack()

print(os.getcwd())

# Start the application
app.mainloop()