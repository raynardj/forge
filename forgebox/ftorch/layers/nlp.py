from torch import nn
import torch

class SublayerConnection(nn.Module):
    def __init__(self ,size ,dropout_ratio):
        """
        A residual connection followed by a layer norm
        size: feature number, for layer norm
        dropout_ratio:
        """
        super(SublayerConnection ,self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self ,x, sublayer):
        """
        x: input tensor
        sublayer: layer/network module
        """
        return x+ self.dropout(sublayer(self.norm(x)))


class Attention(nn.Module):
    """
    Compute "Scaled Dot Product Attention"
    """

    def forward(self, query, key, value, mask=None, dropout=None):
        scores = torch.matmul(query, key.transpose(-2, -1)) \
                 / math.sqrt(query.size(-1))  # regulize the scale down

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        p_attn = F.softmax(scores, dim=-1)  # usually the seq length is the last dim

        return torch.matmul(p_attn, value), p_attn


class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout_ratio=0.1, ):
        """
        Increase an extra dimension(heads) to increase more latent space
        h: attn heads
        d_model: d_k(number of heads) * h
        dropout_ratio: float, default 0.1
        """
        super().__init__()
        assert d_model % h == 0, "d_model can be devided by h"

        self.d_k = d_model // h
        self.h = h

        # Linear Layers
        self.linear_q = nn.Linear(d_model, d_model)
        self.linear_k = nn.Linear(d_model, d_model)
        self.linear_v = nn.Linear(d_model, d_model)
        self.linear_output = nn.Linear(d_model, d_model)

        self.attention = Attention()
        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self, query, key, value, mask=None):
        bs = query.size(0)
        # Linear Project in batch from d_model => h,seq_len,d_k
        query = self.linear_project(self.linear_q, query)
        key = self.linear_project(self.linear_k, key)
        value = self.linear_project(self.linear_v, value)

        # apply attentions to all project vectors
        x, attn = self.attention(query, key, value, mask=mask, dropout=self.dropout)

        #
        x = x.transpose(1, 2).contiguous().view(bs, -1, self.h * self.d_k)
        return self.linear_output(x)  # outputsize: bs, seq_len, d_model

    def linear_project(self, layer, x):
        """
        Increase the dimension: hidden size => head numbers * k
        output shape: bs, num_of_heads, sequence length, dimension under each head
        """
        bs = x.size(0)
        return layer(x).view(bs, -1, self.h, self.d_k).transpose(1, 2)


class FFN(nn.Module):
    def __init__(self, d_model, hs, dropout_ratio=0.1, activation=nn.ReLU):
        """
        Feed forward network, with layer norm
        """
        super().__init__()
        self.l1 = nn.Linear(d_model, hs)
        self.l2 = nn.Linear(hs, d_model)
        self.dropout = nn.Dropout(dropout_ratio)
        self.activation = activation()

    def forward(self, x):
        x = self.l1(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.l2(x)
        return x


class TransformerBlock(nn.Module):
    """
    Bidirectional Encoder  = Transformer(self-attention)
    Transformer = MultiHead_Attention + Feed Forward with sublayer connection
    """

    def __init__(self, hidden, attn_heads, feed_forward_hidden, dropout_ratio):
        super().__init__()
        self.attention = MultiHeadedAttention(h=attn_heads, d_model=hidden)
        self.FFN = FFN(d_model=hidden, hs=feed_forward_hidden, dropout_ratio=dropout_ratio)

        self.input_block = SublayerConnection(hidden, dropout_ratio=dropout_ratio)
        self.output_block = SublayerConnection(hidden, dropout_ratio=dropout_ratio)
        self.dropout = nn.Dropout(dropout_ratio)

    def forward(self, x, mask):
        x = self.input_block(x, lambda _x: self.attention(_x, _x, _x, mask=mask))
        x = self.output_block(x, self.FFN)
        return self.dropout(x)
