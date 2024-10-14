# HigherGroundHW
Some homework problems for an interview with Higher Ground LLC

This started as a mini homework assignment but turned into a cool mini-project. I did some  BPSK modulation and demodulation and plotted its IQ constellation. I threw this all into a flask app to visualize it. I added the abilty to put AWGN onto the modulated data to make it a little less boring and not a perfect bpsk IQ. You can asjust the power of the noise on the web page too. I experimented with using chatgpt to generate the flask app for me. I did this for a couple reasons. First, this was an extra feature on top of the assignment so I did not subtract from its purpose or integruity. Second, I'm taking a course on deep learning right now, and it's timely relavent for me to use chatgpt and get a better feel for how to feed it good prompts. I'm also trying to gain some intuition for its behavior. My final project in that class is using the chatgpt api to make a calendar planning / scheduling assistant. So, this allowed me to both play with chatgpt more and also add a cool feature to this project. Lastly, I though this all in docker, both to answer part of the homework for higher ground and because it was quick and easy. I've worked with docker a lot the past couple summers at my jobs, and at home in my homelab.

# Repo Files
```
app  
    app.py  (Flask web app with the HTML page embedded in it. Renders the website)  
    utilities.py  (DSP functions which are called by the flask app to modulate, demodulate, and plot)  
README.md  
Dockerfile  
requirements.txt  
.gitignore  
```


# usage
## ENV
Setup a python environment to keep your local environment clean.
1) `virtualenv ./env`
2) `source ./env/bin/activate`
3) `pip install -r requirements.txt`

## build docker
1) `docker build --tag bpsk .`
2) check the image exist with `docker iamages`
   
## run docker
1) `docker run -p 5000:5000 bpsk`

# Useful resources
I knew the background of a lot of this before doing this project but I had not written any code to handle of this before. Even still, I found the docs for pysdy to be super well written and easy to follow. Definitly worth a read!

1) [pysdr modulation](https://pysdr.org/content/digital_modulation.html )
2) [pysdr IQ sampling](https://pysdr.org/content/sampling.html)
3) [pysdr pulse shaping](https://pysdr.org/content/pulse_shaping.html) not as related but also good read
4) [pysdr link budget](https://pysdr.org/content/link_budgets.html) related to the paper in the attached pdf

# example
![Example](example_use.png)
