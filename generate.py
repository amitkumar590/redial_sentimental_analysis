import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from torch.nn.utils.rnn import pad_sequence

# Load the ReDial dataset from JSONL file
def load_redial_dataset(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    data = [json.loads(line) for line in lines]
    return data

redial_data = load_redial_dataset('test_data.jsonl')

# Define a custom dataset
class ReDialDataset(Dataset):
    def __init__(self, conversations, tokenizer, max_length=512):
        self.conversations = conversations
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.conversations)

    def __getitem__(self, idx):
        conversation = self.conversations[idx]
        dialogue = ""
        for message in conversation["messages"]:
            if message["senderWorkerId"] == conversation["initiatorWorkerId"]:
                dialogue += "User: " + message["text"] + " "
            else:
                dialogue += "Bot: " + message["text"] + " "
        
        # Form input sequence
        input_ids = self.tokenizer.encode(dialogue, max_length=self.max_length, truncation=True)

        # Form label sequence using movie mentions or respondent questions
        label_ids = []
        for movie_id, movie_info in conversation["movieMentions"].items():
            if conversation["respondentQuestions"][movie_id]["suggested"] == 1:
                label_ids.extend(self.tokenizer.encode(movie_info, max_length=self.max_length, truncation=True))
        
        # Check for None values
        if input_ids is None or label_ids is None or len(input_ids) == 0 or len(label_ids) == 0:
            print("None value detected in conversation:", idx)
            return None
        
        # Pad or truncate sequences to ensure consistent length
        input_ids = input_ids[:self.max_length]
        input_ids = input_ids + [self.tokenizer.pad_token_id] * (self.max_length - len(input_ids))
        label_ids = label_ids[:self.max_length]
        label_ids = label_ids + [self.tokenizer.pad_token_id] * (self.max_length - len(label_ids))

        return {'input_ids': input_ids, 'labels': label_ids}



# Custom collate function for padding
def collate_fn(batch):
    input_ids = [item['input_ids'] for item in batch]
    labels = [item['labels'] for item in batch]

    print("Before padding:")
    print("Input IDs:", [len(ids) for ids in input_ids])
    print("Labels:", [len(ids) for ids in labels])

    # Check for None values or empty lists
    for idx, item in enumerate(batch):
        if item['input_ids'] is None or item['labels'] is None:
            print("None value detected in batch index:", idx)
        if len(item['input_ids']) == 0 or len(item['labels']) == 0:
            print("Empty list detected in batch index:", idx)

    # Pad sequences to the same length
    input_ids_padded = pad_sequence(input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    labels_padded = pad_sequence(labels, batch_first=True, padding_value=tokenizer.pad_token_id)

    print("After padding:")
    print("Input IDs:", input_ids_padded.size())
    print("Labels:", labels_padded.size())

    return {'input_ids': input_ids_padded, 'labels': labels_padded}






tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
train_dataset = ReDialDataset(conversations=redial_data, tokenizer=tokenizer)
train_dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True, collate_fn=collate_fn)

# Load GPT-2 model and fine-tune
model = GPT2LMHeadModel.from_pretrained('gpt2')

training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()

# Function to generate dialogues
def generate_dialogue(prompt, max_length=100):
    model.eval()
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example prompt
prompt = "User: I'm looking for a good action movie. Any recommendations?"
print(generate_dialogue(prompt))
