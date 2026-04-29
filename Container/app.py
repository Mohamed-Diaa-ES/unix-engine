# ==============================================================================
# Application file name :  app.py
# Description:  Application file that runs all building and behind the scene
# Author:       MohammedDiaa (mohammeddiaato@gmail.com)
# Company:      Gestell - Professional Embedded Solutions
# ==============================================================================

from flask import Flask, request, send_file
import os
import subprocess
import zipfile
import shutil

app = Flask(__name__)
WORKSPACE = "/workspace"

@app.route('/run', methods=['POST'])
def run_project():
    # 1. Capture Project Name from PowerShell
    project_name = request.form.get('project_name', 'app')
    final_binary_name = f"{project_name}.out"
    
    if 'file' not in request.files:
        return "Error: No file uploaded", 400

    if os.path.exists(WORKSPACE):
        shutil.rmtree(WORKSPACE)
    os.makedirs(WORKSPACE)

    zip_path = os.path.join(WORKSPACE, "project.zip")
    request.files['file'].save(zip_path)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(WORKSPACE)
        
        # Build Detection Logic
        makefile_path = os.path.join(WORKSPACE, "Makefile")
        if not os.path.exists(makefile_path):
            makefile_path = os.path.join(WORKSPACE, "makefile")

        if os.path.exists(makefile_path):
            build_process = subprocess.run(["make"], cwd=WORKSPACE, capture_output=True, text=True)
            build_cmd = "make"
        else:
            source_files = {}
            for root, dirs, files in os.walk(WORKSPACE):
                for file in files:
                    if file.endswith(".c"):
                        source_files[file] = os.path.join(root, file)
            all_sources = " ".join(source_files.values())
            # Temporary name during build
            build_cmd = f"gcc -I{WORKSPACE} {all_sources} -o {os.path.join(WORKSPACE, 'temp_build.out')}"
            build_process = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)

        if build_process.returncode != 0:
            return f"BUILD FAILED:\n{build_process.stderr}", 400

        # --- NEW: Cleanup and Renaming Logic ---
        # 1. Find the resulting binary (either temp_build.out or Makefile output)
        origin_binary = os.path.join(WORKSPACE, "temp_build.out")
        if not os.path.exists(origin_binary):
            # If Makefile was used, find any executable
            for f in os.listdir(WORKSPACE):
                f_path = os.path.join(WORKSPACE, f)
                if os.access(f_path, os.X_OK) and not os.path.isdir(f_path) and f != "project.zip":
                    origin_binary = f_path
                    break

        # 2. Move binary to a temporary safe spot outside workspace
        temp_safe_path = os.path.join("/tmp", final_binary_name)
        shutil.move(origin_binary, temp_safe_path)

        # 3. Wipe the workspace clean
        shutil.rmtree(WORKSPACE)
        os.makedirs(WORKSPACE)

        # 4. Move the renamed binary back into the clean workspace
        final_workspace_path = os.path.join(WORKSPACE, final_binary_name)
        shutil.move(temp_safe_path, final_workspace_path)

        return send_file(
            final_workspace_path, 
            mimetype='application/octet-stream',
            as_attachment=True, 
            download_name=final_binary_name
        )

    except Exception as e:
        return f"System Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# ==============================================================================
# Application file name :  app.py
# Description:  Application file that runs all building and behind the scene
# Author:       MohammedDiaa (mohammeddiaato@gmail.com)
# Company:      Gestell - Professional Embedded Solutions
# ==============================================================================
