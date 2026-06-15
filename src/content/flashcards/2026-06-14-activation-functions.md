---
title: "Activation Functions"
date: "2026-06-14"
description: ""
tags: ["deep-learning", "neural-networks", "ml"]
---

## First Principles

### What is an activation?

An activation function is the non-linear rule applied after a layer's linear computation.

For a layer:

$$
z = Wx + b
$$

$$
a = f(z)
$$

Where:

- `z` is the pre-activation or logit-like score.
- `f` is the activation function.
- `a` is the signal passed to the next layer.

The linear layer computes a score. The activation decides how that score should become signal.

### Why do we need activations?

Without activation functions, deep networks collapse into one linear transformation.

$$
W_3(W_2(W_1x)) = W'x
$$

Depth would add parameters, but not real expressive power.

Activation functions introduce non-linearity, which lets networks learn curves, thresholds, interactions, and hierarchical features.

This is the core point: linear layers mix information; activations bend the function.

### How should I think about activations?

Think of activations as gates.

Different gates pass information differently:

- Sigmoid: soft yes/no probability gate.
- Tanh: centered squashing gate.
- ReLU: hard positive-only gate.
- GELU / SiLU: smooth probabilistic gates.
- Softmax: competition gate across classes.

The activation shapes both the forward signal and the backward gradient.

### What are activations doing?

Hidden-layer activations mainly affect optimization and representation.

They answer:

- Can gradients flow?
- Does the layer keep useful signal?
- Does training stay stable?
- Does the architecture expect this activation?

Output activations mainly affect prediction meaning.

They answer:

- Is this a probability?
- Are classes mutually exclusive?
- Can multiple labels be true?
- Is the output bounded or unconstrained?

### How do activations affect gradients?

During backpropagation, each activation contributes a local derivative.

If:

$$
a = f(z)
$$

then gradients flowing backward are multiplied by:

$$
f'(z)
$$

This is why activation shape matters. If `f'(z)` is often near zero, gradients shrink. If it is stable, gradients flow more easily.

In practice, activation functions are not just forward transformations; they are also gradient filters.

### Why is saturation bad?

Saturation happens when large input ranges produce almost constant outputs.

Examples:

- Sigmoid saturates near `0` and `1`.
- Tanh saturates near `-1` and `1`.

In saturated regions, derivatives are close to zero. During backpropagation, multiplying by many tiny derivatives can make gradients vanish.

That is why saturating activations are usually poor hidden-layer defaults in very deep networks.

### What makes an activation good?

A useful activation usually balances:

- Non-linearity
- Stable gradients
- Cheap computation
- Good behavior near zero
- Good behavior for large positive and negative inputs
- Suitable output range
- Compatibility with the architecture

There is no universally best activation. The right question is: what behavior do I need here?

## Core Activations

### What are the key activations?

| Activation | Full form | Formula | Range |
| --- | --- | --- | --- |
| Sigmoid | Logistic sigmoid | $\sigma(x)=\frac{1}{1+e^{-x}}$ | `(0, 1)` |
| Tanh | Hyperbolic tangent | $\tanh(x)$ | `(-1, 1)` |
| ReLU | Rectified Linear Unit | $\max(0,x)$ | `[0, infinity)` |
| Leaky ReLU | Leaky Rectified Linear Unit | $x$ if $x>0$, else $\alpha x$ | `(-infinity, infinity)` (attenuated negative) |
| Softplus | Smooth ReLU-like function | $\log(1+e^x)$ | `(0, infinity)` |
| SiLU | Sigmoid Linear Unit | $x\sigma(x)$ | roughly `(-0.28, infinity)` |
| GELU | Gaussian Error Linear Unit | $x\Phi(x)$ | roughly `(-0.17, infinity)` |
| Softmax | Vector probability map | $\frac{e^{z_i}}{\sum_j e^{z_j}}$ | probabilities sum to `1` |

This table is the activation zoo in one card. Most practical decisions come from understanding the behavior, not memorizing every variant.

### Sigmoid: what matters?

Sigmoid maps any real number to `(0, 1)`.

$$
\sigma(x)=\frac{1}{1+e^{-x}}
$$

Its derivative is:

$$
\sigma'(x)=\sigma(x)(1-\sigma(x))
$$

Its maximum derivative is only `0.25`, and it saturates for large positive or negative inputs.

Use sigmoid for binary or independent probabilities. Avoid it as a default hidden-layer activation.

### Tanh: what matters?

Tanh maps values to `(-1, 1)` and is zero-centered.

$$
\tanh(x)=2\sigma(2x)-1
$$

Its derivative is:

$$
\frac{d}{dx}\tanh(x)=1-\tanh^2(x)
$$

Tanh is often better centered than sigmoid, but it still saturates.

Use it when bounded, symmetric output is useful, such as some recurrent states or action outputs scaled to `[-1, 1]`.

<svg viewBox="0 0 640 250" role="img" aria-labelledby="sigmoid-tanh-title" style="max-width:100%;height:auto;color:var(--text-color);">
  <title id="sigmoid-tanh-title">Sigmoid and tanh activation curves</title>
  <g fill="none" stroke="currentColor" stroke-opacity="0.22" stroke-width="1">
    <path d="M56 124H584"></path>
    <path d="M320 24V224"></path>
  </g>
  <path d="M56,124L68,124L80,124L92,123L104,123L116,123L128,123L140,123L152,122L164,121L176,121L188,120L200,118L212,117L224,115L236,112L248,109L260,105L272,101L284,96L296,91L308,85L320,79L332,72L344,66L356,61L368,56L380,52L392,48L404,45L416,42L428,40L440,39L452,37L464,36L476,36L488,35L500,35L512,34L524,34L536,34L548,34L560,33L572,33L584,33" fill="none" stroke="#3273dc" stroke-width="2.5"></path>
  <path d="M56,215L68,215L80,215L92,215L104,215L116,215L128,215L140,215L152,215L164,215L176,215L188,214L200,214L212,214L224,213L236,211L248,208L260,204L272,196L284,185L296,169L308,148L320,124L332,100L344,79L356,63L368,52L380,44L392,40L404,37L416,35L428,34L440,34L452,34L464,33L476,33L488,33L500,33 Bell,33 L512,33L524,33L536,33L548,33L560,33L572,33L584,33" fill="none" stroke="#8b6fcb" stroke-width="2.5"></path>
  <g font-family="Verdana, sans-serif" font-size="13">
    <text x="478" y="53" fill="#3273dc">sigmoid</text>
    <text x="430" y="82" fill="#8b6fcb">tanh</text>
    <text x="324" y="239" fill="currentColor" opacity="0.55">0</text>
  </g>
</svg>

### ReLU: what matters?

ReLU stands for Rectified Linear Unit.

$$
\operatorname{ReLU}(x)=\max(0,x)
$$

For positive inputs, its derivative is `1`. For negative inputs, its derivative is `0`.

That makes it cheap and good for gradient flow on the positive side.

Its weakness is that negative signal is killed completely, which can cause dead neurons.

### How does ReLU die, and how do we fix it?

A ReLU unit "dies" when an aggressive gradient update (often due to a high learning rate) shifts its weights such that the pre-activation $z$ is negative across the *entire* training dataset. 

Because $\operatorname{ReLU}'(x) = 0$ for all negative values, the gradient becomes zero, locking the weights permanently.

**Alternative Smooth & Leaky Cutoffs:**

| Activation | Core idea |
| --- | --- |
| **Leaky ReLU** | Leaky Rectified Linear Unit - Keep a small fixed negative slope (e.g., $\alpha = 0.01$) to guarantee gradient backprop. |
| **PReLU** | Parametric Rectified Linear Unit -Treat the negative slope $\alpha$ as a learnable parameter. |
| **ELU** | Exponential Linear Unit -Smoothly map negatives toward $-\alpha$ using exponentials to reduce noise susceptibility. |
| **SELU** | Scaled Exponential Linear Unit - Self-normalizing variant of ELU; requires LeCun initialization and alpha dropout. |

<svg viewBox="0 0 640 250" role="img" aria-labelledby="relu-family-title" style="max-width:100%;height:auto;color:var(--text-color);">
  <title id="relu-family-title">ReLU, Leaky ReLU, and Softplus curves</title>
  <g fill="none" stroke="currentColor" stroke-opacity="0.22" stroke-width="1">
    <path d="M56 192H584"></path>
    <path d="M320 24V224"></path>
  </g>
  <path d="M56,192L68,192L80,192L92,192L104,192L116,192L128,192L140,192L152,192L164,192L176,192L188,192L200,192L212,192L224,192L236,192L248,192L260,192L272,192L284,192L296,192L308,192L320,192L332,185L344,177L356,170L368,163L380,156L392,148L404,141L416,134L428,127L440,119L452,112L464,105L476,97L488,90L500,83L512,76L524,68L536,61L548,54L560,47L572,39L584,32" fill="none" stroke="currentColor" stroke-width="2.5"></path>
  <path d="M56,208L68,207L80,207L92,206L104,205L116,204L128,204L140,203L152,202L164,201L176,201L188,200L200,199L212,199L224,198L236,197L248,196L260,196L272,195L284,194L296,193L308,193L320,192L332,185L344,177L356,170L368,163L380,156L392,148L404,141L416,134L428,127L440,119L452,112L464,105L476,97L488,90L500,83L512,76L524,68L536,61L548,54L560,47L572,39L584,32" fill="none" stroke="#8b6fcb" stroke-width="2.2"></path>
  <path d="M56,191L68,191L80,191L92,191L104,191L116,190L128,190L140,189L152,189L164,188L176,188L188,187L200,186L212,185L224,184L236,182L248,180L260,178L272,176L284,174L296,171L308,168L320,164L332,160L344,156L356,152L368,147L380,142L392,137L404,131L416,125L428,119L440,113L452,107L464,100L476,94L488,87L500,80L512,74L524,67L536,60L548,53L560,46L572,38L584,31" fill="none" stroke="#3273dc" stroke-width="2.2"></path>
  <g font-family="Verdana, sans-serif" font-size="13">
    <text x="493" y="49" fill="currentColor">ReLU</text>
    <text x="384" y="184" fill="#8b6fcb">Leaky</text>
    <text x="360" y="136" fill="#3273dc">Softplus</text>
  </g>
</svg>

### Softplus: when is it useful?

Softplus is a smooth approximation to ReLU.

$$
\operatorname{Softplus}(x)=\log(1+e^x)
$$

For large positive inputs, it behaves like `x`. For large negative inputs, it approaches `0`.

It is useful when you need a completely smooth positive output, such as predicting variance, learning rates, scales, or physical parameters in Bayesian neural networks.

### SiLU / Swish: what matters?

SiLU stands for Sigmoid Linear Unit.

$$
\operatorname{SiLU}(x)=x\sigma(x)
$$

Swish is the generalized form:

$$
\operatorname{Swish}(x)=x\sigma(\beta x)
$$

When `beta = 1`, Swish is identical to SiLU.

The intuition: SiLU softly gates the input by its own sigmoid. It keeps large positive values, smoothly downweights negatives, and preserves some small negative signal to support gradient flow near zero.

### GELU: what matters?

GELU stands for Gaussian Error Linear Unit.

$$
\operatorname{GELU}(x)=x\Phi(x)
$$

Where `Phi(x)` is the standard normal cumulative distribution function (CDF).

GELU is like a smooth, probabilistic ReLU: instead of hard-clipping negatives based on sign, it softly gates values based on their value magnitude relative to a normal distribution. It is the gold standard default in Transformer MLP blocks.

### GELU approximation: why know it?

A common approximation is:

$$
\operatorname{GELU}(x) \approx 0.5x\left(1+\tanh\left(\sqrt{\frac{2}{\pi}}(x+0.044715x^3)\right)\right)
$$

This avoids computing the exact, computationally heavy normal CDF. You rarely implement this manually, but recognizing this formula prevents confusion when analyzing raw model source code.

## Softmax and Outputs

### Softmax: what is it?

Softmax turns a vector of logits into a valid probability distribution.

$$
\operatorname{softmax}(z_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
$$

Each output is positive, and all outputs sum to `1`.

Unlike sigmoid or ReLU, softmax is **not elementwise**. Each output score scales relative to every other logit in the vector.

### Softmax: what's the intuition?

Softmax makes classes compete.

Increasing one logit exponentially increases that class probability while crushing the relative probability of all other classes.

Use softmax when **exactly one** class can be correct.
- Digit classification
- Single-label classification
- Next-token prediction in LLMs
- Mutually exclusive categories

### What is Softmax Temperature Scaling?

Temperature scaling ($T$) shifts output distributions without altering classification rank.

$$
\operatorname{softmax}(z_i) = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}
$$

- **$T \to 0$ (Low Temp):** Amplifies differences; the largest logit dominates completely. Distribution approaches a hard `argmax` (highly deterministic).
- **$T > 1$ (High Temp):** Diminishes differences; flattens the distribution towards uniform probability (increases randomness/entropy in generation).

### Why max-shift softmax?

Exponentials cause extreme numerical overflow for large logits during computing.

Instead, production engines use:

$$
\operatorname{softmax}(z_i)=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}
$$

Where:

$$
m=\max_j z_j
$$

Subtracting the maximum constant value shifts the largest exponent to $e^0 = 1$, perfectly preserving mathematical probabilities while guaranteeing mathematical stability.

### Sigmoid or softmax?

Use sigmoid when outputs are independent. Use softmax when outputs compete.

| Situation | Activation |
| --- | --- |
| Is this email spam? | Sigmoid |
| Which digit is this? | Softmax |
| Which tags apply to this document? | Sigmoid per tag |
| What is the next token? | Softmax |
| Can this image be both indoor and blurry? | Sigmoid per label |

### What about regression outputs?

For unconstrained regression, use a linear output.

For constrained regression:

| Desired output | Activation |
| --- | --- |
| Any real number | Linear |
| Positive number | Softplus |
| Probability in `(0, 1)` | Sigmoid |
| Value in `(-1, 1)` | Tanh |
| Distribution over classes | Softmax |

Hidden layers can still use ReLU, GELU, SiLU, or another hidden activation.

### Output logits or probabilities?

Many standard frameworks combine the activation and cross-entropy loss into single integrated routines for extreme numerical precision.
- `Binary Cross-Entropy with Logits` combines sigmoid and BCE.
- `Cross Entropy Loss` combines softmax and Negative Log Likelihood.

This prevents taking the `log` of absolute zeros. Always verify if your loss function demands raw logits or activated values. Mixing them up breaks model learning silently.

## Modern Architecture Choices

### GLU: what is the idea?

GLU stands for Gated Linear Unit. A GLU splits a linear layer projection into two parallel paths: a values path and a control gate path.

$$
\operatorname{GLU}(x) = a \otimes \sigma(b)
$$

Where `a` and `b` are separate linear projections ($a = xW, b = xV$) and `\otimes` denotes elementwise multiplication. The model leverages the sigmoid path to explicitly filter information flow.

### SwiGLU: why care?

SwiGLU is a modern gated activation variant that replaces the basic sigmoid gate with a Swish/SiLU gate. In production Transformers (like LLaMA), it completely swaps out the classic FFN layer using three distinct weight matrices ($W, V, W_2$):

$$
\operatorname{SwiGLU}(x) = (\operatorname{SiLU}(xW) \otimes xV)W_2
$$

It maps the hidden dimension to an up-sampled gate path ($\operatorname{SiLU}(xW)$) and value path ($xV$), combines them elementwise, and projects back down via $W_2$.

### What is the training memory overhead of smooth activations?

Smooth activations (GELU, SiLU) incur significantly higher **activation memory footprints** during training than ReLU.

- **ReLU:** Requires storing only a single bit per activation for the backward pass (identifying if $x > 0$).
- **GELU/SiLU:** Require saving continuous, full-precision floating-point values of their inputs to calculate complex local derivatives during backpropagation. This trade-off requires advanced memory management like kernel fusions or activation checkpointing at scale.

### What's a sane hidden-layer default?

| Architecture / Use Case | Recommended Default | Trade-offs to Consider |
| --- | --- | --- |
| **Simple MLP** | ReLU | Fast, compute-efficient, ultra-low memory overhead. Risk of dead neurons. |
| **CNN** | ReLU, Leaky ReLU, or SiLU | SiLU assists edge detail retention but demands higher VRAM buffers. |
| **Transformer** | GELU, SiLU, or SwiGLU | Smooth gradients maximize attention optimization. Expensive compute. |
| **Recurrent Gates** | Sigmoid & Tanh | Explicitly required for stable state limits. |

When implementing complex networks, prioritize the default activation used by the baseline architecture.

<svg viewBox="0 0 640 250" role="img" aria-labelledby="modern-activations-title" style="max-width:100%;height:auto;color:var(--text-color);">
  <title id="modern-activations-title">ReLU, GELU, and SiLU curves</title>
  <g fill="none" stroke="currentColor" stroke-opacity="0.22" stroke-width="1">
    <path d="M56 199H584"></path>
    <path d="M320 24V224"></path>
  </g>
  <path d="M56,199L68,199L80,199L92,199L104,199L116,199L128,199L140,199L152,199L164,199L176,199L188,199L200,199L212,199L224,199L236,199L248,199L260,199L272,199L284,199L296,199L308,199L320,199L332,191L344,184L356,176L368,169L380,161L392,154L404,146L416,138L428,131L440,123L452,116L464,108L476,101L488,93L500,85L512,78L524,70L536,63L548,55L560,47L572,40L584,32" fill="none" stroke="currentColor" stroke-width="2.3"></path>
  <path d="M56,199L68,199L80,199L92,199L104,199L116,199L128,199L140,199L152,200L164,200L176,200L188,201L200,202L212,202L224,203L236,204L248,205L260,206L272,206L284,206L296,204L308,202L320,199L332,195L344,189L356,183L368,176L380,168L392,160L404,151L416,143L428,134L440,126L452,118L464,109L476,101L488,93L500,86L512,78L524,70L536,63L548,55L560,47L572,40L584,32" fill="none" stroke="#8b6fcb" stroke-width="2.3"></path>
  <path d="M56,202L68,202L80,203L92,203L104,204L116,205L128,205L140,206L152,207L164,207L176,208L188,209L200,210L212,210L224,210L236,211L248,210L260,210L272,209L284,207L296,205L308,202L320,199L332,195L344,190L356,185L368,179L380,172L392,165L404,158L416,150L428,142L440,134L452,126L464,117L476,109L488,101L500,92L512,84L524,76L536,68L548,59L560,51L572,43L584,35" fill="none" stroke="#0f766e" stroke-width="2.3"></path>
  <g font-family="Verdana, sans-serif" font-size="13">
    <text x="498" y="51" fill="currentColor">ReLU</text>
    <text x="408" y="125" fill="#8b6fcb">GELU</text>
    <text x="372" y="177" fill="#0f766e">SiLU</text>
  </g>
</svg>

### What's the takeaway?

Remember:
- Activations add non-linearity.
- Hidden activations shape learning dynamics; output activations shape prediction meaning.
- Saturating activations vanish gradients; dead ReLUs are caused by absolute mathematical lock out.
- ReLU is ultra-fast; GELU and SiLU are smooth, high-performing, memory-intensive defaults.
- Sigmoid scales independent features/probabilities; Softmax governs strict competition.

## PyTorch Implementation Details

### Module (`nn`) vs. Functional (`F`) activations?

PyTorch provides two ways to call activation functions: **Stateful Modules** (`torch.nn`) and **Stateless Functional calls** (`torch.nn.functional`).

| Approach | Code Example | When to use |
| --- | --- | --- |
| **Module (`nn`)** | `model = nn.Sequential(nn.Linear(10, 5), nn.ReLU())` | Inside `nn.Sequential` containers or when defining network layers in `__init__`. |
| **Functional (`F`)** | `x = F.relu(self.fc(x))` | Inside the `forward` pass of an `nn.Module` for cleaner, stateless code. |

Under the hood, `nn.ReLU` simply calls `F.relu` during its forward pass.

### What is the `inplace=True` flag in PyTorch?

Some activations (like `nn.ReLU` or `nn.LeakyReLU`) accept an `inplace` argument.

```python
# Modifies the input tensor directly without allocating new memory
nn.ReLU(inplace=True) 
```

- **Pros:** Saves VRAM by overwriting intermediate activation tensors instead of allocating fresh buffers.
- **Cons:** Destroys the original input tensor. If that input is needed elsewhere (like in a residual connection `x + conv(x)`), it will trigger a runtime error during backpropagation.

### How do you implement SwiGLU in PyTorch?

Because PyTorch does not have a native single-class `nn.SwiGLU`, you build it by combining `F.silu` with linear projections.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SwiGLU(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()
        self.w = nn.Linear(d_model, d_ff) # Gate path
        self.v = nn.Linear(d_model, d_ff) # Value path

    def forward(self, x):
        # Element-wise multiplication of the gated SiLU and the value projection
        return F.silu(self.w(x)) * self.v(x)
```

### Why use `nn.LogSoftmax` instead of `nn.Softmax`?

While `nn.Softmax` outputs clean probabilities, calculating probabilities explicitly can cause log-underflow issues when passing them to a loss function.

`nn.LogSoftmax` computes the logarithm of the softmax mathematically inside a single, fused step:

```python
# Highly stable alternative to torch.log(F.softmax(x, dim=-1))
output = F.log_softmax(x, dim=-1)
```

Pairing raw logits with `nn.CrossEntropyLoss` is usually preferred because it applies this logarithmic optimization under the hood automatically.

### What does the `dim` parameter in PyTorch Softmax mean?

The `dim` (dimension) parameter specifies the axis along which the probabilities must sum to 1.

```python
# For a batch of token logits: [batch_size, sequence_length, vocab_size]
output = F.softmax(logits, dim=-1)
```

- `dim=-1` (or `dim=2` in this case) ensures the competition happens across the *vocabulary word choices*, making sure the tokens sum to 1.
- Choosing the wrong dimension (like `dim=0`) will accidentally force competition across different *batches*, entirely breaking the model's logic.