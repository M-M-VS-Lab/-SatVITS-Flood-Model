# SatVITS-Flood-Model

## 1) Introduction
The SatVITS-Flood-Model (Satellite Vegetation Index Time Series Flood) is designed to identify past floods since 1980 in hyperarid regions (places with precipitation amounts < 100 mm year-1) around the world. The model detects changes in vegetation in the ephemeral rivers and thus identifies the occurrence of a flood and estimates its magnitude – the volume of the flood (Mm^3) and its duration (days). Here you will find two codes that operate in the Google Colab environment, the first "Satvits_Floods" is more detailed and organized in a way that is easier to understand while the second code "Satvits_Floods_short" is more concise and allows faster execution of the code and in a simpler way. These codes will allow you to select a point in an ephemeral river as you wish and download a table CSV file with the results of the model as detailed below.

When using the SatVITS-Flood model, please cite the article tghat describes the model:

Burstein Omer, Grodek T, Enzel Y, Helman David. (2023) SatVITS-Flood: Satellite Vegetation Index Time Series Flood detection model for hyperarid regions. Water Resources Research, 59, e2023WR035164.

A link to the open-access Article:
https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2023WR035164


## 2) Requirenments
The code is adapted to the Google Colab environment and requires an account in GEE (Google Earth Engine) in order to download the necessary data. A video explaining how to open an account in GEE can be found in the following link: https://www.youtube.com/watch?v=S0AzoP40cDI&t=8s

GEE website: https://earthengine.google.com/

## 3) The Code

### A) Initializing the GEE account

In order to initialize your GEE account, you need to run this cell of the code. Then click the link that will appear as you can see in fig 1. After following the instructions that appear and generating a token, you will receive a code that you need to put in the box that appears after the inscription: " Enter verification code:" and press enter (fig 1).

<img width="602" alt="image" src="https://user-images.githubusercontent.com/95708635/224546720-7338423a-db5d-4abb-8f85-4d86e2ebe7bb.png">

fig 1.

### B) Choosing your river

In order to activate the model you need to insert a coordinate,  there is 2 options how to do it. 
option 1: write your coordinates in the code where is writen "option 1"(fig 2)

<img width="310" alt="image" src="https://user-images.githubusercontent.com/95708635/224547312-95df9614-9ed3-4448-ba14-92e5a5d77ac2.png">

fig 2.

Option 2: Using the map.
First you can show only the precipitation layer in order to see the hyper-arid regions in yellow (fig 3.A). Than, you can see the STD (Standart Deviation) layer in order to see the rivers and choose pixel with high changes in vegetation - green pixels (fig 3.B). Than you can use the tool "draw a marker" in order to choose your coordinate (fig 3.B).

<img width="491" alt="image" src="https://user-images.githubusercontent.com/95708635/224548590-6c263755-56e9-4fa2-be01-964c8f2d3ce4.png">

fig 3

In both options you can insert your river_name in order to save the final CSV file on its name, and you can also change the month of the start of the hydrological year of your choosen river (fig 2). 

After inserting the coordinates of your ephemeral river in a hyper-arid region, you can just run the code and get the results of the model.

## 4) Output

The model will download to your computer a CSV file with the years when floods was detected and their magnitude (fig 4). Years that was detected but without values of volume and duration, means that the model cant evaluate their specific magnitude but can detect a flood.

<img width="452" alt="image" src="https://user-images.githubusercontent.com/95708635/224549415-cedc8abb-1436-4bc7-8b9d-96b3dd2cb246.png">

fig 4

## 5) Supplements

We add our raw codes that help us to develop the model. You can also use those codes in order to download data that eventually we didnt used in our model from the GEE links below, and analyze the data with the other codes in this repository.

Links to code in GEE to download time series:

MODIS: https://code.earthengine.google.com/3061df7bf284f085233d9a5172d25292

Landsat: https://code.earthengine.google.com/8577a70078a5c0d648274ebb551d2f26

AVHRR: https://code.earthengine.google.com/7aaa10e7a7f40fb8e97747fdbb2157fd
