import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.SparkSession
import stat.calcOffsidesStats


object launch {
  val appName: String = "bd4h_l1000"
  val clusterId: String = "loacal"
  val sparkConf: SparkConf = new SparkConf().setAppName(appName).setMaster(clusterId)
  val sc: SparkContext = new SparkContext(sparkConf)
  val ss: SparkSession = SparkSession
    .builder()
    .appName(appName)
    .getOrCreate()

  def main(args: Array[String]): Unit = {
    val offsidesData: RDD[Offside] = Utils.readOffsidesData(sc)

    calcOffsidesStats(offsidesData)
    sc.stop()
  }
}
