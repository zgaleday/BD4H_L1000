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
  }
}
