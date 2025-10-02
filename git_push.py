import subprocess

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

def git_push(commit_msg="Auto commit"):
    try:
        run_cmd("git add .")
        run_cmd(f'git commit -m "{commit_msg}"')
        run_cmd("git branch -M main")
        run_cmd("git push -u origin main")
        print("✅ Changes pushed to GitHub successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    msg = input("Enter commit message: ")
    git_push(msg if msg else "Auto commit")
