from flask import Flask, render_template
import os

# Specify the exact paths
base_dir = r"C:\D\Coding\C++\Project Alpha\stock_price_prediction"
template_dir = os.path.join(base_dir, 'src', 'webapp', 'templates')
static_dir = os.path.join(base_dir, 'src', 'webapp', 'static')

print(f"Template directory: {template_dir}")
print(f"Static directory: {static_dir}")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error rendering home page: {str(e)}", 500

@app.route('/predict')
def predict():
    try:
        return render_template('predict.html')
    except Exception as e:
        return f"Error rendering predict page: {str(e)}", 500

@app.route('/analysis')
def analysis():
    try:
        return render_template('analysis.html')
    except Exception as e:
        return f"Error rendering analysis page: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
