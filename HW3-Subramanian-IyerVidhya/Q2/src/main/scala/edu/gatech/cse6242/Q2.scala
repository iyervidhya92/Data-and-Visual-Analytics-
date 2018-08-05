package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._

object Q2 {

	def main(args: Array[String]) {
    	val sc = new SparkContext(new SparkConf().setAppName("Q2"))
    	
		val sqlContext = new SQLContext(sc)
		import sqlContext.implicits._

    	// read the file
    	    val file = sc.textFile("hdfs://localhost:8020" + args(0))
			val graph = file.map(lines => lines.split("\t")).map(arrays=>(arrays(0),arrays(1), arrays(2).toInt)).toDF("src", "tgt", "weight")

			val filtered = graph.filter(graph("weight") >= 10);
			val src = filtered.groupBy("src").agg(avg("weight")).withColumnRenamed("avg(weight)", "sourceWeight");
			val tgt = filtered.groupBy("tgt").agg(avg("weight")).withColumnRenamed("avg(weight)", "targetWeight");

			val joined_df = src.join(tgt, src("src") === tgt("tgt"), "fullouter");
			val temp = joined_df.na.fill(0.0, Seq("sourceWeight"));
			val joined = temp.na.fill(0.0, Seq("targetWeight"));

			val myExpression = "sourceWeight-targetWeight";
			val weightDiff = List(col("sourceWeight"),col("targetWeight"))
			val output = joined.withColumn("diff", weightDiff.reduce(_ - _));

			val weights = output.select(output("tgt"), output("diff"));
			weights.map(x => x.mkString("\t")).saveAsTextFile("hdfs://localhost:8020" + args(1));
  	}
}
