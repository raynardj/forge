# Forge

### A Machine Learning Task Page/Butler/Assistant/Helper

Like cooking, after you've done some machine learning experiment in your jupyter notebook, you'll leave behind a trial of mess in the kitchen.

Ask your self have you encountered the following:

* Hmmmm.... what hyper-parameter did I change for last epoch?
* I increased this h-param to 64, which yields the F1 score 0.879, wait... what was my F1 before this?
* I'm putting my model to production, I clearly remember the model weight ```nlp_binary_cls-v0.2.5.npy``` was my best performer, but what was the activation function for its attention mask again?
* I think I have a decent translation model by now, I can use it to build an API!... only if I stored that version of word-to-index mapping relationship 2 days ago

Forge is originally created to organize the above chaos with minimal extra coding, and parallel access through WebUI/python.

Hopefully, this tracking mechanism will evolve to a way offering clearer sense of managing your AI/Learning tasks.

### The Web UI

Forge offers a [Web UI solution](forge/README.md) for administrative cleaning up your AI tasks.


### Python code API

```forgebox``` is a [python api](forgebox/README.md) that you can add to your python script or jupyter notebook cell. You can train your model happily in the way you like, with very limited addition to your original code. And read/check/review your training trial on a clean shaved Web interface.

