# BD4H L1000 Project

## Overview
We love chemistry, drugs, and data!

## Contributors
1) \#zgd || Zachary Gale-Day
2) \#deven || Deven Desai
3) \#ddey || Daniel Deychakiwsky

## Environment
1) Java 1.8
2) Sbt 0.13.16
3) Scala 2.11.8

See `build.sbt` for dependency versioning

## Launching Feature Construction (Scala)
Run the following commands in the root dir
* `sbt`
* `clean`
* `project bd4h_l1000`
* `runMain launch`

## Launching Modeling (Python)
1) `conda env create -f env.yml` to create env and load dependencies
2) `source activate bd4h_l1000` to activate env
3) `source deactivate` to deactivate

## OFFSIDES Data
To run the offsides statistics and classification vector construction follow the following steps:
1) Download: https://api.pharmgkb.org/v1/site/redirect?p=https%3A%2F%2Fstanford.box.com%2Fshared%2Fstatic%2Fpgc2z0pke4w2z1p6540h.zip
2) Unzip and delete the header of the file
3) Place file into the /data dir
4) Deleted the header

## SIDER Data
To run the SIDER statistics and classification vector construction follow the following steps:
1) Navigate to http://sideeffects.embl.de/download/
2) Download the meddra.tsv, meddra_all_se.tsv and meddra_freq.tsv files
3) Place these files in the /data dor

## L1000 Data
To run the L1000 statistics and classification it is recommended that you start from the intermediate files provided:
1) Download https://drive.google.com/file/d/0B0694sXjQ1_wcUtQSm9jeEgtZkk/view?usp=sharing
2) Download https://drive.google.com/file/d/0B0694sXjQ1_wWHJvS1RIRVRCcE0/view?usp=sharing
3) Move these files into the /data dir

## Feature File for training
Download the file at:
https://drive.google.com/file/d/1fWUxgTo0QFOss_xNZgTdUM2qRkFtHtEg/view?usp=sharing

## Pre-selected features for training with CustomBRClassifier
For 25 features selected with RFE dowload:
https://drive.google.com/file/d/1H4Jei_yPlKu1yFFRvsOP9VcdgJX1HjeY/view?usp=sharing

## Helpful Links

* [SparkSql](https://spark.apache.org/docs/latest/sql-programming-guide.html#sql)
* [MLLib](https://spark.apache.org/docs/latest/ml-guide.html)

## Running Instructions

Use the included env.yml to build the required python environment

It is recommended that you start with the intermediate files about otherwise there is about 25 hours of combined running time for
various data preprocessing steps, for instructions with this intermediate representation see here.  For full data preprocessing instructions
see below.

#### Training our models

1) If all of the above file are included in your data directory nagivate to src/main/python
2) To reproduce the models shown in the paper simply run main.py

#### Filtering L1000 Dataset
Warning this is a very slow and space intensive process it is recommended to start from the preprocessed data above!
1) Navigate to https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE70138
2) Download GSE70138_Broad_LINCS_Level5_COMPZ_n118050x12328_2017-03-06.gctx.gz
3) Download GSE70138_Broad_LINCS_gene_info_2017-03-06.txt.gz
4) Download GSE70138_Broad_LINCS_pert_info.txt.gz
5) Download GSE70138_Broad_LINCS_sig_info_2017-03-06.txt.gz
6) Unpack all files and move then to the data directory of this project (warning over 30 gb free space required)
7) Open the parse_l1000.py file in src/parse_l1000
8) Run reduce_and_save()
9) Run read_reduced() and save as a df
10) use this df as an input to the max_mag_sig method with default params
11) This will produce the l1000_scala_features.txt from above

#### Finding CIDs for compounds in L1000

Warning this does about 8 hours of API calls recommended to from the link in L1000 data section
1) Run the read_cmpnds method in src/parse_l1000/find_cids.py (This generates perts_with_cid.txt)

#### Generating final feature vectors for training

1) Import the Scala project (build.sbt in the BD4H_L1000 dir) into IntelliJ
2) Delete the header from the meddra_all_label_se.tsv and 3003377s-offsides.tsv
2) Run the "main" routine in the "src.main.scala.launch" object
Please ensure that all the raw data has been downloaded into the "./data" directory as described in the prior sections
3) The output of this stage will be stored in the "./data/combined/part-0000" file
4) Rename this file pandas_input_combined.csv and move to the main data directory
5) Paste the header to the top of the file by opening a txt editor, searching for CID and cutting this line from its location
to the top of the file

This is good to go for training an model creation! See description above for details!

#### Running Feature Selection
We are running recursive feature selection and the current implementation would run before each model training.  It is therefore recommended to either
use our preselected features or run feature selection once (saving you file see docstring in comment) otherwise result reproduction will take several days
most likely.
1) Navigate to line 91 of models.py
2) sets the select_feats parameter of model.fit == True
3) Run main.py as before.
If you want to run single models you can remove models from the array in main.py.
Valid arguements are "logistic", "tree", "forest", "nnet", "adaboost", "extra", "SVC"
