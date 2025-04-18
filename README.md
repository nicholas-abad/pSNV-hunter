# pSNV Hunter

![GitHub Release](https://img.shields.io/github/v/release/nicholas-abad/psnv-hunter?include_prereleases) ![GitHub last commit](https://img.shields.io/github/last-commit/nicholas-abad/psnv-hunter) ![GitHub top language](https://img.shields.io/github/languages/top/nicholas-abad/psnv-hunter) ![Github Number of Dependencies](https://img.shields.io/badge/number_of_dependencies-122-blue) ![GitHub repo size](https://img.shields.io/github/repo-size/nicholas-abad/psnv-hunter) ![Docker Pulls](https://img.shields.io/docker/pulls/nicholasabad/psnv-hunter)



<h4>Created by Nicholas Abad<sup>1,2,</sup>, Cindy Körner<sup>3</sup> and Lars Feuerbach<sup>1</sup></h4>

<html><sup>1</sup></html> Division of Applied Bioinformatics at the German Cancer Research Center (DKFZ)
<br>
<html><sup>2</sup></html> Faculty of Engineering (Molecular Biotechnology) at Heidelberg University
<br>
<html><sup>3</sup></html> Division of Molecular Genome Analysis at the German Cancer Research Center (DKFZ)
<br>

![Github Number of Dependencies](https://img.shields.io/badge/repository_maintainer-nicholas_abad_(nicholas.a.abad@gmail.com)-lightgreen)

***Promoter SNV (pSNV) Hunter*** is a comprehensive data aggregation and visualization tool particularly used to identify functional promoter SNVs within the [REMIND-Cancer project](https://github.com/nicholas-abad/REMIND-Cancer).

![](./assets/pSNV_Hunter.png)

---

## Run pSNV Hunter

### Option 1: Locally

1. Clone the repository.
   ```
   git clone https://github.com/nicholas-abad/pSNV-hunter.git
   ```
2. Download the necessary Python packages using pip.
   ```
   pip install -r requirements.txt
   ```
3. Run pSNV Hunter
   ```
   python src/run_visualization_tool.py
   ```
4. The prior Python command should output the following:

![](./assets/run_visualization_tool.png)

By default, pSNV Hunter will be running locally at the location listed, which by default and in this case is [http://127.0.0.1:8050](http://127.0.0.1:8050) or [localhost:8050](localhost:8050).

6. You can either click the link if it’s clickable or open a browser and manually type the full link into the address bar. An example can be seen below:

![](./assets/browser.png)

7. When you're done using **_pSNV Hunter_**, make sure to stop it from running in the command line by pressing `Ctrl + c`.


### Option 2: Run with Docker
1. Pull the latest image
   ```
   docker pull nicholasabad/psnv-hunter:beta_0.1
   ```
3. Run while exposing port 8050
   ```
   docker run -p 8050:8050 nicholasabad/psnv-hunter:beta_0.1
   ```
5. Navigate to localhost:8050 in your browser.


## Tutorial

This section will outline the main features of pSNV-Hunter and how to use it. As a reminder, the main goal of **_pSNV Hunter_** is to individually analyze mutations, particularly SNVs within the promoter that have passed the REMIND-Cancer pipeline.

#### Loading in two example datasets

You can load two example datasets included in the repository by clicking the `Load Example Files` button [Step 1]. Conversely, if you wanted to input your own .vcf files, you can load them by clicking on the `Drop and Drag or Select Files` button above it.

Once files are loaded in, basic details such as the filename, the number of rows and the number of columns can be seen. To proceed, click on the `Go to File Viewer` button [Step 2].

![](./assets/loading_in_data.png)

#### Choose the dataset to analyze

A window will appear on the left, displaying the uploaded file names along with `Interesting Mutations`. To switch between files, simply click on the desired file [Step 1] and then press `Okay` [Step 2]. The selected file name will be displayed above the file list.

If you need to go back to the file uploader page, click the red `Return to File Uploader` button at the bottom left.

![](./assets/choosing_dataset.png)

#### Filter, sort, and download the table

The file you selected will now be displayed in a table-like format as seen below. Conversely, to switch between the uploaded files click on the `View Uploaded Files` button.

![](./assets/filtering_sorting_downloading.png)

Using this table, you can filter, sort, and download the dataset. The example below demonstrates how to: (1) filter by a specific string column (e.g., GENE), (2) filter a numerical column (e.g., score) using mathematical expressions, (3) sort the table by a numerical column, and (4) download the filtered dataset.

![](./assets/vertical_filtering_sorting_downloading.png)
<br>

#### Selecting a mutation

To view detailed information about an individual, sample-specific mutation, click the blue button to the left of the mutation of interest within the table [Step 1].

After selecting a mutation, you can explore various tabs [Step 2] to view information and graphs related to the chosen mutation.

![](./assets/selecting_a_mutation.png)

In short, the seven different selectable tabs can be summarized here:

- **`Patient Info`**: Key details about the mutation, including the number of recurrent mutations, raw and normalized expression values, whether it is classified as a known cancer gene (i.e., listed in the Cancer Gene Census), its presence in a region of open chromatin, allele frequency, CpG island status, and any transcription factor binding sites (TFBSs) that are created or disrupted.
- **`Gene`**: This tab provides information on the gene linked to the SNV, including its expression levels and functional details sourced from NCBI.
- **`Transcription Factors`**: Displays expression levels of transcription factor binding sites (TFBS) predicted to be created or disrupted, along with their associated functions. Additionally, JASPAR2022 sequence logo plots for the TFBS are available.
- **`IGV Genome Browser`**: Integrates the IGV genome browser with the NCBI HG19 genome track and ChromHMM-derived regions of open chromatin for in-depth visualization.
- **`Deep Pileup`**: Presents multiple quality control plots from DeepPileup to assess the signal clarity at the genomic location in question.
- **`Genome Tornado Plots`**: Displays focal copy number alterations (e.g., amplifications and deletions) in the context of the entire PCAWG dataset.
- **`Notes`**: Allows users to take, save, and export notes related to individual mutations for reference.

## Exploring the Seven Analysis Tabs

### `Patient Info`

**Example**

![](./assets/patient_info.png)

**Description**
The `Patient Info` tab is by default the first tab chosen when selecting an individual mutation to analyze. Here, the name of the gene that the pSNV is associated with, which in this example is _ANKRD53_, is shown at the top as well as the mutations nucleotide change (e.g. G to A), the chromosomal location and the strand the SNV was found in.

Furthermore, the eight boxes represent key mutational details. First, _Recurrence Mutations_ refers to the number of occurrences of the mutation at this genomic location in other samples, which has been used in identifying functional pSNVs such as within the promoter of _TERT_. Secondly, the raw and Z-score normalized expression values can be seen here. Within the REMIND-Cancer pipeline, normalization was relative to only those samples within the cohort.

Next, the presence of this mutation within the Cancer Gene Census (CGC) database is noted here such that a value of `True` means that this gene is a known cancer gene. Additionally, the fact that this mutation lays in a region of open chromatin according to ChromHMM annotations is denoted here. To specifically see regions of open chromatin, refer to the `IGV Genome Browser` where these are listed as a track. Furthermore, the variant allele frequency as well as whether this mutation lays within a CpG island is also denoted.

The last two boxes contain information regarding the predicted created and destroyed TFBS' according to JASPAR2022. Here, a TFBS is predicted to be created if it's binding affinity is greater than or equal to 11 whereas it's predicted to be destroyed if it's less than or equal to 0.09.

**Notes About The Code**
To ensure proper display of these boxes, update the `_config.py` file by aligning the dictionary keys in `DATAFRAME_SETTINGS` with your dataset's column names:

- **Recurrence Mutations**: `name_of_paths_with_recurrence_column`
- **Gene Expression**: `name_of_expression_column`, `name_of_normalized_expression_column`
- **Created Transcription Factors**: `name_of_column_with_list_of_created_tfbs`
- **Destroyed Transcription Factors**: `name_of_column_with_list_of_destroyed_tfbs`

**Note:** The following attributes have not yet been integrated:

- **Within CGC List**
- **Open Chromatin**
- **Allele Frequency**
- **CpG Island**

Make sure these keys correspond to your dataset to properly render the necessary information.

### `Gene`

**Example**

![](./assets/gene.png)

**Description**
The `Gene` tab offers detailed information about the gene associated with the SNV. It includes **interactive violin plots** that display gene expression across samples. The sample of interest is marked in red while other recurrent samples with the same mutation appear in black. By default, the normalized expression is shown but users can select other measures (e.g., Z-score, raw, logged) from the legend on the right.

These plots (and all subsequent visualizations) are **interactive**, enabling users to zoom into specific areas by dragging to create a selection box and hover over individual data points for more details. A brief demonstration video is available below:

https://github.com/user-attachments/assets/07d8c7d2-4a21-4019-aed5-fae15564ab6e

Below the violin plot, the **NCBI gene function** is shown if available. These descriptions were sourced from [this repository](https://github.com/nicholas-abad/ncbi_gene_names_and_descriptions) and last updated on 4 February 2025. The definitions should align with those on [GeneCards.com](GeneCards.com).

**Notes About The Code**
Placeholder.

### `Transcription Factors`

**Example**
**Description**
Within the `Transcription Factors` tab, a secondary set of tabs pop up that represents both the created (green) and destroyed (red) TFBS'.

Utilizing the Find Individual Motif Occurrences (FIMO) tool from the MEME Suite toolkit along with the JASPAR2020 database of curated transcription factors, the hg19 reference DNA sequence of +/-10 bp around every pSNV underwent scanning by FIMO against every TF motif in JASPAR2020. Using the positional weight matrix of the TF and its associated sequence context, FIMO calculated a statistical binding affinity score, which indicates the likelihood of observing the specific motif. To assess the impact of a mutation, the ratio (denoted as S(TFBS)) between the binding affinity scores for the mutant over the wild type allele was calculated as a quantitative measure indicating the impact of mutations on the binding motif of TFs. Motifs with S(TFBS)>11 were defined as a created TFBS motif and S(TFBS)<0.09 as a destroyed TFBS motif. 

By selecting one of the created or destroyed tabs, the known gene function (similar to the `Gene` tab) is displayed alongside the expression values of the associated transcription factor. By default, the raw expression values serve as a proxy for TF activity, but users can switch to Z-score or logged expression using the options on the right side of the violin plot.

Below the plots are two pieces of information: the JASPAR2022 sequence logo plot and the actual sequence surrounding the mutation (i.e. sequence context). To verify that the sequence context aligns with the known motif, users can drag the actual sequence on the right to align it with the sequence logo on the left. Ideally, a perfect match should be observed for a created or destroyed TFBS.

For the sequence logo plot, clicking the left or right arrows toggles between the reverse complement and the original sequence logo.

**Notes About The Code**
Placeholder.

### `IGV Genome Browser`

**Example**

![](./assets/igv_genome_browser.png)

**Description**
The `IGV Genome Browser` tab integrates the **Integrative Genomics Viewer (IGV)** to provide a detailed visualization of genomic regions relevant to the selected mutation. This tool allows users to explore regions of open chromatin (ChromHMM track; red), RefSeq genes (RefSeq track; blue) and NCBI reference genes (NCBI track; yellow) mapped according to the hg19 genome assembly.

To easily pinpoint the mutation, click the Center Line button in the top-right corner. This will add a light gray line indicating the exact mutation position. By default, the browser displays a ±3,000 bp region around the mutation, but users can zoom in or out to adjust the view.

**Notes About The Code**
Within the Dash ID tab-igv, users can add additional publicly available tracks, including the default RefSeq track and the publicly available NCBI track, which is hosted in an AWS S3 bucket. The ChromHMM track is loaded directly from a BED file utilized in the REMIND-Cancer filtering pipeline. This file is available [here](https://raw.githubusercontent.com/nicholas-abad/REMIND-Cancer/refs/heads/main/examples/data/annotations/chromhmm.bed). Further documentation regarding IGV's implementation can be seen [here](https://dash.plotly.com/dash-bio/igv) using Dash and, in particular, the [Dash Bio](https://dash.plotly.com/dash-bio) library.

### `Deep Pileup`

**Example**

![](./assets/deep_pileup.png)

**Description**
The `Deep Pileup` tab displays quality control plots to help with assessing the signal clarity at the specific genomic location of the selected mutation. The initial two plots are described below:

- **Patients with a minor allele frequency greater than 25%**
- **Patients with at least 2 variant alleles**

Ideally, these plots should show no signal in control samples but a clear signal in tumor samples. Below, a good example (left) and a potential artificat (right) are shown for the ANKRD53 pSNV and NF2 pSNV:

![](./assets/deep_pileup_good_and_bad.png)

These initial plots only include cohorts on the x-axis that exhibit a signal in either tumor or control samples, making visualization easier. However, the subsequent two plots display the same data across all cohorts, providing a broader perspective.

**Notes About The Code**
These plots were generated within the `./src/plots/_get_deep_pileup_plots.py` file, which generate a plot given a _Deep Pileup repository_. This repository is nothing more than a folder with genes, genomic locations and their corresponding `Overview.tsv` files. The path to this overarching repository can be changed within the `_config.py` file, particularly within the variable `PATH_TO_DEEP_PILEUP_REPOSITORY`.

To generate this Deep Pileup repository / folder of overview files, the [Deep Pileup repository](https://github.com/nicholas-abad/deep-pileup-wrapper) can be used. In particular, by passing in a metadata file, which maps samples to cohorts as well as samples to the location of their BAM files, the following folder structure will be outputted:

```
deep_pileup_repository/
├── ANKRD53/
│   ├── chr2:71204529/
│   │   ├── Overview.tsv
├── TERT/
│   ├── chr5:1295228/
│   │   ├── Overview.tsv
│   ├── chr5:1295250/
│   │   ├── Overview.tsv
├── ...
```

### `Genome Tornado Plots`

**Example**

![](./assets/genome_tornado_plots.png)

**Description**
The `Genome Tornado Plots` tab provides an overview of dataset-wide focal deletions and amplifications in comparison to the PCAWG dataset. Since an increase in copy number can lead to higher gene expression, these plots offer insights into convergent tumor evolution, illustrating how different genomic events may drive similar biological outcomes.

**Notes About The Code**
The code display plots that have been previously-generated using the [Genome Tornado Plots Wrapper repository](https://github.com/nicholas-abad/genome-tornado-plot-wrapper). This wrapper script was initially created to easily flow into the REMIND-Cancer filtering pipeline as well as pSNV Hunter. Please refer to the [original Genome Tornado Plots repository](https://github.com/chenhong-dkfz/GenomeTornadoPlot) as well as the corresponding [paper](https://academic.oup.com/bioinformatics/article/38/7/2036/6517781).

### `Notes`
**Example**
![](./assets/notes.png)

**Description**
The `Notes` tab allows users, whether working individually or as part of a molecular tumor board, to take and save mutation-specific notes that remain private to each entry. Users can add multiple timestamped comments, which can be saved by clicking the Save Comment button and removed by selecting the red X next to the comment.

This feature is especially useful for recording observations about a mutation’s potential significance, including factors that may warrant further investigation or functional validation in the future.

Future versions of pSNV Hunter will include the ability to export notes individually, and development is currently in progress to implement this feature.

**Notes About The Code**
By default, pSNV Hunter creates a new column in the dataframe called `Notes`. If a column with the same name already exists, it may cause conflicts or unexpected behavior.

## To-do:

As this is still in the beta version, I've compiled a list of features that I still need to integrate below. If you'd like to add to this list, please feel free to contact me, open an issue on GitHub and/or send me a pull request!

- [ ] Containerize with Docker
- [ ] Ensure compatibility with regular VCFs
- [ ] Properly implement the `Interesting` column
- [ ] Ensure that the `Notes` are saved with the ability to export.
- [ ] Make it available on PyPi

## Additional Information:

- All images displayed, which are within this repository's `assets` folder, were created using a premium [BioRender.com](https://www.Biorender.com) account and are licensed under CC-BY (Creative Commons). For proof of individual image licenses, please contact Nicholas Abad at `nicholas.a.abad@gmail.com`.
