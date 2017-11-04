import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD

case class
OffsidesDataRaw(stitchId: String, // 0
                drugName: String, // 1
                umlsId: String, // 2
                event: String, // 3
                rr: Double, // 4
                log2rr: Double, // 5
                tStat: Double, // 6
                pValue: Double, // 7
                observed: Double, // 8
                expected: Double, // 9
                bgCorrection: Double, // 10
                sider: Double, // 11
                futureAers: Double, // 12
                medEffect: Double) // 13


case class
SiderDataRaw(stitchId_flat: String, // 0
             stitchId_stereo: String, // 1
             umlsId_label: String, // 2
             conceptType: String, // 3
             umlsId_meddra: String, // 4
             event: String) // 5

case class
L1000IdsRaw (dummy : String, // 0
             pertId : String, // 1
             smiles : String, // 2
             stitchId : String) // 3

//case class ADRdata (stitchId: Long, umlsId: String, event: String)
case class ADRdata (stitchId: Long, umlsId: String)

case class L1000Ids (stitchId: Long, pertId: String)
case class L1000Perts (pertId : String, perts: Array[Double])
case class L1000Data (stitchId: Long, perts : Array[Double])

object DataProcessing {

  // Files names for all the raw data
  val sider_tsv = "./data/SIDER/meddra_all_se.tsv"
  val offsides_tsv = "./data/3003377s-offsides.tsv"
  val l1000ids_csv = "./data/perts_with_cid.txt"
  val l1000perts_csv = "./data/l1000_scala_features.txt"

  // utility routine to drop double-quotes surrounding the strings in the offsides data
  def dropQuotes(str : String) : String = {
    str.replace("\"", "")
  }

  // utility routine to convert the SIDER stitchId to a Long
  def convertSiderStitchId(stitchId :String) : Long = {
    stitchId.replace("CID", "").toLong - 100000000
  }

  // utility routine to convert the Offsides stitchId to a Long
  def convertOffsidesStitchId(stitchId :String) : Long = {
    stitchId.replace("CID", "").toLong
  }

  // utility routine to convert the Perts stitchId to a Long
  def convertPertsStitchId(stitchId :String) : Long = {
    stitchId.replace("CID", "").toLong
  }

  // top-level routine for this object
  def start(sc : SparkContext) {

    // first read in the offsides and SIDER data into RDDs
    val siderRDD: RDD[ADRdata] =
        sc.textFile(sider_tsv)
          .map(line =>
            {
                val cols = line.split("\t")
                // ADRdata(convertSiderStitchId(cols(0)), cols(2), cols(5))
                ADRdata(convertSiderStitchId(cols(0)), cols(2))
            })

    val offsidesRDD : RDD[ADRdata] =
      sc.textFile(offsides_tsv)
        .map(line =>
        {
          val cols = line.split("\t")
          //ADRdata(convertOffsidesStitchId(dropQuotes(cols(0))), dropQuotes(cols(2)), dropQuotes(cols(3)))
          ADRdata(convertOffsidesStitchId(dropQuotes(cols(0))), dropQuotes(cols(2)))
        })


    // combine the data into one
    val adrRDD = siderRDD.union(offsidesRDD)

    // read in the L1000 ids
    val l1000IdsRDD : RDD[L1000Ids] =
      sc.textFile(l1000ids_csv)
        .map(line =>
        {
          val cols = line.split(",")
          L1000Ids(convertPertsStitchId(cols(3)), cols(1))
        })

    // read in the L1000 perts data
    val l1000PertsRDD : RDD[L1000Perts] =
      sc.textFile(l1000perts_csv)
          .map(line =>
          {
            val cols = line.split(",")
            L1000Perts(cols(0), cols.slice(1,978).map(x => x.toDouble))
          })

    val drugs_sider = siderRDD.map(x => x.stitchId).distinct()
    val drugs_offsides = offsidesRDD.map(x => x.stitchId).distinct()
    val drugs_adr = adrRDD.map(x => x.stitchId).distinct()
    val drugs_l1000 = l1000IdsRDD.map(x => x.stitchId).distinct()

    println("[info] Number of drugs in SIDER = %d".format(drugs_sider.count()))
    println("[info] Number of drugs in Offsides = %d".format(drugs_offsides.count()))
    println("[info] Number of drugs in SIDER and Offsides = %d".format(drugs_adr.count()))
    println("[info] Number of drugs in L1000 = %d".format(drugs_l1000.count()))


    val drugs_sider_l1000 = drugs_sider.intersection(drugs_l1000)
    val drugs_offsides_l1000 = drugs_offsides.intersection(drugs_l1000)
    val drugs_common = drugs_adr.intersection(drugs_l1000)

    println("[info] Number of drugs common in SIDER and L1000 = %d".format(drugs_sider_l1000.count()))
    println("[info] Number of drugs common in Offsides and L1000 = %d".format(drugs_offsides_l1000.count()))
    println("[info] Number of drugs common = %d".format(drugs_common.count()))

    val se_adr = adrRDD.map(x => x.umlsId).distinct()
    println("[info] Number of side effects = %d".format(se_adr.count()))

    val drug_se = adrRDD.map(x => (x.stitchId, x.umlsId)).groupByKey()
    drug_se.coalesce(1, true).saveAsTextFile("all_side_effects")

    val drug_perts = l1000IdsRDD.map(x => (x.pertId, x.stitchId)).join(l1000PertsRDD.map(x =>(x.pertId, x.perts))).map(x => (x._2._1, x._2._2))
    drug_perts.coalesce(1, true).saveAsTextFile("all_perts")

    val drug_se_perts = drug_se.join(drug_perts)
    println("[info Number of data rows = %d".format(drug_se_perts.count()) )

  }

}