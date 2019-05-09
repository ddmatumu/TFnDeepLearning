import bert.run_classifier as run_classifier
import bert.tokenization as tokenization
import bert.modeling as modeling
import os
import tensorflow as tf
import numpy as np









LEARNING_RATE = 2e-5
WARMUP_PROPORTION = 0.1
MAX_SEQ_LENGTH = 128
SAVE_CHECKPOINTS_STEPS = 1000 
ITERATIONS_PER_LOOP = 1000
NUM_TPU_CORES = 8


        


def create_bert_examples(lines, set_type, labels=None):
#Generate data for the BERT model
    guid = f'{set_type}'
    examples = []
    if guid == 'train':
        for line, label in zip(lines, labels):
            text_a = line
            label = str(label)
            examples.append(
              run_classifier.InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
    else:
        for line in lines:
            text_a = line
            label = '0'
            examples.append(
              run_classifier.InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
    return examples


def imdb_to_bert_features(records, max_seq_length, repo_path, train=True):

    repo = repo_path
    model = 'uncased_L-12_H-768_A-12'
    
    
    pretrained_dir = f'{repo}/{model}'

    vocab_file = os.path.join(pretrained_dir, 'vocab.txt')
    do_lower_case = model.startswith('uncased')
    
    
    records_txt_v, records_lbl_v = records[:, 0], records[:, 1:]

    get_id = lambda v: str(np.argmax(v))
    get_str = lambda v: str(v)

    records_txt = list(map(get_str, records_txt_v))

    records_lbl = list(map(get_id, records_lbl_v))

    label_list = ['0', '1']

    tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file, do_lower_case=do_lower_case)
    
    guid = 'train' if train else 'test'
    
    records_examples = create_bert_examples(records_txt, guid, labels=records_lbl)
    records_features = run_classifier.convert_examples_to_features(records_examples, label_list, max_seq_length, tokenizer)
    
    return records_features



def get_tpu_estimator(model_dir, train_epochs, size_train_set, batch_size, num_labels, classifier_model_fn):

    bert_pretrained_dir = f'{model_dir}/uncased_L-12_H-768_A-12'
    config_file = os.path.join(bert_pretrained_dir, 'bert_config.json')
    init_checkpoint = os.path.join(bert_pretrained_dir, 'bert_model.ckpt')
    
    
    tpu_cluster_resolver = None
    
    run_config = tf.contrib.tpu.RunConfig(
        cluster=tpu_cluster_resolver,
        model_dir=model_dir,
        save_checkpoints_steps=SAVE_CHECKPOINTS_STEPS,
        tpu_config=tf.contrib.tpu.TPUConfig(
            iterations_per_loop=ITERATIONS_PER_LOOP,
            num_shards=NUM_TPU_CORES,
            per_host_input_for_training=tf.contrib.tpu.InputPipelineConfig.PER_HOST_V2)
    )

    num_train_steps = int(size_train_set / batch_size * train_epochs)

    num_warmup_steps = int(num_train_steps * WARMUP_PROPORTION)

    model_fn = run_classifier.model_fn_builder(
        bert_config=modeling.BertConfig.from_json_file(config_file),
        num_labels=num_labels,
        init_checkpoint=init_checkpoint,
        learning_rate=LEARNING_RATE,
        num_train_steps=num_train_steps,
        num_warmup_steps=num_warmup_steps,
        use_tpu=False,  # If False training will fall on CPU or GPU, depending on what is available
        use_one_hot_embeddings=True,
        classifier_model_fn=classifier_model_fn)

    estimator = tf.contrib.tpu.TPUEstimator(
        use_tpu=False,  # If False training will fall on CPU or GPU, depending on what is available
        model_fn=model_fn,
        config=run_config,
        train_batch_size=batch_size,
        eval_batch_size=batch_size)

    return estimator