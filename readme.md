# BD4H L1000 Project

## Overview
We chemistry, drugs, and data!

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

## Launching Modealing (Python)
1) `conda env create -f env.yml` to create env and load dependencies
2) `source activate bd4h_l1000` to activate env
3) `source deactivate` to deactivate

## OFFSIDES Data
To run the offsides statistics and classification vector construction follow the following steps:
1) Download: https://api.pharmgkb.org/v1/site/redirect?p=https%3A%2F%2Fstanford.box.com%2Fshared%2Fstatic%2Fpgc2z0pke4w2z1p6540h.zip
2) Unzip and delete the header of the file
3) Place file into the /data dir

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

## Helpful Links

* [SparkSql](https://spark.apache.org/docs/latest/sql-programming-guide.html#sql)
* [MLLib](https://spark.apache.org/docs/latest/ml-guide.html)
