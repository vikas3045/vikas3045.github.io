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
| Leaky ReLU | Leaky Rectified Linear Unit | $x$ if $x>0$, else $\alpha x$ | `(-infinity, infinity)` |
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
  <path d="M56,215L68,215L80,215L92,215L104,215L116,215L128,215L140,215L152,215L164,215L176,215L188,214L200,214L212,214L224,213L236,211L248,208L260,204L272,196L284,185L296,169L308,148L320,124L332,100L344,79L356,63L368,52L380,44L392,40L404,37L416,35L428,34L440,34L452,34L464,33L476,33L488,33L500,33L512,33L524,33L536,33L548,33L560,33L572,33L584,33" fill="none" stroke="#8b6fcb" stroke-width="2.5"></path>
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

### How does ReLU die?

A ReLU unit can die when it outputs zero for almost all inputs.

If the pre-activation is always negative:

$$
\operatorname{ReLU}(x)=0
$$

and the gradient is also zero.

The unit may stop learning.

This is why variants like Leaky ReLU, PReLU, ELU, GELU, and SiLU preserve some negative-side signal.

### What fixes ReLU's harsh cutoff?

| Activation | Full form | Core idea |
| --- | --- | --- |
| Leaky ReLU | Leaky Rectified Linear Unit | Keep a small fixed negative slope |
| PReLU | Parametric Rectified Linear Unit | Learn the negative slope |
| ELU | Exponential Linear Unit | Smoothly map negatives toward `-\alpha` |
| SELU | Scaled Exponential Linear Unit | ELU-like activation for self-normalizing networks |

Use these when plain ReLU is too harsh, especially if dead neurons or negative-signal loss seem problematic.

SELU is special: it expects conditions like LeCun normal initialization and alpha dropout.

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

For large positive inputs, it behaves like `x`.

For large negative inputs, it approaches `0`.

It is useful when you need a smooth positive output, such as variance, rate, scale, or another positive parameter.

### SiLU / Swish: what matters?

SiLU stands for Sigmoid Linear Unit.

$$
\operatorname{SiLU}(x)=x\sigma(x)
$$

Swish is:

$$
\operatorname{Swish}(x)=x\sigma(\beta x)
$$

When `beta = 1`, Swish is SiLU.

The intuition: SiLU softly gates the input by its own sigmoid. It keeps large positive values, smoothly downweights negatives, and preserves some small negative signal.

### GELU: what matters?

GELU stands for Gaussian Error Linear Unit.

$$
\operatorname{GELU}(x)=x\Phi(x)
$$

Where `Phi(x)` is the standard normal CDF.

GELU is like a smooth, probabilistic ReLU: instead of hard-clipping negatives, it softly gates values based on magnitude.

It is common in transformer MLP blocks.

### GELU approximation: why know it?

A common approximation is:

$$
\operatorname{GELU}(x) \approx 0.5x\left(1+\tanh\left(\sqrt{\frac{2}{\pi}}(x+0.044715x^3)\right)\right)
$$

This avoids computing the exact normal CDF.

You do not usually need to implement this by hand, but recognizing it helps when reading model code.

## Softmax and Outputs

### Softmax: what is it?

Softmax turns a vector of logits into a probability distribution.

$$
\operatorname{softmax}(z_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
$$

Each output is positive, and all outputs sum to `1`.

Unlike sigmoid or ReLU, softmax is not elementwise. Each output depends on every logit.

### Softmax: what's the intuition?

Softmax makes classes compete.

Increasing one logit increases that class probability and lowers the relative probability of other classes.

Use softmax when exactly one class should be correct.

Examples:

- Digit classification
- Single-label image classification
- Next-token prediction
- Mutually exclusive classes

### Why max-shift softmax?

Exponentials can overflow for large logits.

Use:

$$
\operatorname{softmax}(z_i)=\frac{e^{z_i-m}}{\sum_j e^{z_j-m}}
$$

Where:

$$
m=\max_j z_j
$$

Subtracting the same constant from every logit does not change the probabilities, but it prevents very large exponentials.

### Sigmoid or softmax?

Use sigmoid when outputs are independent.

Use softmax when outputs compete.

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

Many libraries combine the output activation and loss for numerical stability.

Examples:

- Binary cross-entropy with logits combines sigmoid and binary cross-entropy.
- Cross-entropy loss for multi-class classification often combines softmax and negative log likelihood.

This avoids unstable computations like taking `log` of probabilities that are extremely close to `0`.

Practical rule: check whether the loss expects raw logits or already-activated probabilities. Passing both can silently hurt training.

## Modern Architecture Choices

### GLU: what is the idea?

GLU stands for Gated Linear Unit.

A GLU splits a projection into two parts: values and gates.

One common form is:

$$
\operatorname{GLU}(x)=a \otimes \sigma(b)
$$

Where `a` and `b` are learned projections, and `\otimes` means elementwise multiplication.

The model learns what information to pass through.

### SwiGLU: why care?

SwiGLU is a gated activation that uses a Swish or SiLU-style gate.

A simplified form is:

$$
\operatorname{SwiGLU}(x)=a \otimes \operatorname{SiLU}(b)
$$

It is common in modern transformer feedforward blocks.

For basics, learn ReLU, sigmoid, tanh, softmax, GELU, and SiLU first. Then treat GLU and SwiGLU as architecture refinements.

### What's a sane hidden-layer default?

Practical defaults:

| Architecture / use case | Good default |
| --- | --- |
| Simple MLP | ReLU or GELU |
| CNN | ReLU, Leaky ReLU, or SiLU |
| Transformer | GELU, SiLU, or SwiGLU |
| Recurrent gates | Sigmoid and tanh |
| Positive scalar output | Softplus |

When in doubt, start with the activation used by the architecture you are implementing.

### ReLU, GELU, or SiLU?

Use ReLU when you want a fast, simple baseline.

Use GELU when you are working with transformer-style architectures or want smooth probabilistic gating.

Use SiLU when you want a smooth ReLU-like activation that preserves small negative signal.

| Activation | Main benefit | Main drawback |
| --- | --- | --- |
| ReLU | Fast and simple | Can kill negative signal |
| GELU | Smooth and transformer-friendly | More expensive than ReLU |
| SiLU | Smooth and preserves small negative signal | More expensive than ReLU |

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

### What's the common beginner trap?

The biggest beginner mistake is choosing activations only by habit.

Ask:

- What should the output mean?
- Are labels mutually exclusive or independent?
- Does the loss expect logits or probabilities?
- Does the activation saturate?
- Does it preserve useful gradients?
- Does the architecture expect a specific activation?

Output activations define prediction meaning. Hidden activations shape optimization.

### What's the takeaway?

Remember:

- Activations add non-linearity.
- Hidden activations shape learning dynamics.
- Output activations shape prediction meaning.
- Saturating activations can vanish gradients.
- ReLU is simple and strong.
- GELU and SiLU are smooth modern defaults.
- Sigmoid is for probabilities and gates.
- Softmax is for competing classes.
- There is no universally best activation.
