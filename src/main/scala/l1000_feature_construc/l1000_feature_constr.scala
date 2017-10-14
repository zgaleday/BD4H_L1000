package l1000_feature_construc

import org.apache.spark.sql.{DataFrame, SparkSession}

object l1000_feature_constr {
  def loadFeatures(spark: SparkSession, f_path: String): DataFrame = {
    spark.read.format("csv").
      option("header", "true").
      option("delimiter", "\t").
      load(f_path)
  }
}
