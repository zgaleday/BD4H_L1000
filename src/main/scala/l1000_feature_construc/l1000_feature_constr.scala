package l1000_feature_construc

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, SparkSession}


object l1000_feature_constr {
  def loadFeatures(spark: SparkSession): DataFrame = {
    val perts = loadPerts(spark)
    perts.show(10)
    spark.read.format("csv").
      option("header", "true").
      option("delimiter", ",").
      load("data/l1000_scala_features.txt")
  }

  def loadPerts(spark: SparkSession): DataFrame = {
    spark.read.format("csv").
      option("header", "true").
      option("delimiter", "\t").
      load("data/GSE92742_Broad_LINCS_sig_info.txt")
  }
}
