# 参数 --input_file=./data/tune.txt --input_format=wikisplit --output_tfrecord=./output/tune.tf_record --label_map_file=./output/label_map.txt --vocab_file=./model/RoBERTa-tiny-clue/vocab.txt --max_seq_length=40 --output_arbitrary_targets_for_infeasible_examples=false
# 参数 --input_file=./data/train.txt --input_format=wikisplit --output_tfrecord=./output/train.tf_record --label_map_file=./output/label_map.txt --vocab_file=./model/RoBERTa-tiny-clue/vocab.txt --max_seq_length=40  --output_arbitrary_targets_for_infeasible_examples=false
from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

from typing import Text

from absl import app
from absl import flags
from absl import logging

import bert_example
import tagging_converter
import utils

import tensorflow as tf
from curLine_file import curLine

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'input_file', None,
    'Path to the input file containing examples to be converted to '
    'tf.Examples.')
flags.DEFINE_enum(
    'input_format', None, ['wikisplit', 'discofuse'],
    'Format which indicates how to parse the input_file.')
flags.DEFINE_string('output_tfrecord', None,
                    'Path to the resulting TFRecord file.')
flags.DEFINE_string(
    'label_map_file', None,
    'Path to the label map file. Either a JSON file ending with ".json", that '
    'maps each possible tag to an ID, or a text file that has one tag per '
    'line.')
flags.DEFINE_string('vocab_file', None, 'Path to the BERT vocabulary file.')
flags.DEFINE_integer('max_seq_length', 128, 'Maximum sequence length.')
flags.DEFINE_bool(
    'do_lower_case', False,
    'Whether to lower case the input text. Should be True for uncased '
    'models and False for cased models.')
flags.DEFINE_bool('enable_swap_tag', True, 'Whether to enable the SWAP tag.')
flags.DEFINE_bool(
    'output_arbitrary_targets_for_infeasible_examples', False,
    'Set this to True when preprocessing the development set. Determines '
    'whether to output a TF example also for sources that can not be converted '
    'to target via the available tagging operations. In these cases, the '
    'target ids will correspond to the tag sequence KEEP-DELETE-KEEP-DELETE... '
    'which should be very unlikely to be predicted by chance. This will be '
    'useful for getting more accurate eval scores during training.')


def _write_example_count(count: int) -> Text:
    """Saves the number of converted examples to a file.

    This count is used when determining the number of training steps.

    Args:
      count: The number of converted examples.

    Returns:
      The filename to which the count is saved.
    """
    count_fname = FLAGS.output_tfrecord + '.num_examples.txt'
    with tf.io.gfile.GFile(count_fname, 'w') as count_writer:
        count_writer.write(str(count))
    return count_fname


def main(argv):
    if len(argv) > 1:
        raise app.UsageError('Too many command-line arguments.')
    flags.mark_flag_as_required('input_file')
    flags.mark_flag_as_required('input_format')
    flags.mark_flag_as_required('output_tfrecord')
    flags.mark_flag_as_required('label_map_file')
    flags.mark_flag_as_required('vocab_file')

    label_map = utils.read_label_map(FLAGS.label_map_file)
    converter = tagging_converter.TaggingConverter(
        tagging_converter.get_phrase_vocabulary_from_label_map(label_map),  # phrase_vocabulary  set
        FLAGS.enable_swap_tag)
    # print(curLine(), len(label_map), "label_map:", label_map, converter._max_added_phrase_length)
    builder = bert_example.BertExampleBuilder(label_map, FLAGS.vocab_file,
                                              FLAGS.max_seq_length,
                                              FLAGS.do_lower_case, converter)

    num_converted = 0
    with tf.io.TFRecordWriter(FLAGS.output_tfrecord) as writer:
        for i, (sources, target) in enumerate(utils.yield_sources_and_targets(FLAGS.input_file, FLAGS.input_format)):
            logging.log_every_n(
                logging.INFO,
                f'{i} examples processed, {num_converted} converted to tf.Example.',
                10000)
            example = builder.build_bert_example(
                sources, target,
                FLAGS.output_arbitrary_targets_for_infeasible_examples)
            if example is None:
                continue  # 根据output_arbitrary_targets_for_infeasible_examples，不能转化的忽略或随机，如果随机也会加到num_converted
            #print("example.to_tf_example().SerializeToString()",example.to_tf_example().SerializeToString())
            writer.write(example.to_tf_example().SerializeToString())
            num_converted += 1
    logging.info(f'Done. {num_converted} examples converted to tf.Example.')
    count_fname = _write_example_count(num_converted)
    logging.info(f'Wrote:\n{FLAGS.output_tfrecord}\n{count_fname}')


if __name__ == '__main__':
    app.run(main)
