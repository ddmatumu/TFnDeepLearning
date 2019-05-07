# -*- coding: utf-8 -*-
#prediction using model.
#process--->1.load data(X:list of lint,y:int). 2.create session. 3.feed data. 4.predict
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import tensorflow as tf
import numpy as np
from a07_Transformer import  Transformer
from data_util_zhihu import load_data_predict,load_final_test_data,create_voabulary,create_voabulary_label
from tflearn.data_utils import pad_sequences #to_categorical
import os
import codecs

#configuration
FLAGS=tf.app.flags.FLAGS
tf.app.flags.DEFINE_integer("num_classes",1999+3,"number of label") #3 ADDITIONAL TOKEN: _GO,_END,_PAD
tf.app.flags.DEFINE_float("learning_rate",0.01,"learning rate")
tf.app.flags.DEFINE_integer("batch_size", 128, "Batch size for training/evaluating.") #批处理的大小 32-->128 #16
tf.app.flags.DEFINE_integer("decay_steps", 6000, "how many steps before decay learning rate.") #6000批处理的大小 32-->128
tf.app.flags.DEFINE_float("decay_rate", 1.0, "Rate of decay for learning rate.") #0.87一次衰减多少
tf.app.flags.DEFINE_string("ckpt_dir","checkpoint_transformer/","checkpoint location for the model")
tf.app.flags.DEFINE_integer("sequence_length",25,"max sentence length") #100-->25
tf.app.flags.DEFINE_integer("embed_size",512,"embedding size")
tf.app.flags.DEFINE_boolean("is_training",False,"is traning.true:tranining,false:testing/inference")
#tf.app.flags.DEFINE_string("cache_path","text_cnn_checkpoint/data_cache.pik","checkpoint location for the model")
#train-zhihu4-only-title-all.txt
tf.app.flags.DEFINE_string("traning_data_path","train-zhihu4-only-title-all.txt","path of traning data.") #O.K.train-zhihu4-only-title-all.txt-->training-data/test-zhihu4-only-title.txt--->'training-data/train-zhihu5-only-title-multilabel.txt'
tf.app.flags.DEFINE_string("word2vec_model_path","zhihu-word2vec-title-desc.bin-512","word2vec's vocabulary and vectors") #zhihu-word2vec.bin-100-->zhihu-word2vec-multilabel-minicount15.bin-100
tf.app.flags.DEFINE_boolean("multi_label_flag",True,"use multi label or single label.") #set this false. becase we are using it is a sequence of token here.
tf.app.flags.DEFINE_float("l2_lambda", 0.0001, "l2 regularization")
tf.app.flags.DEFINE_string("predict_target_file","checkpoint_transformer/zhihu_result_transformer.csv","target file path for final prediction")
tf.app.flags.DEFINE_string("predict_source_file",'test-zhihu-forpredict-title-desc-v6.txt',"target file path for final prediction") #test-zhihu-forpredict-v4only-title.txt
tf.app.flags.DEFINE_integer("decoder_sent_length",25,"length of decoder inputs")

tf.app.flags.DEFINE_integer("d_model",512,"hidden size")
tf.app.flags.DEFINE_integer("d_k",64,"hidden size")
tf.app.flags.DEFINE_integer("d_v",64,"hidden size")
tf.app.flags.DEFINE_integer("h",8,"hidden size")
tf.app.flags.DEFINE_integer("num_layer",1,"hidden size") #6
#1.load data(X:list of lint,y:int). 2.create session. 3.feed data. 4.training (5.validation) ,(6.prediction)
# 1.load data with vocabulary of words and labels
_GO="_GO"
_END="_END"
_PAD="_PAD"

def main(_):
    # 1.load data with vocabulary of words and labels
    vocabulary_word2index, vocabulary_index2word = create_voabulary(word2vec_model_path=FLAGS.word2vec_model_path,name_scope="transformer")  # simple='simple'
    vocab_size = len(vocabulary_word2index)
    print("transformer.vocab_size:", vocab_size)
    vocabulary_word2index_label, vocabulary_index2word_label = create_voabulary_label(name_scope="transformer",use_seq2seq=True)
    questionid_question_lists=load_final_test_data(FLAGS.predict_source_file)
    test= load_data_predict(vocabulary_word2index,vocabulary_word2index_label,questionid_question_lists)
    testX=[]
    question_id_list=[]
    for tuple in test:
        question_id,question_string_list=tuple
        question_id_list.append(question_id)
        testX.append(question_string_list)
    # 2.Data preprocessing: Sequence padding
    print("start padding....")
    testX2 = pad_sequences(testX, maxlen=FLAGS.sequence_length, value=0.)  # padding to max length
    print("end padding...")
   # 3.create session.
    config=tf.ConfigProto()
    config.gpu_options.allow_growth=True
    with tf.Session(config=config) as sess:
        # 4.Instantiate Model
        model=Transformer(FLAGS.num_classes, FLAGS.learning_rate, FLAGS.batch_size, FLAGS.decay_steps, FLAGS.decay_rate, FLAGS.sequence_length,
                 vocab_size, FLAGS.embed_size,FLAGS.d_model,FLAGS.d_k,FLAGS.d_v,FLAGS.h,FLAGS.num_layer,FLAGS.is_training,decoder_sent_length=FLAGS.decoder_sent_length,l2_lambda=FLAGS.l2_lambda)
        saver=tf.train.Saver()
        if os.path.exists(FLAGS.ckpt_dir+"checkpoint"):
            print("Restoring Variables from Checkpoint")
            saver.restore(sess,tf.train.latest_checkpoint(FLAGS.ckpt_dir))
        else:
            print("Can't find the checkpoint.going to stop")
            return
        # 5.feed data, to get logits
        number_of_training_data=len(testX2);print("number_of_training_data:",number_of_training_data)
        index=0
        predict_target_file_f = codecs.open(FLAGS.predict_target_file, 'a', 'utf8')
        #decoder_input=np.reshape(np.array([vocabulary_word2index_label[_GO]]+[vocabulary_word2index_label[_PAD]]*(FLAGS.decoder_sent_length-1)),[-1,FLAGS.decoder_sent_length])
        decoder_input=np.full((FLAGS.batch_size,FLAGS.decoder_sent_length),vocabulary_word2index_label[_PAD])
        decoder_input[:,0:1]=vocabulary_word2index_label[_GO] #set all values in first column to _GO
        for start, end in zip(range(0, number_of_training_data, FLAGS.batch_size),range(FLAGS.batch_size, number_of_training_data+1, FLAGS.batch_size)):
            predictions,logits=sess.run([model.predictions,model.logits],
                                        feed_dict={model.input_x:testX2[start:end],
                                                   model.decoder_input:decoder_input,
                                                   model.dropout_keep_prob:1
                                                   })
            ####################################################################################
            #for j in range(FLAGS.decoder_sent_length):
            #    predict = sess.run(model.predictions, #model.loss_val,--->loss, model.train_op
            #                        feed_dict={model.input_x:testX2[start:end],
            #                                   model.decoder_input:decoder_input,
            #                                   #model.input_y_label: input_y_label,
            #                                   model.dropout_keep_prob: 1.0,
            #                                   })
            #    decoder_input[:,j] = predict[:,j]
           ####################################################################################
            print("===============>",start,"predict:",predict)
            # 6. get lable using logtis
            for _,logit in enumerate(logits):
                predicted_labels=get_label_using_logits(logit,predictions,vocabulary_index2word_label,vocabulary_word2index_label)
                print(index," ;predicted_labels:",predicted_labels)
                # 7. write question id and labels to file system.
                write_question_id_with_labels(question_id_list[index],predicted_labels,predict_target_file_f)
                index=index+1
        predict_target_file_f.close()

def get_label_using_logits(logits, predictions,vocabulary_index2word_label,vocabulary_word2index_label, top_number=5):
    print("logits:",logits.shape) #(6, 2002)
    result_list=[]
    for i,row in enumerate(logits):
        #print("i,",i,"row:",row)
        if i!=len(logits)-1: #not include result from last column, which usually it should be <END> TOKEN.
            label=process_each_row_get_lable(row,vocabulary_index2word_label,vocabulary_word2index_label,result_list)
            result_list.append(label)
    return result_list

def process_each_row_get_lable(row,vocabulary_index2word_label,vocabulary_word2index_label,result_list):
    """
    :param row: it is a list.length is number of labels. e.g. 2002
    :param vocabulary_index2word_label
    :param result_list
    :return: a lable
    """
    label_list=list(np.argsort(row))
    label_list.reverse()
    #print("label_list:",label_list) # a list,length is number of labels.
    for i,index in enumerate(label_list): # if index is not exists, and not _PAD,_END, then it is the label we want.
        #print(i,"index:",index)
        flag1=vocabulary_index2word_label[index] not in result_list
        flag2=index!=vocabulary_word2index_label[_PAD]
        flag3=index!=vocabulary_word2index_label[_END]
        if flag1 and flag2 and flag3:
            #print("going to return ")
            return vocabulary_index2word_label[index]

# write question id and labels to file system.
def write_question_id_with_labels(question_id,labels_list,f):
    labels_string=",".join(labels_list)
    f.write(question_id+","+labels_string+"\n")

if __name__ == "__main__":
    tf.app.run()