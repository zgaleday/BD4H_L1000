import org.apache.spark.sql.SparkSession

object launch {
  def main(args: Array[String]): Unit = {
    println("Time for some statistics")
    val spark = SparkSession.builder()
      .master("local")
      .appName("L1000_data")
      .getOrCreate()
  }
}
