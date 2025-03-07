# pSNV Hunter

Promoter SNV (pSNV) Hunter is a comprehensive data aggregation and visualization tool particularly used to identify functional promoter SNVs within the REMIND-Cancer project.

Currently, pSNV Hunter is within a closed beta form. However, if you'd like access, please contact Nicholas Abad at nicholas.a.abad@gmail.com.

## Run pSNV Hunter

1. Clone the repository and the submodule
   ```
   git clone --recurse-submodules -j8 https://github.com/nicholas-abad/pSNV-hunter.git
   ```
2. Open the terminal and change directories into `REMIND-Cancer-visualization `
   ```
   cd pSNV-hunter/REMIND-Cancer-visualization
   ```
3. Download the necessary Python packages using .
   ```
   pip install -r requirements.txt
   ```
4. Run pSNV Hunter
   ```
   python src/run_visualization_tool.py
   ```
5. The prior Python command should output the following:

<center>
<img src="./assets/run_visualization_tool.png">
</center>

By default, pSNV Hunter will be running locally at the location listed, which by default and in this case is [http://127.0.0.1:8050](http://127.0.0.1:8050) or [localhost:8050](localhost:8050).

6. You can either click the link if it’s clickable or open a browser and manually type the full link into the address bar. An example can be seen below:

<center>
<img src="./assets/browser.png">
</center>

7. When you're done using **_pSNV Hunter_**, make sure to stop it from running in the command line by pressing `Ctrl + c`.

## Tutorial

This section will outline the main features of pSNV-Hunter and how to use it. As a reminder, the main goal of **_pSNV Hunter_** is to individually analyze mutations, particularly SNVs within the promoter that have passed the REMIND-Cancer pipeline.


#### Loading in two example datasets
You can load two example datasets included in the repository by clicking the `Load Example Files` button [Step 1]. Conversely, if you wanted to input your own .vcf files, you can load them by clicking on the `Drop and Drag or Select Files` button above it.

Once files are loaded in, basic details such as the filename, the number of rows and the number of columns can be seen. To proceed, click on the `Go to File Viewer` button [Step 2].

![loading in the dataset](./assets/loading_in_data.png)

#### Choose the dataset to analyze
A window will pop up to the left, which contains the different file names that you have in addition to `Interesting Mutations`. To navigate between the uploaded files, click on them directly [Step 1] and then press `Okay` [Step 2]. The selected file name should also appear above the file list.

Conversely, if you wanted to return back to the file uploader page, click on the red bottom left button `Return to File Uploader`.

![choosing dataset](./assets/choosing_dataset.png)

#### Filter, sort, and download the table

![filtering, sorting, and downloading](./assets/filtering_sorting_downloading.png)

<center>
<img src="./assets/vertical_filtering_sorting_downloading.png" width=70% height=70%>
</center>
<br>

#### Select a mutation
