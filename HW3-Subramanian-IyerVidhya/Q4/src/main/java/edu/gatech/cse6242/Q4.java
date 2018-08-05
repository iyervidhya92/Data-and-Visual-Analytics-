package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.StringTokenizer;


public class Q4 {

  public static class Mapper_1
    extends Mapper<Object, Text, IntWritable, IntWritable>{

    private final static IntWritable one = new IntWritable(1);
    private final static IntWritable neg_one = new IntWritable(-1);    

    private IntWritable source = new IntWritable();
    private IntWritable target = new IntWritable();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
      while (itr.hasMoreTokens()) {
        String tokens[] = itr.nextToken().split("\t");
	if (tokens.length > 1){
	  source.set(Integer.parseInt(tokens[0]));
	  target.set(Integer.parseInt(tokens[1]));

      context.write(source, neg_one);
	  context.write(target, one);
	}
      }
    }
  }

  public static class Reducer_1
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context
                       ) throws IOException, InterruptedException {
      int total = 0;
      for (IntWritable value : values) {
        total = total + value.get();
      }
      result.set(total);
      context.write(key, result);
    }
  }

  public static class Mapper_2
    extends Mapper<Object, Text, IntWritable, IntWritable>{

    private final static IntWritable one = new IntWritable(1);
    private IntWritable node = new IntWritable();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
      while (itr.hasMoreTokens()) {
        String tokens[] = itr.nextToken().split("\t");
	if (tokens.length > 1){
          node.set(Integer.parseInt(tokens[1]));
          context.write(node, one);
        }
      }
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job1 = Job.getInstance(conf, "Q4");

    /* TODO: Needs to be implemented */
    job1.setJarByClass(Q4.class);
    job1.setMapperClass(Mapper_1.class);
    job1.setCombinerClass(Reducer_1.class);
    job1.setReducerClass(Reducer_1.class);
    job1.setOutputKeyClass(IntWritable.class);
    job1.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job1, new Path(args[0]));
    String outputTempDir = args[1]+"-1";
    FileOutputFormat.setOutputPath(job1, new Path(outputTempDir));

    job1.waitForCompletion(true);

    Job job2 = Job.getInstance(conf, "job2");

    job2.setJarByClass(Q4.class);
    job2.setMapperClass(Mapper_2.class);
    job2.setCombinerClass(Reducer_1.class);
    job2.setReducerClass(Reducer_1.class);
    job2.setOutputKeyClass(IntWritable.class);
    job2.setOutputValueClass(IntWritable.class);


    FileInputFormat.addInputPath(job2, new Path(outputTempDir));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }
}
