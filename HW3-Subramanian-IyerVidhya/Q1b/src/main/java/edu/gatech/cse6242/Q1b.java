package edu.gatech.cse6242;
 
import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.lang.InterruptedException;
 
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
 
public class Q1b {
 
    public static class FileKey implements Writable, WritableComparable<FileKey> {
 
        private int receiver;
        private int sender;
        private int weight;
 
        public FileKey() {
        }
 
        public FileKey(int receiver, int sender, int weight) {
            this.receiver = receiver;
            this.sender = sender;
            this.weight = weight;
        }
 
        public void set(int receiver, int sender, int weight) {
            this.receiver = receiver;
            this.sender = sender;
            this.weight = weight;
        }
 
        
        public int getReceiver() {
            return this.receiver;
        }
        
        public int getSender() {
            return this.sender;
        }
 
        public int getWeight() {
            return this.weight;
        }
 
        @Override
        public void readFields(DataInput in) throws IOException {
            this.receiver = in.readInt();
            this.sender = in.readInt();
            this.weight = in.readInt();
        }
 
        @Override
        public void write(DataOutput out) throws IOException {
 
            out.writeInt(this.receiver);
            out.writeInt(this.sender);
            out.writeInt(this.weight);
        }
 
        @Override
        public int compareTo(FileKey other) {
            if (this.receiver != other.receiver) {
                return Integer.compare(this.receiver,other.receiver);
            } else if (this.weight != other.weight) {
                return -Integer.compare(this.weight,other.weight);
            } else {
                return Integer.compare(this.sender,other.sender);
            }
        }
 
    }
 
    public static class Q1bMapper extends Mapper<Object, Text, FileKey, IntWritable> {
    	 
        private FileKey key1 = new FileKey(0,0,0);
        private IntWritable node = new IntWritable(0);
 
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] values = value.toString().split("\\t");
            int receiver = Integer.parseInt(values[1]);
            int sender = Integer.parseInt(values[0]);
            int weight = Integer.parseInt(values[2]);
            node.set(sender);
            key1.set(receiver,sender,weight);
            context.write(key1,node);
        }
    }
 
    public static class Q1bReducer extends Reducer<FileKey,IntWritable,IntWritable,IntWritable> {
        private IntWritable receiver = new IntWritable();
        private IntWritable maxSender = new IntWritable();
 
        public void reduce(FileKey key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
 
            receiver.set(key.getReceiver());
            maxSender.set(key.getSender());
            context.write(receiver,maxSender);
        }
    }
 
    public static class Q1bGroupingComparator extends WritableComparator {
       
        protected Q1bGroupingComparator() {
            super(FileKey.class, true);
        }
 
        @Override
        public int compare(WritableComparable tp1, WritableComparable tp2) {
            FileKey fileKey = (FileKey) tp1;
            FileKey fileKey2 = (FileKey) tp2;
            return Integer.compare(fileKey.getReceiver(),fileKey2.getReceiver());
        }
    }
 
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Q1b");
 
        job.setJarByClass(Q1b.class);
        job.setJobName("highest sender");
        job.setOutputKeyClass(FileKey.class);
        job.setOutputValueClass(IntWritable.class);
        job.setMapperClass(Q1bMapper.class);
        job.setGroupingComparatorClass(Q1bGroupingComparator.class);
        job.setReducerClass(Q1bReducer.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}