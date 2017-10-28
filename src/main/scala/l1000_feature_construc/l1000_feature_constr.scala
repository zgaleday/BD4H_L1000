package l1000_feature_construc

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._


object l1000_feature_constr {

  //Loads in the L1000 feature vectors with CIDs as the key
  def loadFeatures(spark: SparkSession): DataFrame = {
    val features = spark.read.format("csv").
      option("header", "true").
      option("delimiter", ",").
      load("data/l1000_scala_features.txt")
    val perts = loadPerts(spark).select("pert_id", "CID").
      join(features, "pert_id").drop("pert_id")
    perts
  }


  //Loads in the perts from the output of CID curation (allowing for join with ADRs)
  def loadPerts(spark: SparkSession): DataFrame = {
    spark.read.format("csv").
      option("header", "true").
      option("delimiter", ",").
      load("data/perts_with_cid.txt")
  }
}
