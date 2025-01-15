// /opt/mapr/spark/spark-2.3.1/bin/spark-shell \
// --master yarn \
// --deploy-mode client \
// --driver-memory 1g \
// --executor-memory 5g \
// --num-executors 2 \
// --executor-cores 2 \
// --queue mapr_etl_svcaccnts \
// --conf "spark.jars.packages=com.google.cloud.spark:spark-bigquery-with-dependencies_2.11:0.16.1" \
// --conf "spark.yarn.executor.memoryOverhead=2000" \
// --conf "spark.newwork.buffer.timeout=300s" \
// --conf "spark.sql.shuffle.partitions=65" \
// --conf "spark.sql.parquet.writeLegacyFormat=true"


import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.io.{File, FileOutputStream, BufferedOutputStream}
import java.util.zip.{ZipEntry, ZipOutputStream}
import org.zeroturnaround.zip.ZipUtil
import com.jcraft.jsch.{ChannelSftp, JSch}


class file_move{
  
  def make_zip(csv_path:String):Int = {

      try{
        ZipUtil.pack(new File(csv_path), new File(f"${csv_path}.zip"))
        println("succssfully finished..")
        return 1
      }
      catch {
        case e: Exception =>
          println(s"Error zipping folder: ${e.getMessage}")
          return 0
      }
  }

  def migrate(sftpHost:Int, sftpUsername:String, sftpPassword:String, sftpFilePath:String, localFilePath:String, cdpath:String):Int = {

    val sftpHost = sftpHost // "PWSFTP01.classic.pchad.com"
    val sftpPort = 22
    val cdpath = cdpath
    val sftpUsername = sftpUsername // "spectmims"
    val sftpPassword = sftpPassword // "Fall2016"
    val sftpFilePath =  sftpFilePath // "/Spectrum_MIMS_Product_Views/test2/part-00000-c11d996e-a697-4664-adc2-fb1d276a0fac-c000.csv" // specify the destination path on the SFTP server
    val localFilePath = localFilePath // "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/staging_temp/bigdata/prod/test/thamo/bq_to_sftp_zip_move/spark_test/TestFloder/ / data/part-00000-c11d996e-a697-4664-adc2-fb1d276a0fac-c000.csv"     // specify the local file path


    val jsch = new JSch()
    val session = jsch.getSession(sftpUsername, sftpHost, sftpPort)
    session.setPassword(sftpPassword)
    session.setConfig("StrictHostKeyChecking", "no")
    session.connect()


    try {
      val channel = session.openChannel("sftp").asInstanceOf[ChannelSftp]
      channel.connect()

      try {
        channel.cd(cdpath)

        channel.put(localFilePath, sftpFilePath)

        println(s"File uploaded successfully to $sftpHost:$sftpFilePath")
        return 1
      } catch {
        case e: Exception =>
          println(s"Error Migration folder: ${e.getMessage}")
          return 0
      } finally {
        channel.disconnect()
      }
    } catch {
      case e: Exception =>
        println(s"Error Migration folder: ${e.getMessage}")
        return 0
    } finally {
      session.disconnect()
    }

  }

}


object sftpbq{

  var mm = new file_move()

  var local_file = "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/staging_temp/bigdata/prod/test/thamo/bq_to_sftp_zip_move/spark_test/"

  val credentialsFile = "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/restricted/bigdata/dev/keystores/gcp/dev_gold_core/svc-dev-nexus-elt-bigdata-c1449cf1f89c.json"

  val tableid = "dev-gold-core.it_dms_customer.club_central_return_tdmkrtn"

  val df = spark.read.format("bigquery").option("credentialsFile",credentialsFile).option("viewsEnabled", "true").option("table",tableid).load()

  val format = DateTimeFormatter.ofPattern("yyyyMMdd")
  var date = LocalDate.now().minusDays(2).format(format)

  var csv_path = f"${local_file}Ecom_${date}1400N"

  df.write.format("csv").save(csv_path)

  var flag = mm.make_zip(csv_path)

  if(flag == 1){
    val sftpHost = "PWSFTP01.classic.pchad.com"
    val sftpUsername = "spectmims"
    val sftpPassword = "Fall2016"
    val cdpath = "/Spectrum_MIMS_Product_Views/test2/"
    val localFilePath = f"${csv_path}/part-00000-286e5b8d-08d6-4793-b532-8b212b3f3f62-c000.csv"   
    val sftpFilePath = "/Spectrum_MIMS_Product_Views/test2/part-00000-c11d996e-a697-4664-adc2-fb1d276a0fac-c000.csv" 

    var flag = mm.migrate(sftpHost= sftpHost, sftpUsername= sftpUsername, sftpPassword= sftpPassword, sftpFilePath= sftpFilePath, localFilePath= localFilePath, cdpath= cdpath)

    println(flag)

  }
  else{
    println("Zip not completed there is an error..")
  }

}


/*

dev-gold-core.it_dms_customer.club_central_return_tdmkrtn


val df = spark.read.format("bigquery").option("credentialsFile","/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/restricted/bigdata/dev/keystores/gcp/dev_gold_core/svc-dev-nexus-elt-bigdata-c1449cf1f89c.json").option("project","dev-gold-core").option("dataset","it_dms_customer").option("table","club_central_return_tdmkrtn").load()


var local_file = "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/staging_temp/bigdata/prod/test/thamo/bq_to_sftp_zip_move/spark_test/"

val format = DateTimeFormatter.ofPattern("yyyyMMdd")
var date = LocalDate.now().minusDays(2).format(format)

var csv_path = f"${local_file}Ecom_${date}1400N"

df.write.format("csv").save(csv_path)

-- var mv = f"${csv_path}/part-00000-286e5b8d-08d6-4793-b532-8b212b3f3f62-c000.csv"
-- var sftppath = "/Spectrum_MIMS_Product_Views/test2/part-00000-c11d996e-a697-4664-adc2-fb1d276a0fac-c000.csv"


val sftpHost = "PWSFTP01.classic.pchad.com"
val sftpUsername = "spectmims"
val sftpPassword = "Fall2016"
val sftpPort = 22
val localFilePath = f"${csv_path}/part-00000-286e5b8d-08d6-4793-b532-8b212b3f3f62-c000.csv"   
val sftpFilePath = "/Spectrum_MIMS_Product_Views/test2/part-00000-c11d996e-a697-4664-adc2-fb1d276a0fac-c000.csv" 


val jsch = new JSch()
val session = jsch.getSession(sftpUsername, sftpHost, sftpPort)
session.setPassword(sftpPassword)
session.setConfig("StrictHostKeyChecking", "no")
session.connect()

val channel = session.openChannel("sftp").asInstanceOf[ChannelSftp]
channel.connect()

channel.cd("/Spectrum_MIMS_Product_Views/test2/")

channel.put(localFilePath, sftpFilePath)

*/