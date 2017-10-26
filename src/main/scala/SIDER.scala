import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD


object SIDER {

  def read_meddra_tsv(sc : SparkContext) = {

    val meddra_tsv = "./data/SIDER/meddra.tsv"
    val meddraRDD = sc.textFile(meddra_tsv)
    val sideEffects = meddraRDD
      .map(x => x.split('\t'))   // (UMLS concept id, kind of term, MedDRA id, name of side effect)
      .map(x => (x(0), (x(2), x(1), x(3))))  // (UMLS concept id, (MedDRA id, kind of term, side effect name))
      .groupByKey()

    println ("[info] Number of distinct side effects in meddra.tsv = %d".format(sideEffects.count()))
  }

  def print_min_max_avg_median(rdd : RDD[Int], name : String) = {

    val arr = rdd.collect()
    val min = arr.min
    val max = arr.max
    val mean = arr.sum / arr.size.toDouble
    val median = arr.sorted.drop(arr.length/2).head

    println("[info] min, max, mean, median for (%s) = %d, %d, %f, %d".format(name, min, max, mean, median))
  }

  def read_meddra_all_se_tsv(sc : SparkContext)  = {

    val all_se_tsv = "./data/SIDER/meddra_all_se.tsv"
    val all_se_rdd = sc.textFile(all_se_tsv).map(x => x.split('\t'))

    val freq_tsv = "./data/SIDER/meddra_freq.tsv"
    val freq_rdd = sc.textFile(freq_tsv).map(x => x.split('\t'))

    val drugs = all_se_rdd.map(x => x(0)).distinct()
    println ("[info] Number of distinct drugs in meddra_all_se.tsv = %d".format(drugs.count()))

    val side_effects =  all_se_rdd.map(x => x(2)).distinct()
    println ("[info] Number of distinct side_effects in meddra_all_se.tsv = %d".format(side_effects.count()))

    val drug_se_pairs = all_se_rdd.map(x =>(x(0), x(2))).distinct()
    println ("[info] Number of distinct drug_se_pairs in meddra_all_se.tsv = %d".format(drug_se_pairs.count()))

    val drug_se_freq  = freq_rdd.filter(x => (x(3) != "placebo")).map(x => ((x(0), x(2)),(x(4), x(5), x(6)))).groupByKey()
    println ("[info] Number of distinct drug_se_pairs in meddra_freq.tsv = %d".format(drug_se_freq.count()))

    val drug_se_freq_placebo  = freq_rdd.filter(x => (x(3) == "placebo")).map(x => ((x(0), x(2)),(x(4), x(5), x(6)))).groupByKey()
    println ("[info] Number of distinct drug_se_pairs (placebo) in meddra_freq.tsv = %d".format(drug_se_freq_placebo.count()))


    val num_se_per_drug = all_se_rdd
      .map(x => (x(0), x(2)))
      .distinct()
      .groupByKey()
      .map(x => x._2.count(x => true).toInt)

    print_min_max_avg_median(num_se_per_drug, "Number Of Side Effects per Drug")

    val num_drug_per_se = all_se_rdd
      .map(x => (x(2), x(0)))
      .distinct()
      .groupByKey()
      .map(x => x._2.count(x => true).toInt)


    print_min_max_avg_median(num_drug_per_se, "Number Of Drugs per Side Effect")

  }


}
