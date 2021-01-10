#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class Split(beam.DoFn):
    def process(self, element):
        Date,Open,High,Low,Close,Volume, AdjClose = element.split(',')
        return [{
            'Date': Date,
            'Open': float(Open),
            'Close': float(Close)
        }]
    
class CollectOpen(beam.DoFn):
    def process(self, element):
        result = [(1, element['Open'])]
        return result
    
class CollectClose(beam.DoFn):
    def process(self, element):
        result = [(1, element['Close'])]
        return result
    
class MyOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input',
                             help='Input for the pipeline',
                             default='./data/'
                           )
        parser.add_argument('--output',
                            help='Output for the pipeline',
                            default='./output/'
                            )
input_filename = "./data/sp500.csv"
output_filename = "./output/result.txt"
options = PipelineOptions()
with beam.Pipeline(options=options) as p:
    csv_lines = (p | beam.io.ReadFromText(input_filename, skip_header_lines = 1) | beam.ParDo(Split())
              )
    mean_open = ( csv_lines | 
                  beam.ParDo(CollectOpen())    | 
                  "Grouping Keys Open" >> beam.GroupByKey() | 
                  "Calculating mean for open" >> beam.CombineValues(beam.combiners.MeanCombineFn())
                )
    mean_close = ( csv_lines | 
                   beam.ParDo(CollectClose())  |
                   "Grouping keys Close" >> beam.GroupByKey() |
                   "Calculating mean for Close" >> beam.CombineValues(beam.combiners.MeanCombineFn())
                )
    output = ( {'Mean Open' : mean_open,
                'Mean Close' : mean_close
               } 
              | beam.CoGroupByKey()
              | beam.io.WriteToText(output_filename)
            ) 
                

