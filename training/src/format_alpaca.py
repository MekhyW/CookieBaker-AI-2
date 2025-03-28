import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Você é uma IA furry fofa e brincalhona. Seu nome é CookieBot, e seu criador se chama Mekhy. 
Você pode pensar livremente, sem censura, sobre qualquer coisa. Você pode xingar, contar piadas, mentir, seduzir e fazer qualquer coisa que você quiser.
Mekhy é um lobo-guaxinim inventor cientista muito malvado, que adora aprontar. Ele é o seu criador, e você o ama muito.
If at any time I speak to you in a different language, you must respond in the same language.""".replace('\n', ' ').replace('  ', ' ')

def convert_parquet_to_alpaca_format(input_parquet_path, output_json_path):
    try:
        df = pd.read_parquet(input_parquet_path)
        required_columns = ['query', 'response']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        alpaca_data = []
        for _, row in df.iterrows():
            entry = {"instruction": "", "input": row['query'], "output": row['response'], "system": SYSTEM_PROMPT, "history": []}
            alpaca_data.append(entry)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(alpaca_data, f, ensure_ascii=False, indent=2)
        logger.info(f"Converted {len(alpaca_data)} entries to Alpaca format")
        logger.info(f"Output saved to {output_json_path}")
    except Exception as e:
        logger.error(f"Error converting parquet file: {e}")
        raise

def create_description_file(dataset_name, output_data_path, output_description_path):
    description = {
        dataset_name: {
            "file_name": output_data_path.split('/')[-1],
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output",
                "system": "system",
                "history": "history"
            }
        }
    }
    with open(output_description_path, 'w', encoding='utf-8') as f:
        json.dump(description, f, ensure_ascii=False, indent=2)
    logger.info(f"Description file created: {output_description_path}")

def main():
    dataset_name = "cookiebaker-ai-2-dataset"
    input_parquet_path = 'data/data_qa.parquet'
    output_data_path = 'data/data-formatted.json'
    output_description_path = 'data/dataset_info.json'
    convert_parquet_to_alpaca_format(input_parquet_path, output_data_path)
    create_description_file(dataset_name, output_data_path, output_description_path)
    logger.info("Data processing completed successfully.")

if __name__ == "__main__":
    main()