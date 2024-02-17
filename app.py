import io
import yaml
import json
import os
from flask import Flask, Response, request, send_file, jsonify
from flask_cors import CORS
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
CORS(app)

DATA_DIR = 'data'

@app.route('/plot/<folder_name>.png')
def plot_png(folder_name):
    # Ensure the print statement outputs to your console
    print(f"Generating plot for folder: {folder_name}")
    fig = create_figure(folder_name)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    output.seek(0)
    return send_file(output, mimetype='image/png', as_attachment=False)


@app.route('/submit_prompt', methods=['POST'])
def submit_prompt():
    data = request.json
    search_folder = data.get('prompt', '').strip()
    folder_path = os.path.join(DATA_DIR, search_folder)
    print(f"Searching for folder: {folder_path}")
    if os.path.isdir(folder_path):
        return jsonify({"message": "Match found", "folderName": search_folder})
    else:
        return jsonify({"message": "No match found", "folderName": ""})


def create_figure(folder_name):
    # Paths to the files
    task_graph_path = os.path.join(DATA_DIR, folder_name, "save/it10000-export/task_graph.json")
    lego_lib_path = "standard_lego_library.yaml"

    # Load the data
    with open(task_graph_path, 'r') as file:
        assembly_list = json.load(file)
    with open(lego_lib_path, 'r') as file:
        lego_lib = yaml.safe_load(file)

    print(assembly_list)
    print("PRESENT")

    # Create the figure and plot
    fig = Figure()
    ax = fig.add_subplot(111, projection='3d')

    for piece_id, piece in assembly_list.items():
        x, y, z = piece['x'], piece['y'], piece['z']
        height = lego_lib[piece_id]['height']
        width = lego_lib[piece_id]['width']
        depth = 1  # Sudo value
        color = lego_lib[piece_id]['color']
        orientation = piece['ori']

        if orientation == 0:
            width, height = height, width

        # Adjust color if needed
        if color == "cream": color = "beige"

        # Plot the block
        ax.bar3d(x, y, z, width, height, depth, color, alpha=0.8)

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(folder_name.title())

    # Adjust viewing angle
    ax.view_init(elev=60, azim=90)

    # Set aspect ratio
    ax.set_box_aspect([1, 1, 1])

    return fig

if __name__ == '__main__':
    app.run(debug=True)