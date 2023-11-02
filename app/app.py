import base64
from io import BytesIO
from flask import Flask, render_template_string, request
import matplotlib.pyplot as plt
import numpy as np
from utilities import bpsk_demodulate, string_to_bits, bpsk_modulate

app = Flask(__name__)

# NOTE: IMPORTANT
"""
I decided to use chatgpt to make this webpage. I did this for a couple reasons.

1) This was extra on top of the assignment so I was not subtracting any value
    or the integruity of the assignment.
2) I'm in a deep learning course right now and it is timely relavent for me to
  become more fimilar with chatgpt for my final project I am working on in that 
  class. This lets me "kill two birds with one stone" by making something
  cool for this assignment and also become more fimilar with chatgpt for my
  final project. 
3) An extention of 2, from the course that I'm in, it has become clear that tools
  like chatgpt will eventually become a part of our lives as developers. The question
  is when, not if. And, how will we find a use for them. I think it is benificial to
  get a head start on learning how to use these tools.
"""


# HTML Template with embedded image
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>BPSK Modulator/Demodulator</title>
  </head>
  <body>
    <h2>BPSK Modulation and Demodulation</h2>
    <div style="display: flex;">
      <div style="flex: 50%;">
        <form method="post">
          <label for="inputText">Enter Text:</label><br>
          <textarea id="inputText" name="inputText" rows="4" cols="50">{{ input_text }}</textarea><br>
          <label for="noisePower">Noise Power:</label><br>
          <input type="text" id="noisePower" name="noisePower" size="20" value="{{ noise_power }}"><br>
          <input type="submit" value="Modulate">
        </form>
        <br>
        <label for="modulatedText">Modulated Text:</label><br>
        <textarea id="modulatedText" name="modulatedText" rows="4" cols="50">{{ modulated_text }}</textarea><br>
        <br>
        <label for="demodulatedText">Demodulated Text:</label><br>
        <textarea id="demodulatedText" name="demodulatedText" rows="4" cols="50">{{ demodulated_text }}</textarea>
      </div>
      <div style="flex: 50%; padding-left: 20px;">
        <img src="{{ plot_url }}" alt="Matplotlib Image">
      </div>
    </div>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['inputText']
        noise_power = 0 if request.form.get('noisePower', 0) == '' else float(request.form.get('noisePower', 0))
        noise_gen = False if noise_power == 0 else True
        input_bits = string_to_bits(input_text)
        modulated_text = bpsk_modulate(input_bits, noise_gen=noise_gen, noise_power=noise_power)
        plot_url = create_plot(modulated_text)
        demodulated_text = bpsk_demodulate(modulated_text).decode(encoding="ascii", errors="replace")
    return render_template_string(HTML_TEMPLATE, input_text=input_text, noise_power=noise_power, modulated_text=modulated_text, demodulated_text=demodulated_text,plot_url=plot_url)

# Generate a Matplotlib image and return it as a base64 encoded string
def create_plot(modulated_text):
    fig, ax = plt.subplots()
    ax.plot(np.real(modulated_text), np.imag(modulated_text), '.')
    ax.grid(True)
    ax.set_xlabel("I")
    ax.set_ylabel("Q")
    ax.set_ylim((-1.5, 1.5))
    ax.set_xlim((-1.5, 1.5))
    ax.set_title("BPSK modulated prompt Constellation")

    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    plt.close(fig)  # Close the figure after encoding
    return f"data:image/png;base64,{plot_url}"

if __name__ == '__main__':
    app.run(debug=True)
