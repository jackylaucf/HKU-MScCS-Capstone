## MSc(CompSc) Capstone Project (Year 2024)

---

**Topic**: 

Trend and Pattern Recognition of Stock Price Charts by CNN-based Model in Asia Equity Markets

**Mentor**: 

Dr. JingRui Zhang

**Students**: 

- LAM TSZ YIN (3036034887) (tylamac@connect.hku.hk)
- LAU CHI FUNG (3036035398) (jackylcf@connect.hku.hk)
- LAW VANESSA (3035051773) (u3505177@connect.hku.hk)

---

This is a Github repository for recording and demonstrating our project team's research work and the major deliverables.

**Folder structure**

| Folder    | Purpose                                                       |
|-----------|---------------------------------------------------------------|
| dataset   | - Commonly shared resources for data analysis, model training & portfolio construction <br> - There are three main subfolder: market_data, ohlc_graphs and returns <br> - market_data stores the stock and index prices data that are crawled from various sources <br> - ohlc_graphs stores the OHLC graphs generated for the CNN model training <br> - returns stores the calculated stock return over different time horizon in form of python pickle files <br> - Due to the large number and size of image data, only market_data and returns folders are pushed to Github. <br> - For data in ohlc_graphs, you will need to execute the code in https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/notebook/ohlc_ma_demo.ipynb
| src       | - Python source codes                 |
| training  | - The space for training the CNN model <br> - It contains the labelled OHLC images before 2014-04-01, the training checkpoint files and log files <br> Due to large amount of data, the files are not pushed to the Github |
| portfolio | - It contains the OHLC images since 2014-04-01 for portfolio construction <br> - The portfolio output files will be stored here <br> Due to large amount of data, the files are not pushed to the Github |

---


**Guideline for reproducing the results**

*(A) Crawler*

To run the data crawler, you will need to execute https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/data_crawler_main.py. 

The enviornment setup can be found in another README.md file (https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/README.md)

*(B) Data preparation & cleansing*

1. ohlc_ma_demo.ipynb: Generate the OHLC graphs, which will be stored under dataset/ohlc_graphs folder
2. market_data_analysis: Generate the stock returns and store under dataset/returns folder in form of python pickle files. It also calculates the distribution of each stock's return

*(C) Model Training*

1. training_space.ipynb: Split the image data into model training, model testing, as well as the portfolio backtesting set. Data will also be splitted based on its class label. The output will be stored in the training folder at the project root.
2. cnn_model.ipynb: Define and train the CNN model. Model evaluation by the test set will also be done in this notebook

*(D) Portfolio construction & backtesting*

---

**Notice**
1. For any data to be input to or output by your code. Please try to store them in dataset folder instead of storing 
them along with the source code. This can help us view the data and prepare our final reports without having our data 
scattering around
2. For the code modules, it is encouraged to (i) show the required steps about how to replicate your results; 
(ii) any implementation details that worth readers' notice.
3. To better manage this repository and avoid the headache of managing commit conflicts, it is advised to create and 
work on your own `feature` branch when you know someone else is also working on the same module. Branch protection
is available to the paid users only on Github.
3. Please keep the commit tree clean - preferably always rebase to the head of `main` before you push your `feature` 
branch
