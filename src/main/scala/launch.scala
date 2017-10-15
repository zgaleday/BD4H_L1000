import org.apache.spark.sql.SparkSession
import l1000_feature_construc.l1000_feature_constr._

object launch {
  def main(args: Array[String]): Unit = {
    println("Time for some statistics")

    val l1000_data = loadFeatures(ss, "data/l1000_scala_features.txt")
  }
}
