## **AQ Data Format Processor**
* This script is to extract **daily** AQ monitoring data in CSV files into formatted **hourly** TXT files
#### **Input Data**
* Data Source [中国空气质量历史数据](https://quotsoft.net/air/)
* Currently Support: **Packaged Annual Data of Nationwide Sites** (china_sites_YYYYMMDD.csv)
#### **Output Format**
* Output path: **output/YYYYMM/**
* Output name: **obs.YYYYMMDDHH.txt**
* Columns:

>**City ID** | **Site ID** |
>**PM<sub>2.5</sub>** [ug m<sup>-3</sup>] |
>**PM<sub>10</sub>** [ug m<sup>-3</sup>] |
>**SO<sub>2</sub>** [ug m<sup>-3</sup>] |
>**CO** [ug m<sup>-3</sup>] |
>**NO<sub>2</sub>** [ug m<sup>-3</sup>] |
>**O<sub>3</sub>** [ug m<sup>-3</sup>] |
#### **Usage**
1. Extract daily files into **sites/**
2. Latest site info (站点列表-YYYY.MM.DD起.xlsx) into **sites/**
3. Run Python script **main_processor.py** as

    `python main_processor.py`
4. Define site info filename and more parameters in **user_conf.py**