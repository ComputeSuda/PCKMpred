from keras import layers
from keras import backend as K


def attention_3d_block_v2(inputs, mode, SINGLE_ATTENTION_VECTOR=False):
    # inputs.shape = (batch_size, time_steps, input_dim)
    TIME_STEPS = inputs.shape[1]
    input_dim = inputs.shape[2]

    # Attention mechanism on time steps
    if mode == 'step':
        a = layers.Permute((2, 1))(inputs)  # (None, 56, 11)
        a = layers.Reshape((input_dim, TIME_STEPS))(
            a)  # this line is not useful. It's just to know which dimension is what. # (None, 56, 11)
        a = layers.Dense(TIME_STEPS, activation='softmax')(a)  # (None, 56, 11)
        if SINGLE_ATTENTION_VECTOR:  # SINGLE_ATTENTION_VECTOR=True, all features share a weight，If = False, each dimension will have a separate weight
            a = layers.Lambda(lambda x: K.mean(x, axis=1))(a)
            a = layers.RepeatVector(input_dim)(a)  # (None, 56, 11)
        a_probs = layers.Permute((2, 1), name='attention_vec')(a)
        output_attention_mul = layers.Multiply()([inputs, a_probs])  # (None, 11, 56)
    # outputs = K.sum(output_attention_mul, axis=1)    # (None, 56)

    # Attention mechanism on features
    if mode == 'feature':
        a = inputs
        a = layers.Dense(input_dim, activation='softmax')(a)  # (None, 11, 56)
        if SINGLE_ATTENTION_VECTOR:  # True: all features share a weight
            a = layers.Lambda(lambda x: K.mean(x, axis=1))(a)  # (None, 56)
            a = layers.RepeatVector(TIME_STEPS)(a)  # (None, 11, 56)
        a_probs = a
        output_attention_mul = layers.Multiply()([inputs, a_probs])  # (None, 11, 56)
        output_attention_mul = K.sum(output_attention_mul, axis=1)

    return output_attention_mul