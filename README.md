# SatVITS-Flood Model

## 1) Introduction
The SatVITS-Flood-Model (Satellite Vegetation Index Time Series Flood) is designed to identify past floods since 1980 in hyperarid regions (places with precipitation amounts < 100 mm year<sup>-1</sup>) around the world. The model detects changes in vegetation in the ephemeral rivers and thus identifies the occurrence of a flood and estimates its magnitude – the volume of the flood (M m<sup>3</sup>) and its duration (days). Here you will find two codes that operate in the Google Colab environment, the first "Satvits_Floods" is more detailed and organized in a way that is easier to understand while the second code "Satvits_Floods_short" is more concise and allows faster execution of the code and in a simpler way. These codes will allow you to select a point in an ephemeral river as you wish and download a table CSV file with the results of the model as detailed below.

When using the SatVITS-Flood model, please cite the article tghat describes the model:

Burstein Omer, Grodek T, Enzel Y, Helman David. (2023) **SatVITS-Flood: Satellite Vegetation Index Time Series Flood detection model for hyperarid regions.** *Water Resources Research*, 59, e2023WR035164.

A link to the open-access Article:
https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2023WR035164


## 2) Requirenments
The code is adapted to the Google Colab environment and requires an account in GEE (Google Earth Engine) in order to download the necessary data. A video explaining how to open an account in GEE can be found in the following link: https://www.youtube.com/watch?v=S0AzoP40cDI&t=8s

GEE website: https://earthengine.google.com/

## 3) The Code

### A) Initializing the GEE account

In order to initialize your GEE account, you need to run this cell of the code. Click the link that appears on your screen (Fig 1). After following the instructions and generating a token, you will receive a verification code. Copy and paste the code to the box that reads: " Enter verification code:" and then press Enter (Fig 1).

<img width="602" alt="image" src="https://user-images.githubusercontent.com/95708635/224546720-7338423a-db5d-4abb-8f85-4d86e2ebe7bb.png">

Fig 1.

### B) Choosing the river of interest

To run SatVITS-Flood, you need to insert the coordinates of the pixel that represents the river of interest. There are two options for that: 
**option 1:** If you know the coordinates, insert them directly where it says "option 1" (Fig 2)

<img width="310" alt="image" src="https://user-images.githubusercontent.com/95708635/224547312-95df9614-9ed3-4448-ba14-92e5a5d77ac2.png">

Fig 2.

**Option 2:** Using the map.
If you are not sure of the coordinates, you can first display the precipitation layer to see the hyper-arid regions (yellow regions in Fig 3.A). The NDVI STD (Standart Deviation) around your river can be also displayed. This NDVI STD layer can help you select the pixel of interest (near the river). Notice that greener pixels mean high changes in vegetation, which might be an indication of flood effect (Fig 3.B; see further explanation in Burstein et al., 2023 article: https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2023WR035164). Once you decided which is the pixel that represents your river, use the "draw a marker" option to get its coordinates (Fig 3.B).

<img width="491" alt="image" src="https://user-images.githubusercontent.com/95708635/224548590-6c263755-56e9-4fa2-be01-964c8f2d3ce4.png">

Fig 3

In both options, you can add your river_name to save the name on your output CSV file. You can also change the month of the start of the hydrological year (Fig 2). 

After inserting the coordinates of the hyper-arid river, run the code and get the flood detection year, as well as the flood magnitude (volume and duration), from SatVITS-Flood.

## 4) Output

The app will automaticaly download a CSV file to your computer. This CSV file will contain information about the year of the flood, its volume and duration (Fig 4). When SatVITS-Flood is unable to estimate the flood's volume or duration, the year of the flood will be the only data displayed.

<img width="452" alt="image" src="https://user-images.githubusercontent.com/95708635/224549415-cedc8abb-1436-4bc7-8b9d-96b3dd2cb246.png">

Fig 4

## 5) Supplements

We add our raw code used to develop this app. The user can use these codes directly to run SatVITS-Flood on his own data.

Links to the code in GEE for downloading the VIs time series:

MODIS: https://code.earthengine.google.com/3061df7bf284f085233d9a5172d25292

Landsat: https://code.earthengine.google.com/8577a70078a5c0d648274ebb551d2f26

AVHRR: https://code.earthengine.google.com/7aaa10e7a7f40fb8e97747fdbb2157fd
