#webapp libraries
import cv2
import torch 

import numpy as np
import streamlit as st  #for webapp
from streamlit_drawable_canvas import st_canvas

from models import *
import plotly.graph_objects as go

st.title("The Amazing Digit Recognizer")

column1, column2 = st.columns([1,1,])

with column1:
    st.write('')
    st.write('')
    st.write('')
    mode = st.checkbox("Draw or transform") #Freedraw is better
    canvas_result = st_canvas(
        fill_color = '#000000',
        stroke_width = 20,
        stroke_color = '#FFFFFF',
        background_color = '#000000',
        width = 256,
        height = 256,
        drawing_mode = "freedraw" if mode else "transform",
        key = 'canvas'

    )

    predict_button = st.button("Predict my number")

if canvas_result.image_data is not None:
    img = cv2.resize(canvas_result.image_data.astype('uint8'), (28,28))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #we need to add the channel!
    img = img[:,:,np.newaxis] / 255.0

model = DigitModel()
model.load_state_dict(torch.load('best_weights.pt'))


with column2:
    if predict_button:
        with torch.no_grad():
            img = torch.Tensor(img).permute(2,0,1) #changing convention
            logits = model(img.unsqueeze(0)) #need to add another batch dimension
            sm = torch.nn.Softmax(dim=1)
            probs = sm(logits)[0]

            fig = go.Figure(
                data = [
                    go.Bar(
                        x = np.arange(0,10),
                        y = (probs*100).numpy()
                    )
                ]
            )

            fig.update_layout(
                width=500,
                height= 500
            )

            st.plotly_chart(fig)