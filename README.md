# Intro to Apache Beam (Under Construction)
This is a **Introduction to Apache Beam using Python** Repository. Here we will try to learn basics of Apache Beam to create **Batch** and **Streaming** pipelines. We will follow the learn step by step how to create a pipeline and what are the outputs after each phase. To establish that we will try to create simple pipeline to calculate the mean of two columns in a CSV file.

1. **Introduction to Apache Beam Model**
2. **Basic Codes**
3. **Batch Pipelines**
4. **Streaming Pipeplines**
5. **Conclusion**


## Motivation
For the last two years, I have been part of a great learning curve wherein I have upskilled myself to move into a Machine Learning and Cloud Computing. This project was practice project for all the learnings I have had. This is first of the many more to come. 
 

## Libraries/frameworks used

<b>Built with</b>
- [Apache Beam](https://beam.apache.org/documentation/programming-guide/)
- [Anaconda](https://www.anaconda.com/)
- [Python](https://www.python.org/)

## Code Example

```bash
    # clone this repo, removing the '-' to allow python imports:
    git clone https://github.com/adityasolanki205/Intro-to-Apache-Beam.git
    
    # Installing Virtual Environment
    pip install --upgrade virtualenv
    
    # Create virtual environment 
    virtualenv /path/to/directory
    
    # Activate a virtual environment
    . /path/to/directory/bin/activate
    
    # Install Apache Beam
    pip install apache-beam

    # Execute a Pipeline
    python -m Testing --input ./data/sp500.csv --output ./output/result.txt
    
```

## Apache Beam

Below are the steps to setup the enviroment and run the codes:

- **Introduction to Apache Beam Model**: Apache Beam is an open source model for creating both batch and streaming data-parallel processing pipelines. we will use python to build a program that defines the pipeline. The pipeline is then executed by one of Beam’s supported distributed processing back-ends like Google Cloud Dataflow.

    Beam is particularly useful for Embarrassingly Parallel data processing tasks, for Extract, Transform, and Load (ETL) tasks and pure data integration. These tasks are useful for moving data between different storage media and data sources, transforming data into a more desirable format, or loading data onto a new system.

    Everything in Apache beam are done in form of abstractions like pipelines, Pcollections and Ptransforms. Ptransforms are performed on Pcollections and this process is called pipeline.


- **Basic Codes**: Now we go step by step to learn Apache beam coding:
    
    i. ***Pipeline*** : The Pipeline abstraction encapsulates all the data and steps in your data processing task. Your Beam driver program typically starts by constructing a Pipeline object, and then using that object as the basis for creating the pipeline’s data sets as PCollections and its operations as Transforms.
      
    - ***Creating Pipeline*** :
      
      ```python
        import apache_beam as beam
        import apache_beam.options.pipeline_options as PipelineOptions

        with beam.Pipeline(options=PipelineOptions()) as p:
             pass
      ```
                 
    - ***Setting Pipeline options from command-line*** :
          
       ```python
         import apache_beam as beam
         from apache_beam.options.pipeline_options import PipelineOptions
         import argparse
            
         def run(argv=None, save_main_session=True):
            
             parser = argparse.ArgumentParser()
             parser.add_argument(
                  '--input',
                  dest='input',
                  default='../data/sp500.csv',
                  help='Input file to process.')
            
             parser.add_argument(
                  '--output',
                  dest='output',
                  default='../output/result.txt',
                  help='Output file to write results to.')
                
             known_args, pipeline_args = parser.parse_known_args(argv)
            
             options = PipelineOptions(pipeline_args)
                
             with beam.Pipeline(options=PipelineOptions()) as p:
                  pass
                
          if __name__ == '__main__':
             run()
       ```

     ii. ***Pcollection*** : The PCollection abstraction represents a potentially distributed, multi-element data set. You can think of a PCollection as “pipeline” data; Beam transforms use PCollection objects as inputs and outputs. As such, if you want to work with data in your pipeline, it must be in the form of a PCollection. 
    
    iii. ***Transform*** : Transforms are the operations in your pipeline, and provide a generic processing framework. You provide processing logic in the form of a function object (colloquially referred to as “user code”), and your user code is applied to each element of an input PCollection (or more than one PCollection). Types of transform functions are as follows:
    
    - ***ParDo*** : ParDo is a Beam transform for generic parallel processing. A ParDo transform considers each element in the input PCollection, performs some processing function (your user code) on that element, and emits zero, one, or multiple elements to an output PCollection. We will try to use this to create a SPLIT() function that will segregate the input CSV elements. Output saved from this is present with the name ****PARDO.txt****
         
       ```python
         class Split(beam.DoFn):
        
             def process(self, element):
              
                 Date,Open,High,Low,Close,Volume, AdjClose = element.split(',')
                 return [{
                         'Date': Date,
                         'Open': float(Open),
                         'Close': float(Close)
                         }]
            ...
            
         with beam.Pipeline(options=PipelineOptions()) as p:
            
             csv_lines = (p 
                          | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
                          | beam.ParDo(Split())
                          | beam.io.WriteToText(known_args.output))
       ```

    - ***GroupByKey*** : GroupByKey is a Beam transform for processing collections of key/value pairs. It’s a parallel reduction operation. The input to GroupByKey is a collection of key/value pairs that represents a multimap, where the collection contains multiple pairs that have the same key, but different values. Given such a collection, you use GroupByKey to collect all of the values associated with each unique key. We will try to use this to create a Singular output file containing all OPEN or CLOSE column values. Output saved from this is present with the name ****GroupByKey.txt****

       ```python
         class CollectOpen(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Open'])]
                 return result
            ...
            
         with beam.Pipeline(options=PipelineOptions()) as p:
            
             csv_lines = (p 
                          | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
                          | beam.ParDo(Split())
             open_col  = (csv_lines 
                          | beam.ParDo(CollectOpen()) 
                          | "Grouping Keys Open" >> beam.GroupByKey()
                          | beam.io.WriteToText(known_args.output))          
       ```
    - ***CoGroupByKey*** : CoGroupByKey performs a relational join of two or more key/value PCollections that have the same key type. Consider using CoGroupByKey if you have multiple data sets that provide information about related things. For Example we will combine the output of GroupByKey output from above into one key with the name ****CoGroupByKey.txt****

       ```python
         class CollectOpen(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Open'])]
                 return result
         class CollectClose(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Close'])]
                 return result
            ...
            
         with beam.Pipeline(options=PipelineOptions()) as p:
            
             csv_lines = (p 
                          | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
                          | beam.ParDo(Split())
             open_col  = (csv_lines 
                          | beam.ParDo(CollectOpen()) 
                          | "Grouping Keys Open" >> beam.GroupByKey()
                          )
             close_col =  (csv_lines 
                          | beam.ParDo(CollectClose())
                          | "Grouping Keys Close" >> beam.GroupByKey()
                          )
             output    = ( 
                         ({'Open'  : open_col, 
                          'Close'  : close_col} 
                          | beam.CoGroupByKey())
                          | beam.io.WriteToText(known_args.output)
                         )
       ```

    - ***Flatten*** : Flatten is a Beam transform for PCollection objects that store the same data type. Flatten merges multiple PCollection objects into a single logical PCollection. It returns a single PCollection that contains all of the elements in the PCollection objects in that tuple. Output saved from this is present with the name ****Flatten.txt****

       ```python
         class CollectOpen(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Open'])]
                 return result
         class CollectClose(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Close'])]
                 return result
            ...
            
         with beam.Pipeline(options=PipelineOptions()) as p:
            
             csv_lines =  (p 
                          | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
                          | beam.ParDo(Split())
             open_col  =  (csv_lines 
                          | beam.ParDo(CollectOpen()) 
                          | "Grouping Keys Open" >> beam.GroupByKey()
                          )
             close_col =  (csv_lines 
                          | beam.ParDo(CollectClose())
                          | "Grouping Keys Close" >> beam.GroupByKey()
                          )
             output =     ( (close_col, open_col)
                          | beam.Flatten()
                          | beam.io.WriteToText(known_args.output)
                          )
       ```
    - ***CombineValues*** : CombineValues accepts a function that takes an iterable of elements as an input, and combines them to return a single element. CombineValues expects a keyed PCollection of elements, where the value is an iterable of elements to be combined. Output saved from this is present with the name ****CombineValues.txt****

       ```python
         class CollectOpen(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Open'])]
                 return result
         class CollectClose(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Close'])]
                 return result
            ...
            
         with beam.Pipeline(options=PipelineOptions()) as p:
            
             csv_lines =  (p 
                          | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
                          | beam.ParDo(Split())
             open_col  =  (csv_lines 
                          | beam.ParDo(CollectOpen()) 
                          | "Grouping Keys Open" >> beam.GroupByKey()
                          )
             close_col =  (csv_lines 
                          | beam.ParDo(CollectClose())
                          | "Grouping Keys Close" >> beam.GroupByKey()
                          )
             output =     ( open_col
                          |'Sum' >> beam.CombineValues(sum) 
                          | beam.io.WriteToText(known_args.output)
                          )
       ```
    - ***MeanCombineFn*** : MeanCombineFn accepts a function that takes an iterable of elements as an input, and combines them to return a mean of the input. CombineValues expects a keyed PCollection of elements, where the value is an iterable of elements to be combined. Output saved from this is present with the name ****MeanCombineFn.txt****

       ```python
         class CollectOpen(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Open'])]
                 return result
         class CollectClose(beam.DoFn):
        
             def process(self, element):
                 result = [(1,element['Close'])]
                 return result
            ...
            
         with beam.Pipeline(options=PipelineOptions()) as p:
            
             csv_lines =  (p 
                          | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
                          | beam.ParDo(Split())
             open_col  =  (csv_lines 
                          | beam.ParDo(CollectOpen()) 
                          | "Grouping Keys Open" >> beam.GroupByKey()
                          )
             close_col =  (csv_lines 
                          | beam.ParDo(CollectClose())
                          | "Grouping Keys Close" >> beam.GroupByKey()
                          )
             mean_open =  ( open_col 
                          | "Calculating mean for open" >> beam.CombineValues(beam.combiners.MeanCombineFn())
                          | beam.io.WriteToText(known_args.output)
                          )
       ``` 
    iv. ***Pipeline I/O*** : When you create a pipeline, you often need to read data from some external source, such as a file or a database. Likewise, you may want your pipeline to output its result data to an external storage system. Beam provides read and write transforms for a number of common data storage types. Most commonly used transforms are stated below:
    
    - ***ReadFromText*** : Read transforms read data from an external source and return a PCollection representation of the data for use by your pipeline. 
    
       ```python
            with beam.Pipeline(options=PipelineOptions()) as p:
                csv_lines =  (p | beam.io.ReadFromText(known_args.input,  skip_header_lines = 1) 
       ``` 
       
    - ***WriteToText*** : Write transforms write the data in a PCollection to an external data source. You will most often use write transforms at the end of your pipeline to output your pipeline’s final results. 
    
       ```python
            with beam.Pipeline(options=PipelineOptions()) as p:
                output =  (csv_lines | beam.io.WriteToText(known_args.output) 
       ```
       
    v. ***Schemas*** : Often records have a nested structure. A nested structure occurs when a field itself has subfields so the type of the field itself has a schema. Fields that are array or map types is also a common feature of these structured records. For example Transaction 
    
        | Field Name  | Field Name |
        | ----------- | ----------- |
        | Bank      | String       |
        | purchaseAmount   | Double        |
    
       
## How to use?
To test the code we need to do the following:

    1. Copy the german.data in the current folder
    
    2. Open the 'German credit.ipynb'
    
    3. Run all the cells
    
## Repository Content

    1. German Credit.ipynb

    2. German Credit.html
    
    3. German Credit-Tensorflow.ipynb

    2. German Credit-Tensorflow.html
    
    3. german.data    
    
    4. german.data-numeric
    
    5. german.doc
    

## Credits
1. Akash Nimare's [README.md](https://gist.github.com/akashnimare/7b065c12d9750578de8e705fb4771d2f#file-readme-md)
2. [Machine Learning Mastery](https://machinelearningmastery.com/imbalanced-classification-of-good-and-bad-credit/)
