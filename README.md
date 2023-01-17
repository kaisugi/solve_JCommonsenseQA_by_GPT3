# solve_JCommonsenseQA_by_GPT3

GPT-3 (text-davinci-003) を使って JCommonsenseQA を解く

## Download datasets

```
bash download.sh
```

## Evaluation

```
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX python main.py \
  --test_file datasets/jcommonsenseqa-v1.1/valid-v1.1.json \
  --prediction_file prediction_valid.txt
```

### 手元の実行結果

```
Accuracy: 0.8543342269883825 ( 956 / 1119 )
```