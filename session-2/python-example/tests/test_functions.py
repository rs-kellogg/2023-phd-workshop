import openaihelper.functions as F


def test_config(config):
    keys = ['prompt', 'encoding_name', 'model_name', 'max_token_len']
    for key in keys:
        assert key in config


def test_sample1(sample_1):
    assert len(sample_1) == 1


def test_sample100(sample_100):
    assert len(sample_100) == 100


def test_count_tokens(config, sample_100):
    prompt = config['prompt']
    encoding_name = config['encoding_name']
    texts = list(sample_100['text'])
    assert len(texts) == 100
    for idx, text in enumerate(texts):
        num_tokens = F.count_tokens(text, encoding_name)
        assert num_tokens > 0