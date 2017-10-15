package l1000_feature_construc

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{DataFrame, SparkSession}


object l1000_feature_constr {
  def loadFeatures(spark: SparkSession): DataFrame = {
    spark.read.format("csv").
      option("header", "true").
      option("delimiter", "\t").
      load("data/l1000_scala_features.txt")
  }
}
