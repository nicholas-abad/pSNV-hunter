<h1 align="center">pSNV Hunter</h1>

![GitHub last commit](https://img.shields.io/github/last-commit/nicholas-abad/psnv-hunter) ![Github Primarily Language](https://img.shields.io/badge/language-python-yellow) ![Github Number of Dependencies](https://img.shields.io/badge/number_of_dependencies-122-blue) ![GitHub repo size](https://img.shields.io/github/repo-size/nicholas-abad/psnv-hunter)

<h4>Created by Nicholas Abad<sup>1,2,</sup>, Cindy Körner<sup>3</sup> and Lars Feuerbach<sup>1</sup></h3>

<html><sup>1</sup></html> Division of Applied Bioinformatics at the German Cancer Research Center (DKFZ)
<br>
<html><sup>2</sup></html> Faculty of Engineering (Molecular Biotechnology) at Heidelberg University
<br>
<html><sup>3</sup></html> Division of Molecular Genome Analysis at the German Cancer Research Center (DKFZ)

---

***Promoter SNV (pSNV) Hunter*** is a comprehensive data aggregation and visualization tool particularly used to identify functional promoter SNVs within the [REMIND-Cancer project](https://github.com/nicholas-abad/REMIND-Cancer).

Currently, pSNV Hunter is within a closed beta form. However, if you'd like access, please contact Nicholas Abad at nicholas.a.abad@gmail.com.

---

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

<p align="center">
   <img src="./assets/run_visualization_tool.png">
</p>

By default, pSNV Hunter will be running locally at the location listed, which by default and in this case is [http://127.0.0.1:8050](http://127.0.0.1:8050) or [localhost:8050](localhost:8050).

6. You can either click the link if it’s clickable or open a browser and manually type the full link into the address bar. An example can be seen below:

<p align="center">
   <img src="./assets/browser.png" width=80% height=80%>
</p>

7. When you're done using **_pSNV Hunter_**, make sure to stop it from running in the command line by pressing `Ctrl + c`.

## Tutorial

This section will outline the main features of pSNV-Hunter and how to use it. As a reminder, the main goal of **_pSNV Hunter_** is to individually analyze mutations, particularly SNVs within the promoter that have passed the REMIND-Cancer pipeline.

#### Loading in two example datasets

You can load two example datasets included in the repository by clicking the `Load Example Files` button [Step 1]. Conversely, if you wanted to input your own .vcf files, you can load them by clicking on the `Drop and Drag or Select Files` button above it.

Once files are loaded in, basic details such as the filename, the number of rows and the number of columns can be seen. To proceed, click on the `Go to File Viewer` button [Step 2].

<p align="center">
   <img src="./assets/loading_in_data.png">
</p>

#### Choose the dataset to analyze

A window will appear on the left, displaying the uploaded file names along with `Interesting Mutations`. To switch between files, simply click on the desired file [Step 1] and then press `Okay` [Step 2]. The selected file name will be displayed above the file list.

If you need to go back to the file uploader page, click the red `Return to File Uploader` button at the bottom left.

<p align="center">
   <img src="./assets/choosing_dataset.png">
</p>

#### Filter, sort, and download the table

The file you selected will now be displayed in a table-like format as seen below. Conversely, to switch between the uploaded files click on the `View Uploaded Files` button.
<p align="center">
   <img src="./assets/filtering_sorting_downloading.png">
</p>

Using this table, you can filter, sort, and download the dataset. The example below demonstrates how to: (1) filter by a specific string column (e.g., GENE), (2) filter a numerical column (e.g., score) using mathematical expressions, (3) sort the table by a numerical column, and (4) download the filtered dataset.

<p align="center">
   <img src="./assets/vertical_filtering_sorting_downloading.png" width=90% height=90%>
</p>
<br>

#### Selecting a mutation

To view detailed information about an individual, sample-specific mutation, click the blue button to the left of the mutation of interest within the table [Step 1].

After selecting a mutation, you can explore various tabs [Step 2] to view information and graphs related to the chosen mutation.

<p align="center">
   <img src="./assets/selecting_a_mutation.png" width=90% height=90%>
</p>

In short, the seven different selectable tabs can be summarized here:

- **`Patient Info`**: Key details about the mutation, including the number of recurrent mutations (i.e., occurrences of the mutation at this genomic location in other samples), raw and normalized expression values, whether it is classified as a known cancer gene (i.e., listed in the Cancer Gene Census), its presence in a region of open chromatin, allele frequency, CpG island status, and any transcription factor binding sites (TFBSs) that are created or disrupted.
- **`Gene`**: This tab provides information on the gene linked to the SNV, including its expression levels and functional details sourced from NCBI.
- **`Transcription Factors`**: Displays expression levels of transcription factor binding sites (TFBS) predicted to be created or disrupted, along with their associated functions. Additionally, JASPAR2022 sequence logo plots for the TFBS are available.
- **`IGV Genome Browser`**: Integrates the IGV genome browser with the NCBI HG19 genome track and ChromHMM-derived regions of open chromatin for in-depth visualization.
- **`Deep Pileup`**: Presents multiple quality control plots from DeepPileup to assess the signal clarity at the genomic location in question.
- **`Genome Tornado Plots`**: Displays focal copy number alterations (e.g., amplifications and deletions) in the context of the entire PCAWG dataset.
- **`Notes`**: Allows users to take, save, and export notes related to individual mutations for reference.

## Exploring the Seven Analysis Tabs

### `Patient Info`

### `Gene`

### `Transcription Factors`

### `IGV Genome Browser`

### `Deep Pileup`

### `Genome Tornado Plots`

### `Notes`

## To-do:

As this is still in the beta version, I've compiled a list of features that I still need to integrate below. If you'd like to add to this list, please feel free to contact me, open an issue on GitHub and/or send me a pull request!

- [ ] Containerize with Docker
- [ ] Ensure compatibility with regular VCFs
- [ ] Properly implement the `Interesting` column

## Additional Information:

- All images displayed, which are within this repository's `assets` folder, were created using a premium [BioRender.com](https://www.Biorender.com) account and are licensed under CC-BY (Creative Commons). For proof of individual image licenses, please contact Nicholas Abad at `nicholas.a.abad@gmail.com`.
