from flask import Flask, render_template, send_from_directory
import math
import pygal
from pygal.style import DefaultStyle
import os

app = Flask(__name__)

@app.route('/')

def index():
    a = 2.5 # [m^2] powierzchnia
    b = 0.035 #[m^(5/2) / s] współczynnik
    tp = 0.1 #[s] interwał testowania
    ts = 3600 #[s]    czas symulacji
    n = int(ts / tp) + 1 #liczba iteracji
    q_d = [0.00] #natężenie dopływu  [m^3 / s]
    h = [0] #poziom wody [m]
    t = [0] #[s] czas
    q_o = [b*math.sqrt(h[-1])] #odpływ [m^3 /s]
    hMin, hMax = 0,5 #wysokość min max
    hInput = 3
    qDMax, qDMin = 0.05,0
    uMax, uMin = 10,0
    u =[0]
    kp=0.02
    e = []
    ti = 4
    result = 0

    #funkcja licząca h
    for i in range(n):
        e.append(hInput - h[-1])
        result += e[-1]

        uCurrent = (e[-1] + tp/ti*result)
        u.append(uCurrent)
        # print(f'Current h= {h[-1]}')
        qDCurrent = (qDMax-qDMin)/(uMax-uMin)*u[-1]
        q_d.append(qDCurrent)

        t.append(t[-1]+tp)
        x = min(hMax, max(hMin, (tp*(q_d[-1]-q_o[-1]))/a +h[-1]))
        h.append(x)
        q_o.append(b*math.sqrt(h[-1]))
    

    # Plotting with Pygal
    h.pop()
    line_chart = pygal.Line(
        width=800,   # Set the width of the first chart
        height=400,  # Set the height of the first chart
        style=DefaultStyle,
    )
    line_chart.title = 'Poziom wody'

    # Set custom labels every 50 iterations
    # x_labels = [int(t_val) for t_val in t]  # Use time as x-axis labels
    # line_chart.x_labels = x_labels
    line_chart.add('Poziom wody', h)
    
    # Save the first chart to a file in the 'static' directory
    chart_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'simulation_plot.svg')
    line_chart.render_to_file(chart_filename)

    # Creating a second chart for the ratio hInput / h
    ratio_chart = pygal.Line(
        width=800,   # Set the width of the first chart
        height=400,  # Set the height of the first chart
        style=DefaultStyle,
    )
    ratio_chart.title = 'Wysokość obliczona / Wysokość wprowadzona'
    ratio_chart.add('Wysokość obliczona', h)
    ratio_chart.add('Wysokość wprowadzona', [hInput]*n)
    # line_chart.add('H Input', hInput)


    # Save the second chart to a file in the 'static' directory
    ratio_chart_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'ratio_plot.svg')
    ratio_chart.render_to_file(ratio_chart_filename)

    
    # Creating a third chart for the input flow (q_d)
    input_flow_chart = pygal.Line(
        width=800,   # Set the width of the third chart
        height=400,  # Set the height of the third chart
        style=DefaultStyle,
    )
    input_flow_chart.title = 'Natężenie przypływu/ Natężenie odpływu'


    # Add the input flow data to the chart
    input_flow_chart.add('Natężenie przypływu', q_d)
    input_flow_chart.add('Natężenie odpływu', q_o)

    # Save the third chart to a file in the 'static' directory
    input_flow_chart_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'input_flow_plot.svg')
    input_flow_chart.render_to_file(input_flow_chart_filename)

    u_chart = pygal.Line(
        width=800,   # Set the width of the fourth chart
        height=400,  # Set the height of the fourth chart
        style=DefaultStyle,
    )
    u_chart.title = 'U(n)'

    # Add the variable u data to the chart
    u_chart.add('U(n)', u)

    # Save the fourth chart to a file in the 'static' directory
    u_chart_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'u_plot.svg')
    u_chart.render_to_file(u_chart_filename)


    return render_template('index_pygal.html', chart_filename=chart_filename, ratio_chart_filename=ratio_chart_filename, input_flow_chart_filename=input_flow_chart_filename, u_chart_filename = u_chart_filename)


@app.route('/download')
def download():
    # Provide a link to download the first chart file
    return send_from_directory('static', 'simulation_plot.svg', as_attachment=True)

@app.route('/download_ratio')
def download_ratio():
    # Provide a link to download the second chart file
    return send_from_directory('static', 'ratio_plot.svg', as_attachment=True)

@app.route('/download_input_flow')
def download_input_flow():
    # Provide a link to download the third chart file (input flow)
    return send_from_directory('static', 'input_flow_plot.svg', as_attachment=True)

@app.route('/download_u')
def download_u():
    # Provide a link to download the fourth chart file (u chart)
    return send_from_directory('static', 'u_plot.svg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)