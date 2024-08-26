import os

# Define the folder structure
folder_structure = {
    "stock_price_prediction": {
        "data": {
            "raw": {},
            "processed": {},
            "external": {}
        },
        "notebooks": {},
        "src": {
            "data": {
                "data_collection.py": "",
                "data_preprocessing.py": "",
                "feature_engineering.py": ""
            },
            "models": {
                "lstm_model.py": "",
                "train.py": "",
                "evaluate.py": ""
            },
            "utils": {
                "config.py": "",
                "helpers.py": ""
            },
            "webapp": {
                "app.py": "",
                "templates": {},
                "static": {},
                "routes.py": ""
            }
        },
        "tests": {
            "test_data.py": "",
            "test_models.py": "",
            "test_webapp.py": ""
        },
        "archive": {
            "old_models": {},
            "deprecated_scripts": {},
            "experimental": {}
        },
        "requirements.txt": "",
        "Dockerfile": "",
        "docker-compose.yml": "",
        ".env": "",
        "README.md": "",
        "setup.py": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

# Create the folder structure
base_path = r"C:\D\Coding\C++\Project Alpha\stock_price_prediction" # Change this if you want to create the structure in a different location
create_structure(base_path, folder_structure)
