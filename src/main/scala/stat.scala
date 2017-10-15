import org.apache.spark.rdd.RDD


object stat {
  def calcOffsidesAdrPerDrug(data: RDD[Offside]): Unit = {

  }

  def calcOffsidesStats(data: RDD[Offside]): Unit = {
    calcOffsidesAdrPerDrug(data)
  }
}
