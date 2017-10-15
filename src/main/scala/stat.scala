import org.apache.spark.rdd.RDD
import Utils.calcMedian


object stat {
  def calcOffsidesAdrsPerDrug(data: RDD[Offside]): Unit = {
    val adrPerDrug = data
      .map((o) => (o.stitchId, o.umlsId))
      .distinct()
      .groupBy(_._1)
      .map(_._2.size)

    println(
      "ADRs per Drug",
      "min, max, mean, median ",
      adrPerDrug.min(),
      adrPerDrug.max(),
      adrPerDrug.mean(),
      calcMedian(adrPerDrug))
  }

  def calcOffsidesDrugsPerAdr(data: RDD[Offside]): Unit = {
    val drugsPerAdr = data
      .map((o) => (o.stitchId, o.umlsId))
      .distinct()
      .groupBy(_._2)
      .map(_._2.size)

    println(
      "Drugs per ADR",
      "min, max, mean, median ",
      drugsPerAdr.min(),
      drugsPerAdr.max(),
      drugsPerAdr.mean(),
      calcMedian(drugsPerAdr))
  }

  def calcOffsidesStats(data: RDD[Offside]): Unit = {
    calcOffsidesAdrsPerDrug(data)
    calcOffsidesDrugsPerAdr(data)
  }
}
