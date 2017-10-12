name := "BD4H_L1000"

version := "1.0"

scalaVersion := "2.12.3"

val sparkVersion = "2.2.0"

libraryDependencies ++= Seq(
  "org.apache.spark" % "spark-core_2.10" % sparkVersion % Provided,
  "org.apache.spark" % "spark-sql_2.10" % sparkVersion,
  "org.apache.spark" % "spark-mllib_2.10" % sparkVersion
)
        