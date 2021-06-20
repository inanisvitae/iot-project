from re import split
from bokeh.plotting import figure, show, save


# Example
# prepare some data
for filename in ['barometer_data.txt', 'fahrenheit_data.txt', 'humidity_data.txt']:
  file1 = open(filename, 'r')
  lines = file1.readlines()
  y = []
  for line in lines:
    y.append(float(line.strip()))
  x = range(1, len(lines)+1)


  # create a new plot with a title and axis labels
  p = figure(title=filename, x_axis_label="x", y_axis_label="y")

  # add a line renderer with legend and line thickness
  p.line(x, y, legend_label="Unit", line_width=2)

  # show the results
  save(p, filename=filename + '.html')
