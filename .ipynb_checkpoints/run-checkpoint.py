#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import argparse

class Split(beam.DoFn):
    def process(self, element):
        Date,Open,High,Low,Close,Volume, AdjClose = element.split(',')
        return [{
            'Date':Date,
            'Open': float(Open),
            'Close': float(Close)
        }]

class ConvertDataType(beam.DoFn):
    def process(self, element):
        element['Open'] = float(element['Open']) if 'Open' in element else None
        element['Close'] = float(element['Close']) if 'Close' in element else None

        return [element]

class Collect_Open(beam.DoFn):
    def process(self, element):
        return [(1, element['Open'])]

class Collect_Close(beam.DoFn):
    def process(self, element):
        return [(1, element['Close'])]

#input_file = "./data/sp500.csv"
#output_file = "./output/run_pardo_result.txt"
def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
    '--input',
    dest='input')
    parser.add_argument(
    '--output',
    dest='output'
    )
    known_args, pipeline_args = parser.parse_known_args(argv)
    Options=PipelineOptions(pipeline_args)
    with beam.Pipeline(options=Options) as p:
        csv_lines_open = (p | 'Read for Open'>> beam.io.ReadFromText(known_args.input , skip_header_lines = 1))
        splitting_open = (csv_lines_open | 'Split Open' >> beam.ParDo(Split()))
        csv_lines_close = (p | 'Read for Close' >> beam.io.ReadFromText(known_args.input , skip_header_lines = 1))
        splitting_close = (csv_lines_close |'Split Close' >> beam.ParDo(Split()))
        #converted = (csv_lines_Close | beam.ParDo(ConvertDataType()))
        collecting_open = (splitting_open | 'Collecting open' >> beam.ParDo(Collect_Open()))
        collecting_close = (splitting_close | 'Collecting Close' >> beam.ParDo(Collect_Close()))
        
        addition_open = (collecting_open | 'Open' >> beam.combiners.Mean.PerKey())
        addition_close = (collecting_close | 'Close' >> beam.combiners.Mean.PerKey())
        together = ({'Open':addition_open,
                     'Close': addition_close}
                    | beam.CoGroupByKey()
                    )
        
        output = (together | beam.io.WriteToText(known_args.output))

if __name__ == '__main__':
    run()