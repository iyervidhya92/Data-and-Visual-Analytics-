package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;
import java.lang.Object;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class Q1a {

	  public static class Q1aMapper
	       extends Mapper<Object, Text, IntWritable, IntWritable>{

	    private IntWritable outgoing_node = new IntWritable();
	    private IntWritable weight = new IntWritable();

	    public void map(Object key, Text value, Context context
	                    ) throws IOException, InterruptedException {

	      StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
	      
	      while (itr.hasMoreTokens()) {
	        String tokens[] = itr.nextToken().split("\t");
	        if (tokens.length > 1){	  
		  outgoing_node.set(Integer.parseInt(tokens[0]));
	          weight.set(Integer.parseInt(tokens[2]));
	          context.write(outgoing_node, weight);
	        }
	      }
	    }
	  }

	  public static class Q1aReducer
	       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
	    private IntWritable result = new IntWritable();

	    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context
	                       ) throws IOException, InterruptedException {
	      int max = values.iterator().next().get();
	      for (IntWritable value : values) {
	        if(value.get() > max) max = value.get();
	      }
	      result.set(max);
	      context.write(key, result);
	    }
	  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1a");

    /* TO DO: Needs to be implemented */
    job.setJarByClass(Q1a.class);
    job.setMapperClass(Q1aMapper.class);
    job.setCombinerClass(Q1aReducer.class);
    job.setReducerClass(Q1aReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}

 
