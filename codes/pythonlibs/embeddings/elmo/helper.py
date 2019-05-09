import tensorflow as tf
import tensorflow_hub as hub
import numpy as np


def get_elmo_embeddings_layer(input_tensor, trainable=False):

    elmo = hub.Module("https://tfhub.dev/google/elmo/2", trainable=trainable)
    embeddings = elmo(
        inputs=input_tensor,
        signature='default',
        as_dict=True
        )['default']

    return embeddings


def _save_to_file(vctr_list, fname):
    vctrs = np.vstack(vctr_list)
    np.save(fname, vctrs)
    return vctrs

def transform_imdb_dataset(session, input_ph, elmo_emb_layer, records, batch_size, load=False, npy_path=None):
    '''
    Makes the provided recods pass through ELMo, getting the compressed representations for them.
    A 'load' option allow to instead load a pre-processed dataset from the filesystem. In this case a path for the dataset must be provided.
    In case of loading the returned dataset will not correspond the the one provided as input, but rather to the one saved on the hard drive.
    
    '''

    if not load:
        batches = int(records.shape[0] / batch_size)
        
        output = []
        
        for i, b in enumerate(range(batches)):
            ids = (b * batch_size, min([((b + 1) * batch_size), len(records)]))
            
            if i % 100 == 0 and len(output) > 0:
                print('Record: {}'.format(i))

                _save_to_file(output, npy_path)

            txts = records[ids[0]: ids[1]].reshape(-1)

            results = session.run([elmo_emb_layer],
                                feed_dict={
                                    input_ph: txts
                               })
                
            
            curr = results[0].reshape(batch_size, -1)

            output.append(curr.astype('float16'))

            
        vctrs = _save_to_file(output, npy_path)
            
        return vctrs

    else:
        assert npy_path is not None
        
        vctrs = np.load(f'{npy_path}')
        
        return vctrs


def loss_pass(feeds, batch_size, sess, loss, train_op=None, log=False):
    '''
    
    :param feeds feed dictionary {tensor: records}. For every provided tensor, its corresponding dataset will be splitted by batch size and fed to the model
    '''
    operations = [loss]
    if train_op is not None:
        operations.append(train_op)

    len_feeds = feeds[list(feeds.keys())[0]].shape[0]

    loss_acc = 0
    batches = int(len_feeds / batch_size)
    for b in range(batches):
        ids = (b * batch_size, min([((b + 1) * batch_size), len_feeds]))

        feeds_ = {k: feeds[k][ids[0]:ids[1]] for k in feeds.keys()}
        
        results = sess.run(operations,
                           feed_dict=feeds_
                           )

        loss_value = np.mean(results[0])

        loss_acc = loss_acc + loss_value

        if log:
            print('Batch: {:>6}/{:<6} Loss Value: {}'.format(b + 1, batches, loss_value))

    res_loss = loss_acc / batches

    return res_loss






