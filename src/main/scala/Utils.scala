import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD


object Utils {
  def readOffsidesData(sc: SparkContext): RDD[Offside] = {
    sc
      .textFile("../BD4H_L1000/data/3003377s-offsides.tsv")
      .map((line) => {
        val fields = line.split("\t")

        Offside(
          fields(0),
          fields(1),
          fields(2),
          fields(3),
          fields(4).toDouble,
          fields(5).toDouble,
          fields(6).toDouble,
          fields(7).toDouble,
          fields(8).toDouble,
          fields(9).toDouble,
          fields(10).toDouble,
          fields(11).toDouble,
          fields(12).toDouble,
          fields(13).toDouble)
      })
      .cache()
  }

  // https://stackoverflow.com/questions/28158729/how-can-i-calculate-exact-median-with-apache-spark
  def calcMedian(data: RDD[Int]): Double = {
    val sorted = data.sortBy(identity).zipWithIndex().map {
      case (v, idx) => (idx, v)
    }

    val count = sorted.count()

    if (count % 2 == 0) {
      val l = count / 2 - 1
      val r = l + 1

      (sorted.lookup(l).head + sorted.lookup(r).head).toDouble / 2
    } else {
      sorted.lookup(count / 2).head.toDouble
    }
  }
}
