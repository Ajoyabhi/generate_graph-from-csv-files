# app.py
from flask import Flask, render_template, request
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/process-code', methods=['POST'])
def process_code():
    code_file = request.files['codeFile']
    # Process the code file and generate graphs
    graph_data = generate_graphs(code_file)
    print(graph_data)

    return render_template('upload.html', graphData=graph_data)


def generate_graphs(code_file):
    inputData = pd.read_csv(code_file)

    # Generate Pairplot
    pairplot_path = 'static/pairplot.png'  # Path to save the pairplot image
    sns.pairplot(data=inputData, hue='Outcome')
    plt.xlabel('Mathematical Expression', fontsize=16)
    plt.savefig(pairplot_path)
    plt.close()

    # Generate Heatmap
    heatmap_path = 'static/heatmap.png'  # Path to save the heatmap image
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca()
    heatmap = sns.heatmap(inputData.corr(), annot=True, fmt=".2f", cbar=False, ax=ax, annot_kws={"fontsize": 18})
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45, ha='right', fontsize=18)
    plt.yticks(fontsize=18)
    plt.title("Correlation", fontsize=18)
    plt.savefig(heatmap_path)
    plt.close()

    histograms = []
    length = len(inputData.columns[:-1])
    colors = ["r", "g", "b", "m", "y", "c", "k", "orange"]

    plt.figure(figsize=(15, 10))

    for i, j, k in zip(inputData.columns[:-1], range(length), colors):
        plt.subplot(2, 4, j + 1)
        sns.histplot(inputData[i], color=k)
        plt.title(i)
        plt.axvline(inputData[i].mean(), color="k", linestyle="dashed", label="MEAN")
        plt.axvline(inputData[i].std(), color="b", linestyle="dotted", label="STANDARD DEVIATION")
        plt.legend(loc="upper right")
        plt.xlabel("Values", fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

    # Save the combined histogram image
    hist_path = 'static/histograms.png'  # Path to save the combined histogram image
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()

    # Append the path to the histograms list
    histograms.append(hist_path)

    # Generate Pie Chart
    piechart_path = 'static/piechart.png'  # Path to save the pie chart image
    outcome_counts = inputData['Outcome'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(outcome_counts, labels=outcome_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Outcome Distribution', fontsize=18)
    plt.savefig(piechart_path)
    plt.close()

    # Return the dictionary of graph image paths
    return {
        'Pairplot': pairplot_path,
        'Heatmap': heatmap_path,
        'Histograms': hist_path,
        'Piechart': piechart_path,
    }

if __name__ == '__main__':
    app.run(debug=True)