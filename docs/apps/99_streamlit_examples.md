# 99. Code samples for Streamlit

This app includes code samples for Streamlit. You can run the app and select the sample you want to run from the sidebar.

## Prerequisites

- Python 3.10 or later
- Azure OpenAI Service

## Usage

1. Get Azure OpenAI Service API key
1. Get Azure AI Search API key
1. Copy [.env.template](../../.env.template) to `.env` in the same directory
1. Set credentials in `.env`
1. Run [main.py](./main.py)

```shell
# Create a virtual environment
$ python -m venv .venv

# Activate the virtual environment
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt

# Run the script
$ python -m streamlit run apps/99_streamlit_examples/main.py
```

### Example

Access to http://localhost:8501 and select the sample you want to run from the sidebar.

#### 1. File Q&A

![File Q&A](../images/99_streamlit_examples.fileqa.png)

#### 2. Image Q&A

![Image Q&A](../images/99_streamlit_examples.imageqa.png)

#### 3. Camera Q&A

![Camera Q&A](../images/99_streamlit_examples.cameraqa.png)

#### 4. Translate text

![Translate text](../images/99_streamlit_examples.translate.png)

#### 5. Explain data

![Explain data](../images/99_streamlit_examples.explaindata.png)

#### 6. Speech to Text

![Speech to Text](../images/99_streamlit_examples.stt.png)

#### 7. Text to Speech

![Text to Speech](../images/99_streamlit_examples.tts.png)

#### 8. Create image

![Create image](../images/99_streamlit_examples.createimage.png)

#### 9. Visualize location

![Visualize location](../images/99_streamlit_examples.map.png)

#### 10. Object detection

![Object detection](../images/99_streamlit_examples.objectdetection.png)

#### 11. Pose estimation

![Pose estimation](../images/99_streamlit_examples.poseestimation.png)

#### 12. Video processing

![Video processing](../images/99_streamlit_examples.videoprocessing.png)

ref. [data-videos/traffic.mp4](https://github.com/OlafenwaMoses/ImageAI/blob/master/data-videos/traffic.mp4)

## References

- [🎈 Streamlit + LLM Examples App](https://github.com/streamlit/llm-examples)
- [Streamlit > st.plotly_chart](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)
- [Plotly > Time Series and Date Axes in Python](https://plotly.com/python/time-series/)
