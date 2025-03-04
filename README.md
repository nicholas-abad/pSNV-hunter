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
3. Download the necessary Python packages.
   ```
   pip install -r requirements.txt
   ```
4. Run pSNV Hunter
   ```
   python src/run_visualization_tool.py
   ```

## Tutorial
#### Loading in an example dataset
![loading in the dataset](./assets/loading_in_data.png)
